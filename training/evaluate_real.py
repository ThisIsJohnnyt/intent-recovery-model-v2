#!/usr/bin/env python3
"""
Run a trained checkpoint against datasets/real_validation.jsonl -- the
generalization check this project's real tier exists for. See
DATASET_SPEC.md's "real_validation.jsonl" entry: no generative model wrote
these 15 examples, so a good result here means something a synthetic-only
eval can't -- that the model recovers a real person's notes, not just
Gemini's idea of what a messy note looks like.

This is deliberately NOT wired to real_holdout.jsonl. DATASET_SPEC.md is
explicit that the holdout tier is "evaluated only by a separate, explicit
holdout-evaluation script" -- sealed for declared release milestones, not
routine dev-time checks. Add that script only when there's an actual
release milestone to evaluate against, as its own deliberate action.

Reuses prepare_data.py's serialize_target/deserialize_target and
TASK_PREFIX rather than a second implementation of the model's I/O
contract -- see that module's "Model output serialization" docstring.

No automatic pass/fail scoring: at corpus sizes this small, a numeric
score would carry false precision. What this prints is (a) whether the
model's raw output even parses as the delimited format at all -- a
structural sanity check -- and (b) narrative-to-narrative and
narrative-to-input similarity, using this project's own established
copy-ratio methodology (see REVIEW_GUIDE.md ss4 "No non-recovery"), so a
model that's just echoing the input is visible the same way a bad
synthetic example would be. Full input/expected/actual is printed for
every example -- reading them is the actual evaluation.

Usage (from training/):
    python evaluate_real.py
    python evaluate_real.py --checkpoint checkpoints/flan-t5-base-v2.0
    python evaluate_real.py --max-new-tokens 384
"""
import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
DEFAULT_CHECKPOINT = Path(__file__).resolve().parent / "checkpoints" / "qwen3.5-4b-v2.0"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare_data  # noqa: E402  (reuse serialize/deserialize + TASK_PREFIX)


def word_ratio(a: str, b: str) -> float:
    # Word-boundary regex, not str.split() -- punctuation used to be part
    # of the token ("him" vs "him,"), so adding/removing a comma moved the
    # score with zero real reorganization. External review (Claude
    # API/Fable 5.1, 2026-09-07, finding C5): confirmed by hand against
    # the corpus, not just by argument -- e.g. one record's narrative
    # reproduced its input word-for-word, differing only by punctuation,
    # and scored 0.615 under the old tokenization vs the correct 1.000
    # (zero recovery) under this one.
    ta = re.findall(r"\b\w+\b", a.lower())
    tb = re.findall(r"\b\w+\b", b.lower())
    return SequenceMatcher(None, ta, tb).ratio()


def dedupe_consecutive(items: list) -> list:
    """Drop any entry that's an exact duplicate of the one immediately
    before it. Cleanup layer on top of ConsecutiveRepeatStop, not a
    replacement for it -- see that class's docstring. The stopping
    criteria bounds how much a degenerate loop can generate before
    halting (at minimum `repeats` copies, structurally unavoidable for a
    generation-time guard); this guarantees the copies that do make it
    through never reach the printed/reported result. Zero interaction
    with generation itself, so zero risk of the token-level corruption
    approaches like repetition_penalty caused -- this only touches the
    already-generated, already-parsed list."""
    out = []
    for item in items:
        if not out or item != out[-1]:
            out.append(item)
    return out


