"""
Tests for the model's I/O contract: prepare_data.serialize_target /
deserialize_target (both TARGET_FORMAT options) and validate_record.

WHY THIS FILE EXISTS
--------------------
The subtlest bug this project has hit was found by burning a training run.
flan-t5's SentencePiece tokenizer normalised "\\n" to a plain space at
ENCODE time, so the newlines the original delimited serializer wrote never
survived to a real model -- and its deserializer was splitting on newlines
that no longer existed anywhere in the pipeline. Every eval example failed
to parse despite visibly-correct output (commit 0749442, 2026-08-25). That
is a ~10-line property test, and there wasn't one: the repository had no
tests, no conftest, no CI (external review 2026-09-02, finding M7).

test_delimited_round_trip_survives_newline_collapse is the regression guard
for that bug, kept even though JSON is the active TARGET_FORMAT since
PDR-012 (base model migration) -- the delimited format is still a live,
switchable fallback (see prepare_data.py's TARGET_FORMAT comment), and its
parser still depends on not splitting on "\\n" for the same reason it always
did. If someone "tidies up" _deserialize_target_delimited back into
splitting on "\\n", this test fails instead of the next training run that
happens to reactivate that format.

The JSON-format tests below don't need an equivalent newline-collapse
guard: JSON parsing is whitespace-agnostic regardless of how indentation
survives tokenization (confirmed empirically 2026-09-09 that Qwen's
tokenizer does NOT collapse newlines the way flan-t5's did, but it
wouldn't matter for this format either way).

Run:
    pytest training/tests/
    python training/tests/test_serialization.py     # no pytest needed
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "training"))

import prepare_data as pd  # noqa: E402

CORPUS = REPO_ROOT / "datasets" / "synthetic.jsonl"


def through_tokenizer(text: str) -> str:
    """Simulate what flan-t5's SentencePiece did to newlines at encode time.

    Confirmed by tokenizing "X\\nY" and "X Y" and getting identical token
    ids -- see _deserialize_target_delimited's docstring, which is the
    authoritative write-up of this behaviour. Only meaningful for the
    delimited format's own tests below -- the current model (Qwen) does
    not do this, but the delimited fallback must still tolerate it if it's
    ever reactivated on a tokenizer that does.
    """
    return re.sub(r"\s*\n\s*", " ", text)


def load_corpus():
    if not CORPUS.exists():
        return []
    return [json.loads(l) for l in CORPUS.read_text(encoding="utf-8").splitlines() if l.strip()]


# --------------------------------------------------------------------------
# JSON format (TARGET_FORMAT="json", the active default since PDR-012)
# --------------------------------------------------------------------------

def test_json_round_trip_on_corpus():
    records = load_corpus()
    assert records, f"no corpus at {CORPUS} -- this test needs real data"
    mismatches = []
    for i, r in enumerate(records, 1):
        expected = r["output"]
        got = pd._deserialize_target_json(pd._serialize_target_json(expected))
        if (got["narrative"] != expected["narrative"]
                or got["bullets"] != expected["bullets"]
                or got["action_items"] != expected["action_items"]):
            mismatches.append(i)
    assert not mismatches, f"round-trip failed on corpus lines: {mismatches[:20]}"


def test_json_round_trip_empty_action_items():
    out = {"narrative": "I am just watching the rain.", "bullets": ["Watching the rain"],
           "action_items": []}
    got = pd._deserialize_target_json(pd._serialize_target_json(out))
    assert got == out


def test_json_round_trip_empty_bullets():
    out = {"narrative": "I am just watching the rain.", "bullets": [],
           "action_items": ["Watch the rain"]}
    got = pd._deserialize_target_json(pd._serialize_target_json(out))
    assert got == out


def test_json_round_trip_both_lists_empty():
    out = {"narrative": "Nothing to do.", "bullets": [], "action_items": []}
    got = pd._deserialize_target_json(pd._serialize_target_json(out))
    assert got == out


def test_json_deserialize_raises_on_malformed_input():
    """An early-stop-truncated or otherwise malformed generation must raise
    json.JSONDecodeError, not silently degrade -- callers (evaluate_real.py,
    probe_adversarial.py) rely on this to distinguish a genuine syntax
    error from a repeat-guard truncation."""
    try:
        pd._deserialize_target_json('{"narrative": "unterminated')
        raise AssertionError("expected JSONDecodeError, got no exception")
    except json.JSONDecodeError:
        pass


def test_json_deserialize_raises_on_non_object_json():
    """Valid JSON that isn't an object (e.g. a bare string or list) is
    still not a usable target -- must raise the same exception type as a
    syntax error so callers only need one except clause."""
    try:
        pd._deserialize_target_json('["not", "an", "object"]')
        raise AssertionError("expected JSONDecodeError, got no exception")
    except json.JSONDecodeError:
        pass


def test_active_target_format_dispatches_to_json():
    """serialize_target()/deserialize_target() are dispatchers over
    TARGET_FORMAT -- this pins the currently-active default so a change to
    that constant is a deliberate, visible test failure, not silent."""
    assert pd.TARGET_FORMAT == "json"
    out = {"narrative": "n", "bullets": ["b"], "action_items": []}
    assert pd.serialize_target(out) == pd._serialize_target_json(out)


# --------------------------------------------------------------------------
# Delimited format (TARGET_FORMAT="delimited") -- kept as a measured
# fallback since PDR-012; not the active default. See that constant's
# comment in prepare_data.py.
# --------------------------------------------------------------------------

def test_delimited_round_trip_survives_newline_collapse():
    """serialize -> collapse newlines -> deserialize must reproduce the
    output. This is the regression guard for the bug that cost a training
    run -- see this file's module docstring."""
    records = load_corpus()
    assert records, f"no corpus at {CORPUS} -- this test needs real data"
    mismatches = []
    for i, r in enumerate(records, 1):
        expected = r["output"]
        got = pd._deserialize_target_delimited(
            through_tokenizer(pd._serialize_target_delimited(expected))
        )
        if (got["narrative"] != " ".join(expected["narrative"].split("\n"))
                or got["bullets"] != expected["bullets"]
                or got["action_items"] != expected["action_items"]):
            mismatches.append(i)
    assert not mismatches, f"round-trip failed on corpus lines: {mismatches[:20]}"


