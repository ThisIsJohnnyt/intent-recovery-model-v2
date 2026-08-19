# North Star

> The model should adapt to the person — not the person to the model.

The mission is to help people recover their own intent with as little
cognitive and emotional burden as possible.

Not "organize notes."
Not "summarize text."
Not "detect ADHD."

Every dataset, evaluation, and architecture decision should be checked
against one question:

**Does this make it easier for the user to recover what mattered, without
forcing them to relive more than they need to?**

If the answer is no, redesign it.

## The task: Intent Recovery

This project defines a distinct supervised learning problem, not just an
application of an existing one. Common NLP tasks — translation,
summarization, classification, named entity recognition, sentiment
analysis — all take well-formed text as input. Ours doesn't.

**Intent Recovery**

- **Input**: fragmented human cognition — scattered, interrupted,
  incomplete notes written under real-world conditions (time pressure,
  distraction, fatigue, excitement).
- **Output**: recovered intent — what the person was actually trying to
  capture, structured and readable, without inventing what wasn't there and
  without forcing them to re-enter the state they wrote it in.

The distinction matters: a generic summarizer optimizes for shorter text
that preserves meaning. Intent Recovery optimizes for recovering what the
person meant to preserve — including tasks they didn't finish writing,
topics interleaved without transition, and the difference between an
observation and an action item — while explicitly declining to invent
detail that isn't there (see the "No Magic Examples" check in
[`docs/datasets/REVIEW_GUIDE.md`](../datasets/REVIEW_GUIDE.md)) and while
never assuming *why* a note is fragmented (no diagnosis framing — see
[`training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md)).

## Collaboration model

- **Product owner** (the user): owns the problem and the vision — the lived
  experience of what it's like to look at your own note and not want to
  mentally return to the state you wrote it in just to understand it.
- **Claude**: engineering lead and corpus steward — repository, training
  scripts, export/deployment, debugging, and dataset specification,
  taxonomy, and review methodology.
- **Gemini**: dataset generator — produces synthetic examples against the
  spec Claude and the product owner define, under the diversity/balance and
  difficulty-progression rules in [`docs/datasets/`](../datasets/).

Dataset-content decisions (exactly which examples, how many per category,
how evaluation is scored) come from the product owner, with Claude and
Gemini each contributing within their roles above. Significant project
decisions are recorded in [`../decisions/`](../decisions/) as they're made,
not left to chat history.

**Decisions are evidence-driven and independently checked** — evaluation
itself is a shared practice, not a role assigned to one collaborator. The
mechanics of how that actually happens day to day (who writes what, when)
live in [`../datasets/REVIEW_GUIDE.md`](../datasets/REVIEW_GUIDE.md) and
[`AI_COLLABORATION.md`](AI_COLLABORATION.md), not here — this document
states the value, not the procedure.

## Guiding values

Project-wide values that hold regardless of which release or which
collaborator is involved. See [`AI_COLLABORATION.md`](AI_COLLABORATION.md)
for how these actually get carried out day to day — this section states
what and why, not how.

**Repository Authority** — the committed repository is the authoritative
representation of project state. Conversation history provides context, not
truth. When repository state and conversational context disagree, the
discrepancy must be surfaced rather than silently resolved. This isn't
specific to AI collaborators — it's a general engineering principle that
happens to matter especially here, since a proposal made without checking
the actual repo is exactly how conflicts start. See `AI_COLLABORATION.md`'s
"Conflict resolution" for the procedure this principle requires.

**Preserve Decision History** — decisions should be recorded once,
referenced often, and reconsidered only with new evidence, not re-litigated
from scratch each time a question resurfaces. This is why
[`../decisions/`](../decisions/) exists: so nobody has to reconstruct *why*
something was decided from chat history months later.