class ConsecutiveRepeatStop:
    """Halts generation when a span of tokens repeats immediately,
    back-to-back, self.repeats times in a row.

    Replaces an earlier `no_repeat_ngram_size` guard (2026-09-07) that
    banned a recurring span ANYWHERE in the sequence, regardless of
    distance. That caught the real bug -- a real note's action_items
    repeating "Replace the valves in the shower" as a separate list entry
    25 times -- but a direct measurement against all 15 real_validation.jsonl
    records found 7 of 15 (47%) have a bullet and its own matching action
    item legitimately sharing a verbatim span of >=6 tokens, exactly what
    that guard also blocked, forcing the model onto corrupted substitutes
    ("Reuters"->"rihanna", "Claude"->"Francois", meaning-inverting
    "remember"->"forget") when repetition_penalty was tried, and silent
    list-item fusion even with the plain n-gram ban.

    The property that actually distinguishes the two cases is ADJACENCY,
    not span length: the pathological case is the same span repeating
    immediately; a bullet and its action item are never adjacent in the
    generated sequence (narrative, other bullets, and/or the ###ACTIONS###
    marker sit between them). Checking for CONSECUTIVE repetition instead
    of "has this appeared before, anywhere" structurally can't trigger on
    the legitimate case at all -- it doesn't need to know which section a
    token came from.

    Confirmed the original bug was terminal (the loop filled the rest of
    generation, nothing came after it -- ACTIONS is the last section in
    this format) before choosing a stopping criteria over a mid-sequence
    logits processor. Reviewed via the Claude<->Gemini bridge
    (review_bridge/), 2026-09-08.

    `repeats=2`, not 3: a stopping criteria can only halt FUTURE
    generation, not undo tokens already emitted, so `repeats=N` always
    leaves N copies in the final output at minimum -- the first real test
    (repeats=3) left 3 identical action items behind. The adjacency
    property above holds exactly as well at 2 as at 3 (a 4+ token span
    repeating immediately, back-to-back, by pure coincidence in normal
    generated text isn't something that happens outside genuine
    pathology), so there's no real safety cost to catching it a repeat
    earlier. See `dedupe_consecutive` below for cleanup of the 1-2 copies
    this still can't prevent from reaching the output.

    `prompt_length` (since PDR-012's causal-LM migration): a causal LM's
    `generate()` feeds `input_ids` containing the WHOLE prompt+generation-
    so-far to every stopping criteria call, from step one -- unlike
    seq2seq's decoder-only `input_ids`, which only ever held generated
    tokens. Without slicing the prompt span off before checking for
    repeats, a repeated span already present in the user's own note (see
    the bullet<->action_item overlap this class exists to tolerate, above)
    could falsely count toward a halt before the model has generated
    anything at all. Must be constructed fresh per generation call, with
    that specific call's actual prompt length -- reusing one instance
    across multiple generate() calls (or across records) would silently
    apply the wrong prompt_length to every call after the first.

    `self.fired`: set True the moment this criteria actually triggers a
    halt. Lets a caller distinguish "this generation was cut short by the
    repeat guard" from "this generation completed normally but produced
    malformed output" -- the same-looking symptom (output fails to parse)
    has two different causes, and only one of them is a genuine model
    defect. See evaluate_real.py's parse-failure categorization below.
    """

    def __init__(self, prompt_length: int, min_window: int = 4, max_window: int = 50,
                 repeats: int = 2):
        # Deferred import, not module-level -- matches this file's own
        # pattern (torch is only imported inside main(), once it's known
        # to actually be needed). Imported once here, at instantiation,
        # not per generation step in __call__.
        import torch
        self._torch = torch
        self.prompt_length = prompt_length
        self.min_window = min_window
        self.max_window = max_window
        self.repeats = repeats
        self.fired = False

    def __call__(self, input_ids, scores, **kwargs):
        # transformers.StoppingCriteriaList.__call__ ORs each criterion's
        # result into a running torch.BoolTensor shaped (batch_size,) --
        # matching that return type/shape exactly here rather than
        # returning a bare Python bool, since only `input_ids.shape[0]` is
        # actually guaranteed at this call site (batch size 1 everywhere
        # in this tool today, but this class shouldn't silently assume it).
        # Sliced to the generated span only -- see prompt_length's own
        # docstring above for why the full input_ids can't be used as-is
        # for a causal LM.
        seq = input_ids[0, self.prompt_length:].tolist()
        done = False
        for w in range(self.min_window, self.max_window + 1):
            need = w * self.repeats
            if len(seq) < need:
                continue
            tail = seq[-need:]
            chunks = [tail[i * w:(i + 1) * w] for i in range(self.repeats)]
            if all(c == chunks[0] for c in chunks):
                done = True
                break
        if done:
            self.fired = True
        return self._torch.full((input_ids.shape[0],), done, dtype=self._torch.bool,
                                 device=input_ids.device)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT,
                    help="directory holding the fine-tuned LoRA adapter "
                         "(default: training/checkpoints/qwen3.5-4b-v2.0)")
    ap.add_argument("--real-validation", type=Path, default=DATASETS_DIR / "real_validation.jsonl")
    ap.add_argument("--max-new-tokens", type=int, default=prepare_data.MAX_TARGET_LENGTH)
    ap.add_argument("--limit", type=int, default=None, help="evaluate only the first N examples")
    args = ap.parse_args()

    if not args.checkpoint.exists():
        print(f"error: checkpoint not found at {args.checkpoint}\n"
              f"Train one first (see training/train.py) -- there is nothing to evaluate yet.",
              file=sys.stderr)
        return 2

    records = prepare_data.load_jsonl(args.real_validation)
    if not records:
        print(f"error: {args.real_validation} has no records -- nothing to evaluate against.",
              file=sys.stderr)
        return 2
    if args.limit:
        records = records[:args.limit]

    print(f"Loading checkpoint from {args.checkpoint} ...")
    import torch
    from transformers import AutoTokenizer, StoppingCriteriaList
    from peft import AutoPeftModelForCausalLM
    import model_config
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint)
    # AutoPeftModelForCausalLM, not AutoModelForCausalLM -- train.py's
    # trainer.save_model() saved only the LoRA adapter (standard QLoRA
    # practice; a merged bf16 checkpoint wouldn't fit this hardware's
    # VRAM at all -- see PDR-012). This reads the base model name
    # straight out of the adapter's own saved adapter_config.json and
    # loads base+adapter together; nothing here needs to separately know
    # or pass "Qwen/Qwen3.5-4B".
    model = AutoPeftModelForCausalLM.from_pretrained(
        str(args.checkpoint),
        quantization_config=model_config.build_bnb_config(),
        device_map="auto",
    )
    model.eval()
    device = model.device  # decided by device_map="auto", not a guessed string
    print(f"Device: {device}. Evaluating {len(records)} example(s) from {args.real_validation.name}.\n")

    counts = {"parse_ok": 0, "early_stop_truncation": 0, "genuine_syntax_error": 0}
    narrative_vs_expected, narrative_vs_input = [], []

    for i, r in enumerate(records, 1):
        messages = [
            {"role": "system", "content": prepare_data.TASK_PREFIX},
            {"role": "user", "content": r["input"]},
        ]
        enc = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, enable_thinking=False,
            return_tensors="pt", return_dict=True,
        ).to(device)
        prompt_length = enc["input_ids"].shape[1]

        # See ConsecutiveRepeatStop's own docstring for the full history
        # (why it exists) and for why it must be constructed fresh here,
        # inside the loop, with THIS record's prompt_length -- reusing one
        # instance across records would silently apply the wrong
        # prompt_length (and carry over a stale `fired` flag) to every
        # record after the first.
        stop = ConsecutiveRepeatStop(prompt_length=prompt_length)
        stopping_criteria = StoppingCriteriaList([stop])
        with torch.no_grad():
            out_ids = model.generate(
                **enc,
                max_new_tokens=args.max_new_tokens,
                stopping_criteria=stopping_criteria,
            )
        # A causal LM's generate() returns prompt+generation concatenated
        # -- slice the prompt back off before decoding, unlike seq2seq
        # where out_ids only ever held the decoder's own output.
        gen_ids = out_ids[0][prompt_length:]
        raw_output = tokenizer.decode(gen_ids, skip_special_tokens=True)

        try:
            parsed = prepare_data.deserialize_target(raw_output)
            if not isinstance(parsed, dict) or not parsed.get("narrative"):
                raise ValueError("parsed output has no usable narrative")
            structurally_valid = True
        except (json.JSONDecodeError, ValueError):
            structurally_valid = False
            parsed = {"narrative": "", "bullets": [], "action_items": []}

        parsed["bullets"] = dedupe_consecutive(parsed["bullets"])
        parsed["action_items"] = dedupe_consecutive(parsed["action_items"])

        if structurally_valid:
            counts["parse_ok"] += 1
        else:
            # Two different causes look identical from the outside (raw
            # output that doesn't parse) -- distinguish them by whether
            # the repeat guard actually fired, not just whether the
            # output happens to be malformed. See PDR-012 and
            # ConsecutiveRepeatStop.fired's own docstring.
            category = "early_stop_truncation" if stop.fired else "genuine_syntax_error"
            counts[category] += 1

        print(f"{'=' * 70}\n#{i} [{r.get('category', '?')}]")
        print(f"INPUT:    {r['input']}")
        print(f"EXPECTED: {r['output']['narrative']}")
        print(f"  bullets:      {r['output']['bullets']}")
        print(f"  action_items: {r['output']['action_items']}")
        print(f"ACTUAL:   {parsed['narrative'] or '(did not parse -- raw output below)'}")
        if not structurally_valid:
            print(f"  did not parse ({'early-stop truncation' if stop.fired else 'genuine syntax error'})")
            print(f"  raw model output: {raw_output!r}")
        else:
            print(f"  bullets:      {parsed['bullets']}")
            print(f"  action_items: {parsed['action_items']}")
            r_exp = word_ratio(parsed["narrative"], r["output"]["narrative"])
            r_inp = word_ratio(parsed["narrative"], r["input"])
            narrative_vs_expected.append(r_exp)
            narrative_vs_input.append(r_inp)
            print(f"  narrative-vs-expected similarity: {r_exp:.2f}   "
                  f"narrative-vs-input similarity: {r_inp:.2f}")
        print()

    print(f"{'=' * 70}\nSummary: {counts['parse_ok']}/{len(records)} produced a structurally "
          f"valid (parseable) output. Of the rest: {counts['early_stop_truncation']} were cut "
          f"short by the repeat guard (not a syntax defect), "
          f"{counts['genuine_syntax_error']} were genuine syntax errors on a complete "
          f"generation.")
    if narrative_vs_expected:
        print(f"Mean narrative-vs-expected similarity: "
              f"{sum(narrative_vs_expected) / len(narrative_vs_expected):.2f}")
        print(f"Mean narrative-vs-input similarity:    "
              f"{sum(narrative_vs_input) / len(narrative_vs_input):.2f}  "
              f"(high here means the model is echoing the input rather than recovering it -- "
              f"see REVIEW_GUIDE.md's 'No non-recovery')")
    print("\nThese numbers are not a pass/fail score -- read the per-example output above. "
          "At this corpus size a small numeric summary would carry false precision.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
