"""
Tests for the model's I/O contract: prepare_data.serialize_target /
deserialize_target and validate_record.

WHY THIS FILE EXISTS
--------------------
The subtlest bug this project has hit was found by burning a training run.
flan-t5's SentencePiece tokenizer normalises "\\n" to a plain space at
ENCODE time, so the newlines serialize_target() writes never survive to a
real model -- and deserialize_target() was splitting on newlines that no
longer existed anywhere in the pipeline. Every eval example failed to parse
despite visibly-correct output (commit 0749442, 2026-08-25). That is a
~10-line property test, and there wasn't one: the repository had no tests,
no conftest, no CI (external review 2026-09-02, finding M7).

The load-bearing test here is test_round_trip_survives_newline_collapse:
it simulates the tokenizer's collapse and asserts the round-trip still
holds. If someone "tidies up" deserialize_target back into splitting on
"\\n", that test fails instead of the next training run.

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
    """Simulate what flan-t5's SentencePiece does to newlines at encode time.

    Confirmed by tokenizing "X\\nY" and "X Y" and getting identical token
    ids -- see prepare_data.deserialize_target's docstring, which is the
    authoritative write-up of this behaviour.
    """
    return re.sub(r"\s*\n\s*", " ", text)


def load_corpus():
    if not CORPUS.exists():
        return []
    return [json.loads(l) for l in CORPUS.read_text(encoding="utf-8").splitlines() if l.strip()]


# --------------------------------------------------------------------------
# Round-trip properties
# --------------------------------------------------------------------------

def test_round_trip_survives_newline_collapse():
    """serialize -> collapse newlines -> deserialize must reproduce the output.

    This is the regression guard for the bug that cost a training run.
    """
    records = load_corpus()
    assert records, f"no corpus at {CORPUS} -- this test needs real data"
    mismatches = []
    for i, r in enumerate(records, 1):
        expected = r["output"]
        got = pd.deserialize_target(through_tokenizer(pd.serialize_target(expected)))
        if (got["narrative"] != " ".join(expected["narrative"].split("\n"))
                or got["bullets"] != expected["bullets"]
                or got["action_items"] != expected["action_items"]):
            mismatches.append(i)
    assert not mismatches, f"round-trip failed on corpus lines: {mismatches[:20]}"


def test_round_trip_empty_action_items():
    """A zero_action_items record must survive with action_items still empty.

    The empty-section case is where a delimiter format is most likely to
    break: "###ACTIONS###" is followed by nothing at all.
    """
    out = {"narrative": "I am just watching the rain.", "bullets": ["Watching the rain"],
           "action_items": []}
    got = pd.deserialize_target(through_tokenizer(pd.serialize_target(out)))
    assert got["action_items"] == []
    assert got["bullets"] == ["Watching the rain"]
    assert got["narrative"] == "I am just watching the rain."


def test_round_trip_empty_bullets():
    out = {"narrative": "I am just watching the rain.", "bullets": [],
           "action_items": ["Watch the rain"]}
    got = pd.deserialize_target(through_tokenizer(pd.serialize_target(out)))
    assert got["bullets"] == []
    assert got["action_items"] == ["Watch the rain"]


def test_round_trip_both_lists_empty():
    out = {"narrative": "Nothing to do.", "bullets": [], "action_items": []}
    got = pd.deserialize_target(through_tokenizer(pd.serialize_target(out)))
    assert got["bullets"] == []
    assert got["action_items"] == []
    assert got["narrative"] == "Nothing to do."


def test_all_three_markers_always_present():
    """Headers appear even when their section is empty, so a parser never has
    to guess whether a section was omitted or genuinely empty."""
    text = pd.serialize_target({"narrative": "n", "bullets": [], "action_items": []})
    for marker in ("###NARRATIVE###", "###BULLETS###", "###ACTIONS###"):
        assert marker in text, f"{marker} missing from serialized output"


def test_corpus_content_never_contains_the_delimiter():
    """If record text could contain '###', the format would be corruptible."""
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