def test_delimited_round_trip_empty_action_items():
    """A zero_action_items record must survive with action_items still empty.

    The empty-section case is where a delimiter format is most likely to
    break: "###ACTIONS###" is followed by nothing at all.
    """
    out = {"narrative": "I am just watching the rain.", "bullets": ["Watching the rain"],
           "action_items": []}
    got = pd._deserialize_target_delimited(through_tokenizer(pd._serialize_target_delimited(out)))
    assert got["action_items"] == []
    assert got["bullets"] == ["Watching the rain"]
    assert got["narrative"] == "I am just watching the rain."


def test_delimited_round_trip_empty_bullets():
    out = {"narrative": "I am just watching the rain.", "bullets": [],
           "action_items": ["Watch the rain"]}
    got = pd._deserialize_target_delimited(through_tokenizer(pd._serialize_target_delimited(out)))
    assert got["bullets"] == []
    assert got["action_items"] == ["Watch the rain"]


def test_delimited_round_trip_both_lists_empty():
    out = {"narrative": "Nothing to do.", "bullets": [], "action_items": []}
    got = pd._deserialize_target_delimited(through_tokenizer(pd._serialize_target_delimited(out)))
    assert got["bullets"] == []
    assert got["action_items"] == []
    assert got["narrative"] == "Nothing to do."


