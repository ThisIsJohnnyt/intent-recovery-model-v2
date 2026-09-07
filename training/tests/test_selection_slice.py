"""
Tests for prepare_data.py's train/selection split (PDR-007, external review
finding C3).

WHY THIS FILE EXISTS
--------------------
Before this fix, train.py selected its checkpoint (load_best_model_at_end)
on datasets/real_validation.jsonl -- the same 15 records evaluate_real.py
then reported as the generalization result. Once a checkpoint is chosen on
a set, results on that set stop being a generalization estimate. The fix
carves a selection-only slice out of the synthetic/gold pool instead, by
deterministic content-hash bucketing, and keeps the real tier out of the
training pipeline entirely.

These tests guard the two properties that matter: the split is a true
partition (nothing duplicated, nothing dropped, membership depends only on
content) and real_validation.jsonl never re-enters the training pipeline
through resolve_source_files(). If either regresses, C3 is back.

Run:
    pytest training/tests/
    python training/tests/test_selection_slice.py     # no pytest needed
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "training"))

import prepare_data as pd  # noqa: E402


def _record(text: str) -> dict:
    return {"input": text, "output": {"narrative": "n", "bullets": [], "action_items": []}}


# --------------------------------------------------------------------------
# is_in_selection_slice -- deterministic, content-keyed
# --------------------------------------------------------------------------

def test_membership_depends_only_on_input_text():
    """Same `input` text must land in the same bucket regardless of what
    else is in the record or where it sits in a list -- this is what makes
    the split stable as the corpus grows, unlike a position- or index-based
    split would be."""
    r1 = _record("buy milk and call the plumber")
    r2 = {"input": "buy milk and call the plumber",
          "output": {"narrative": "different narrative entirely",
                     "bullets": ["x"], "action_items": ["y"]}}
    assert pd.is_in_selection_slice(r1) == pd.is_in_selection_slice(r2)


def test_membership_is_stable_across_repeated_calls():
    r = _record("a note that should hash the same way every time")
    first = pd.is_in_selection_slice(r)
    for _ in range(5):
        assert pd.is_in_selection_slice(r) == first


def test_not_every_record_is_selected():
    """A degenerate bucketing that always returns True (or always False)
    would silently defeat either training or selection. Sample enough
    distinct strings that both outcomes must appear if the fraction is
    doing anything at all."""
    records = [_record(f"synthetic note number {i} about something ordinary") for i in range(200)]
    outcomes = {pd.is_in_selection_slice(r) for r in records}
    assert outcomes == {True, False}, (
        f"expected both train and selection outcomes across 200 distinct "
        f"records, got only {outcomes}"
    )


def test_selection_fraction_is_in_the_right_ballpark():
    """Not a precise statistical test -- just a guard that the fraction
    selected across a large, varied sample is somewhere near
    SELECTION_SLICE_FRACTION rather than wildly off (e.g. an off-by-one in
    the modulo arithmetic)."""
    records = [_record(f"note {i} with some varying content {i * 7}") for i in range(2000)]
    selected = sum(pd.is_in_selection_slice(r) for r in records)
    fraction = selected / len(records)
    target = pd.SELECTION_SLICE_FRACTION
    assert abs(fraction - target) < 0.03, (
        f"selected fraction {fraction:.3f} too far from target {target:.3f}"
    )


# --------------------------------------------------------------------------
# split_train_selection -- true partition
# --------------------------------------------------------------------------

def test_split_is_a_complete_partition():
    """Every input record ends up in exactly one of the two output lists,
    nothing duplicated, nothing dropped."""
    records = [_record(f"unique note text {i}") for i in range(150)]
    train, selection = pd.split_train_selection(records)
    assert len(train) + len(selection) == len(records)
    train_texts = {r["input"] for r in train}
    selection_texts = {r["input"] for r in selection}
    assert train_texts.isdisjoint(selection_texts)
    assert train_texts | selection_texts == {r["input"] for r in records}


def test_split_agrees_with_is_in_selection_slice():
    records = [_record(f"note {i}") for i in range(50)]
    train, selection = pd.split_train_selection(records)
    assert all(not pd.is_in_selection_slice(r) for r in train)
    assert all(pd.is_in_selection_slice(r) for r in selection)


# --------------------------------------------------------------------------
# The real tier must never re-enter the training pipeline through this path
# --------------------------------------------------------------------------

def test_resolve_source_files_never_includes_real_validation():
    """This is the actual regression guard for C3: if real_validation.jsonl
    ever gets added back into the files this function returns, it goes
    straight back into train.py's selection set, silently."""
    files = pd.resolve_source_files()
    names = {p.name for p in files}
    assert "real_validation.jsonl" not in names
    assert "real_holdout.jsonl" not in names


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
