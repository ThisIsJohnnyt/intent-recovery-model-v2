# Category quick reference

For tagging `category` on real notes in "Real Examples for Human Input.txt".
Full definitions and history: [`docs/datasets/TAXONOMY.md`](../docs/datasets/TAXONOMY.md).

Pick whichever category is the **dominant** skill the note exercises — real
notes often teach more than one thing at once, unlike synthetic examples
written to isolate a single lesson. It doesn't need to be pure.

Not a closed list. If a note teaches something none of these fit, flag it
rather than forcing it into the nearest one.

---

- **simple_list** — Baseline recovery: a mostly-explicit list, low ambiguity.
  _"milk, eggs, call dentist, return library books"_

- **interrupted_thought** — A thought cut off and left unfinished, vs. one
  cut off and resumed later in the note.
  _"need to talk to sam about the— oh also don't forget the—"_

- **topic_switching** — An abrupt, transition-free jump between unrelated
  subjects.
  _Jumps from a work deadline straight to a birthday gift idea._

- **topic_interleaving** — Topics *woven* through the note out of order, not
  just sequenced one after another.
  _Work and home threads alternating line by line._

- **dangling_reference** — A reference only the writer would understand —
  never guessed at, stays unresolved.
  _"the thing with the blue folder"_

- **repeated_reminder** — A task restated more than once (maybe reworded),
  recognized as one item, not two.
  _Same errand mentioned near the top and again near the bottom._

- **zero_action_items** — A correctly empty `action_items` array rather than
  an invented task.
  _Pure observation or venting, no task implied._

- **contradictory_statement** — A mood or intention that shifts partway
  through, preserved rather than resolved.
  _"so excited about this" … later … "not sure I even want to do it"_

- **rapid_branching** — One idea spawning several sub-ideas in quick
  succession, none flattened into a single generic point.
  _A hyperfocus burst where each line spins off the last._

- **minimal_fragment** — A very short, thin note, not over-elaborated.
  _1–2 lines, little structure._

- **long_rambling** — A long, loosely structured note where low-salience
  fragments aren't lost or merged under compression pressure.
  _Many small points across a long note, none individually load-bearing._

- **multi_person_note** — A fragment correctly attributed to the right
  person when more than one is mentioned.
  _"sam wants pizza, jen said she's not hungry"_

- **voice_to_text_artifact** — Intent recovered through transcription-layer
  noise, distinct from the writer's own phrasing choices.
  _"so i need to um pick up the the dry cleaning"_

- **self_correction** — An explicit retraction honored — the retracted
  content dropped, not preserved alongside the correction.
  _"call the plumber — actually no, forget that, already handled it"_

- **time_ambiguous** — A vague time reference preserved as still vague, not
  resolved to something specific.
  _"before the thing on friday, or maybe after"_