def test_delimited_all_three_markers_always_present():
    """Headers appear even when their section is empty, so a parser never has
    to guess whether a section was omitted or genuinely empty."""
    text = pd._serialize_target_delimited({"narrative": "n", "bullets": [], "action_items": []})
    for marker in ("###NARRATIVE###", "###BULLETS###", "###ACTIONS###"):
        assert marker in text, f"{marker} missing from serialized output"


def test_corpus_content_never_contains_the_delimiter():
    """If record text could contain '###', the delimited fallback format
    would be corruptible -- checked regardless of which format is
    currently active, since TARGET_FORMAT is a one-line switch back to it."""
    offenders = [i for i, r in enumerate(load_corpus(), 1)
                 if "###" in json.dumps(r, ensure_ascii=False)]
    assert not offenders, f"'###' found in record content at lines: {offenders[:20]}"


# --------------------------------------------------------------------------
# Schema validation -- one rejection case per rule validate_record enforces
# --------------------------------------------------------------------------

def _expect_schema_error(record, why):
    try:
        pd.validate_record(record, "test", 1)
    except pd.SchemaError:
        return
    raise AssertionError(f"validate_record accepted {why}: {record!r}")


def _valid():
    return {"input": "a note", "output": {"narrative": "I have a note.",
                                          "bullets": ["A note"], "action_items": []}}


def test_validate_accepts_a_good_record():
    pd.validate_record(_valid(), "test", 1)  # must not raise


def test_validate_rejects_missing_top_level_fields():
    _expect_schema_error({"output": {}}, "a record with no input")
    _expect_schema_error({"input": "x"}, "a record with no output")


def test_validate_rejects_empty_or_non_string_input():
    r = _valid(); r["input"] = ""
    _expect_schema_error(r, "an empty input")
    r = _valid(); r["input"] = 42
    _expect_schema_error(r, "a non-string input")


def test_validate_rejects_bad_output_shape():
    r = _valid(); r["output"] = "not an object"
    _expect_schema_error(r, "a non-object output")
    r = _valid(); del r["output"]["bullets"]
    _expect_schema_error(r, "output missing bullets")


def test_validate_rejects_empty_narrative():
    r = _valid(); r["output"]["narrative"] = ""
    _expect_schema_error(r, "an empty narrative")


def test_validate_rejects_non_list_or_non_string_items():
    r = _valid(); r["output"]["bullets"] = "not a list"
    _expect_schema_error(r, "bullets as a string")
    r = _valid(); r["output"]["action_items"] = [1, 2]
    _expect_schema_error(r, "action_items containing non-strings")


def test_validate_rejects_too_many_bullets():
    """DATASET_SPEC.md's bullets rule is "up to 7". Unenforced until an
    external review (2026-09-02, finding L4) found one record had drifted
    to 8 with nothing catching it."""
    r = _valid(); r["output"]["bullets"] = [f"point {i}" for i in range(pd.MAX_BULLETS + 1)]
    _expect_schema_error(r, "more bullets than the documented cap")


def test_validate_accepts_the_documented_maximum():
    r = _valid(); r["output"]["bullets"] = [f"point {i}" for i in range(pd.MAX_BULLETS)]
    pd.validate_record(r, "test", 1)  # must not raise


def test_validate_rejects_unknown_difficulty():
    r = _valid(); r["difficulty"] = "trivial"
    _expect_schema_error(r, "an out-of-vocabulary difficulty")


def test_validate_accepts_all_documented_difficulties():
    for d in ("easy", "medium", "hard", "expert"):
        r = _valid(); r["difficulty"] = d
        pd.validate_record(r, "test", 1)  # must not raise


def test_validate_rejects_empty_category():
    r = _valid(); r["category"] = ""
    _expect_schema_error(r, "an empty category")


# --------------------------------------------------------------------------
# Runnable without pytest, so the suite is never blocked on an install
# --------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failures = []
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            failures.append((name, e))
            print(f"  FAIL  {name}: {e}")
    print(f"\n{len(tests) - len(failures)}/{len(tests)} passed")
    sys.exit(1 if failures else 0)
