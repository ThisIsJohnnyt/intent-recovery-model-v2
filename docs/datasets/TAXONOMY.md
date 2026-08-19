# Taxonomy

**Not yet designed.** This file is scaffolded as part of this repository's
initial structure ([PDR-001](../decisions/PDR-001.md)); v2.0's own category
vocabulary, difficulty tiers, and boundary/confidence categories are real
next-work, out of scope for the fork itself.

When designed, this file will define:

- **Category vocabulary** — the set of specific recovery skills an example
  can teach (its `category` field in
  [`training_data.schema.json`](training_data.schema.json)), each with a
  short definition and an example.
- **Difficulty categories** — the tier vocabulary for `difficulty` (the
  predecessor project used Basic/Moderate/Complex/High Cognitive Load,
  mapping to `easy`/`medium`/`hard`/`expert`; whether v2.0 keeps this exact
  mapping is an open question for whoever designs this next).
- **Boundary categories** / **Confidence categories** — the vocabulary for
  describing segmentation boundaries and how confidently they're signaled,
  used in design notes (see [`DESIGN_NOTES_TEMPLATE.md`](DESIGN_NOTES_TEMPLATE.md)),
  never in the trained JSONL itself.
- **Dataset labeling rules** — including the "preserve uncertainty" rule
  from [`docs/vision/GOLD_PHILOSOPHY.md`](../vision/GOLD_PHILOSOPHY.md).

See [`CATEGORY_REFERENCE.md`](CATEGORY_REFERENCE.md) for the (also not yet
populated) per-category detail this file's vocabulary will link out to.
