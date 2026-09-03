# Copy-ratio disposition -- proposed calls for all 58 breaches

**Purpose:** decide which of the 58 non-allowlisted copy-ratio breaches
(`docs/reviews/2026-09-02-copy-ratio-breaches.md`) get rewritten to genuinely
reorganize their input, and which get added to `check_copy_ratio.py`'s
allowlist as a correct high ratio (the #118/#127 case: nothing to reorganize).

**How to use this:** each entry has my proposed call and a one-line reason.
Mark **A** (approve) or **O** (override) in the `YOUR CALL` line under each one.
For an override, a word or two on what you want instead is enough -- I will
apply it. Leaving a line blank is the same as A.

**Proposed split:** 29 REWRITE, 29 ALLOWLIST.

One general pattern across most REWRITE calls, so it doesn't repeat 29 times:
the narrative tracks the input's own clause order with only
capitalization/connective changes, while the input actually contains multiple
separable facts or tasks that a genuinely reorganized narrative could lead
with, group, or compress differently. Most ALLOWLIST calls are the opposite
shape: the input is already short, already in the correct narrative order, or
is a single continuous personal reflection where reordering would be
artificial rather than recovery.

`interrupted_thought` note: several short ALLOWLIST calls in that category
have almost no content before their literal cutoff ("the--", "if--") -- the
cutoff itself, preserved verbatim, dominates the text, the same structural
reason #118 is allowlisted for dangling_reference. The REWRITE calls in the
same category (262, 340, 339, 465, 287, 338) have substantial content
*before* their cutoff that still needs to stay verbatim once rewritten -- none
of these proposals touch a cutoff itself.

---

## #262 -- interrupted_thought/medium

**INPUT:** call mom about the thanksgiving menu and ask if she has the recipe for the sweet potato casserole because last year it was so -- wait did i leave the stove on

**NARRATIVE:** I need to call Mom about the Thanksgiving menu and ask if she has the recipe for the sweet potato casserole because last year it was so -- wait did i leave the stove on

**PROPOSED: REWRITE** -- Named directly by the external review as the worst case -- narrative is the input verbatim apart from capitalization. Real content before the cutoff (mom/menu/recipe/last-year clause) to reorganize; keep "it was so --" verbatim.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #340 -- interrupted_thought/medium

**INPUT:** need to scrub the bathtub and maybe clean the mirrors if i have time, also vacuum the rug in the hallw-

**NARRATIVE:** I need to scrub the bathtub and maybe clean the mirrors if I have time, and also vacuum the rug in the hallw-

**PROPOSED: REWRITE** -- Three listable tasks (bathtub, mirrors, rug) compressed into connective tweaks only. Keep "hallw-" verbatim, reorganize the rest.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #185 -- time_ambiguous/hard

**INPUT:** Send the update tomorrow unless they reply today, but I don't think they're in the office until next week anyway.

**NARRATIVE:** I should send the update tomorrow unless they reply today, but I don't think they're in the office until next week anyway.

**PROPOSED: ALLOWLIST** -- Single already-ordered sentence, nothing to reorganize -- same shape as #118/#127.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #180 -- zero_action_items/easy

**INPUT:** The sky looks very hazy today. The AQI must be high. Noticing a lot of dust on the windowsills.

**NARRATIVE:** The sky looks very hazy today. The AQI must be high. I am noticing a lot of dust on the windowsills.

**PROPOSED: ALLOWLIST** -- Three short observations already in natural order; the only real compression (linking haze to AQI) would invent a causal claim the input doesn't make.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #292 -- zero_action_items/medium

**INPUT:** I was just thinking about Sarah and the summer we spent by the lake. We used to stay up all night talking on that old dock. It's crazy how fast ten years went by. I really miss that sense of freedom we had back then.

**NARRATIVE:** I was just feeling nostalgic thinking about Sarah and the summer we spent by the lake. We used to stay up all night talking on that old dock. It's crazy how fast ten years went by, and I really miss that sense of freedom we had back then.

**PROPOSED: ALLOWLIST** -- Single continuous reminiscence -- reordering a person's own train of memory would be artificial, not recovery.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #288 -- topic_switching/medium

**INPUT:** Folding these towels is taking forever, I should really clean the lint trap too. The washing machine is making a weird squeak. Oh, I just remembered the marketing email draft. I need to review the copy before noon tomorrow and approve the header image.

**NARRATIVE:** Folding these towels is taking forever, and I should really clean the lint trap too. The washing machine is making a weird squeak. Separately, I just remembered the marketing email draft; I need to review the copy before noon tomorrow and approve the header image.

**PROPOSED: REWRITE** -- Two-part topic switch, correctly structured, but each segment is compressible beyond "add a connective word".

**YOUR CALL:** [ ] A   [ ] O ->

---

## #442 -- zero_action_items/hard

**INPUT:** everything feels too loud today. the hum of the refrigerator is driving me crazy and I just feel completely burned out. I can't even focus on this book I'm trying to read. my brain is just static right now.

**NARRATIVE:** Everything feels too loud today. The hum of the refrigerator is driving me crazy, and I just feel completely burned out. I can't even focus on this book I'm trying to read, as my brain is just static right now.

**PROPOSED: REWRITE** -- Four distinct facts (loud, fridge hum, burned out, can't focus) presented in input order with no real compression.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #202 -- time_ambiguous/hard

**INPUT:** need to pay the property tax bill soon. probably next Friday when I get paid, or maybe the Monday after if the deposit doesn't clear right away. just has to be done before the end of the month so we don't get a penalty.

**NARRATIVE:** I need to pay the property tax bill soon. I will probably do it next Friday when I get paid, or maybe the Monday after if the deposit doesn't clear right away. It just has to be done before the end of the month so we don't get a penalty.

**PROPOSED: ALLOWLIST** -- Already logically ordered (hedge, hedge, deadline) -- that's the correct narrative order too.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #498 -- topic_switching/expert

**INPUT:** submit the reimbursement form by friday. oh wait, did he ever send the thing over? i can't find it in my email.

**NARRATIVE:** I need to submit the reimbursement form by Friday. Oh wait, did he ever send the thing over? I can't find it in my email.

**PROPOSED: ALLOWLIST** -- Very short, two sentences -- nothing to reorganize.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #188 -- topic_switching/medium

**INPUT:** I'll do 20 minutes of scales and then work on the bridge of that jazz piece. after that I should probably look up how to file a tax extension just in case my W2 doesn't arrive.

**NARRATIVE:** I plan to do 20 minutes of scales and then work on the bridge of that jazz piece. After that, I should probably look up how to file a tax extension just in case my W2 doesn't arrive.

**PROPOSED: ALLOWLIST** -- Naturally sequential plan (do X then Y); chronological order is the correct narrative order.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #339 -- interrupted_thought/hard

**INPUT:** i really want to track down that original pressing of the jazz album, maybe check the local store downtown or I could look on discogs before they-- anyway I need to finish these dishes.

**NARRATIVE:** I really want to track down that original pressing of the jazz album. I could maybe check the local store downtown or look on Discogs before they-- anyway I need to finish these dishes.

**PROPOSED: REWRITE** -- Real content (album-hunting options, dishes) before the cutoff; keep "they--" verbatim, reorganize the rest.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #282 -- long_rambling/hard

**INPUT:** Found grandma's old recipe box. It smells like her kitchen. Most of these are written on index cards, I think I should scan them so they don't fade. The date on the pie recipe is 1982. There's a picture of her in here too, I want to get a nice wooden frame for it. Also need to ask mom if she remembers the secret ingredient for the gravy, it just says 'spices'. I miss those Sunday dinners.

**NARRATIVE:** I found grandma's old recipe box, and it smells just like her kitchen. Most of the recipes are written on index cards, and I think I should scan them so they don't fade. I noticed the date on the pie recipe is 1982. There's a picture of her in here too, and I want to get a nice wooden frame for it. I also need to ask mom if she remembers the secret ingredient for the gravy, as it just says 'spices'. I really miss those Sunday dinners.

**PROPOSED: REWRITE** -- Long, many distinct facts (recipe box, index cards, 1982 date, photo, gravy question) -- real reordering/compression available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #295 -- multi_person_note/hard

**INPUT:** We totally nailed the presentation outline! Alex is doing the historical context slides. I need to gather the primary sources tonight. Maria said she will present the conclusion. David is supposed to format the bibliography but I haven't heard from him yet.

**NARRATIVE:** We totally nailed the presentation outline! For next steps, Alex is doing the historical context slides, and I need to gather the primary sources tonight. Maria said she will present the conclusion. David is supposed to format the bibliography, but I haven't heard from him yet.

**PROPOSED: REWRITE** -- Four people/facts in input order with only connective changes -- real reorganization available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #465 -- interrupted_thought/medium

**INPUT:** the meeting notes from Tuesday said we should review the wireframes before Friday, but didn't Jessica say she was going to— anyway check the shared folder.

**NARRATIVE:** The meeting notes from Tuesday said we should review the wireframes before Friday, but didn't Jessica say she was going to— anyway, I need to check the shared folder.

**PROPOSED: REWRITE** -- Real content (wireframe deadline, Jessica's cutoff, shared folder) before/around the cutoff to reorganize.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #409 -- multi_person_note/medium

**INPUT:** Liam is supposed to draft the opening statement by Wednesday and I have to review the witness list by then maybe Sam can pull the previous case files if he has time

**NARRATIVE:** Liam is supposed to draft the opening statement by Wednesday, and I have to review the witness list by then. Maybe Sam can pull the previous case files if he has time.

**PROPOSED: REWRITE** -- 30 words, three facts (Liam/Wednesday, witness list, Sam maybe) copied in input order with only punctuation changes.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #166 -- interrupted_thought/easy

**INPUT:** need to pick up milk and bread from the store. also check if they have the good brand of

**NARRATIVE:** I need to pick up milk and bread from the store. I also need to check if they have the good brand of

**PROPOSED: ALLOWLIST** -- Minimal pre-cutoff content (two grocery items); the cutoff itself dominates.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #333 -- dangling_reference/hard

**INPUT:** i think sarah is mad at me about what happened yesterday. probably should text her. honey left his jacket here.

**NARRATIVE:** I think Sarah is mad at me about what happened yesterday, and I probably should text her. Honey left his jacket here.

**PROPOSED: ALLOWLIST** -- Short, two sentences, deliberately disconnected fragment (honey left his jacket) -- little to reorganize.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #489 -- multi_person_note/easy

**INPUT:** jessica is drafting the email. i need to pull the analytics for her by noon.

**NARRATIVE:** Jessica is drafting the email, and I need to pull the analytics for her by noon.

**PROPOSED: ALLOWLIST** -- Very short, single sentence.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #334 -- dangling_reference/medium

**INPUT:** saw that cool thing at the antique store on 4th street maybe i should go back and buy it.

**NARRATIVE:** I saw that cool thing at the antique store on 4th street, and maybe I should go back and buy it.

**PROPOSED: ALLOWLIST** -- Single sentence.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #335 -- self_correction/expert

**INPUT:** mark is handling the server migration on tuesday, actually no wait make that wednesday. sarah said she would check the backups, and i probably should email the client. order pizza for the team.

**NARRATIVE:** Mark is handling the server migration on Wednesday. Sarah said she would check the backups, and I probably should email the client. Order pizza for the team.

**PROPOSED: ALLOWLIST** -- Compact list of four short facts, already in a reasonable order; self_correction has already dropped the retracted Tuesday.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #290 -- dangling_reference/easy

**INPUT:** Reviewing the meeting notes. I really doubt the new timeline is feasible. Need to ask Mark about that specific issue he raised yesterday, I'm not sure what it means for my deliverables.

**NARRATIVE:** I am reviewing the meeting notes and I really doubt the new timeline is feasible. I need to ask Mark about that specific issue he raised yesterday, because I'm not sure what it means for my deliverables.

**PROPOSED: ALLOWLIST** -- Short, two sentences.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #386 -- zero_action_items/expert

**INPUT:** I really want to go to the gym later. I always feel better after I lift. But my lower back is feeling weirdly tight today. So maybe I should just rest it. Rest is important for recovery. Although if I don't go I'll feel lazy and I haven't gone since Tuesday. But injuring myself would be worse. I don't know.

**NARRATIVE:** I really want to go to the gym later because I always feel better after I lift, but my lower back is feeling weirdly tight today. So maybe I should just rest it, since rest is important for recovery. Although if I don't go I'll feel lazy, especially since I haven't gone since Tuesday. But injuring myself would be worse. I don't know.

**PROPOSED: REWRITE** -- Long internal debate (gym vs. rest, six distinct considerations) tracked almost sentence-for-sentence -- real compression available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #284 -- long_rambling/hard

**INPUT:** Three syllabi to read, I'm already behind. History book is out of stock at the bookstore, need to find a PDF online. The dates for the sociology essays are all clustered in November, I should put those in my calendar right now. Physics has a group project, I need to email the TA to see how groups are assigned. Plus office hours are on Thursdays, which conflicts with my shift. Have to talk to my manager about swapping days.

**NARRATIVE:** I have three syllabi to read and I'm already feeling behind. The history book is out of stock at the bookstore, so I need to find a PDF online. The dates for the sociology essays are all clustered in November, which I should put in my calendar right now. Physics has a group project, and I need to email the TA to see how groups are assigned. Plus, office hours are on Thursdays, which conflicts with my shift, so I have to talk to my manager about swapping days.

**PROPOSED: REWRITE** -- Long, five distinct facts (syllabi, history book, sociology dates, physics group, office hours conflict) in input order only.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #457 -- contradictory_statement/expert

**INPUT:** I should definitely sign up for that pottery class next week or maybe wait until fall because summer is too crazy, although taking it now might be good.

**NARRATIVE:** I should definitely sign up for that pottery class next week, or maybe wait until fall because summer is too crazy. Although, taking it now might be good.

**PROPOSED: ALLOWLIST** -- Short, single flowing sentence, already well-ordered.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #471 -- zero_action_items/hard

**INPUT:** The therapist said I should try journaling my dreams but frankly it sounds exhausting to write right after waking up, though maybe it would help with the nightmares, I really don't know if I'll actually do it.

**NARRATIVE:** The therapist said I should try journaling my dreams, but frankly, it sounds exhausting to write right after waking up. Though maybe it would help with the nightmares. I really don't know if I'll actually do it.

**PROPOSED: ALLOWLIST** -- Single flowing thought ending in genuine indecision -- already confirmed content-correct in the twelfth re-review; little structure to recover beyond what bullets already extract.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #389 -- contradictory_statement/easy

**INPUT:** Going to sell my old tablet online. I haven't turned it on in a year. But what if I need a backup device if my laptop breaks? It's good to have a backup. But it is just gathering dust. I can't decide if I want to get rid of it.

**NARRATIVE:** I am going to sell my old tablet online since I haven't turned it on in a year. But what if I need it as a backup device if my laptop ever breaks? It's good to have a backup. But it is just gathering dust. I can't decide if I want to get rid of it or not.

**PROPOSED: ALLOWLIST** -- Already confirmed content-correct in an earlier re-review; short, single flowing deliberation.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #448 -- time_ambiguous/expert

**INPUT:** schedule the vet appointment for Buster for Tuesday morning. or maybe afternoon would be better. actually wait, they might be closed on Tuesdays. I should probably check their hours first before trying to call.

**NARRATIVE:** I wanted to schedule the vet appointment for Buster for Tuesday morning, or maybe the afternoon would be better. Actually, wait, they might be closed on Tuesdays. I should probably check their hours first before trying to call.

**PROPOSED: REWRITE** -- Real multi-step content (vet appt, day hedge, closed-Tuesday realization, check-hours plan) copied in input order only.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #488 -- multi_person_note/easy

**INPUT:** i'll vacuum the living room and alex is going to clean the bathrooms.

**NARRATIVE:** I will vacuum the living room and Alex is going to clean the bathrooms.

**PROPOSED: ALLOWLIST** -- Very short, single sentence.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #226 -- voice_to_text_artifact/expert

**INPUT:** the landlord is being ridiculous I need to read the least agreement to see what the exact claws is regarding guests. mark said he might have a digital copy I think. text mark to send me his copy if he can find it, unless he deleted it.

**NARRATIVE:** The landlord is being ridiculous, so I need to read the lease agreement to see what the exact clause is regarding guests. Mark said he might have a digital copy, I think. I should text Mark to send me his copy if he can find it, unless he deleted it.

**PROPOSED: REWRITE** -- Long, real content (landlord, lease clause, Mark's copy, text-Mark plan) with only connective changes.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #285 -- long_rambling/hard

**INPUT:** So excited about the new kitten! Got the litter box set up in the bathroom. The food bowls are ceramic, which is good. Need to buy those feather toys she liked at the shelter. Not sure if I should schedule the vet check for Tuesday or Wednesday, have to look at my work meetings. Also need to look up articles on introducing a kitten to an older dog, Buster is going to be so confused.

**NARRATIVE:** I am so excited about the new kitten! I got the litter box set up in the bathroom, and the ceramic food bowls are ready, which is good. I need to buy those feather toys she liked at the shelter. I am not sure if I should schedule the vet check for Tuesday or Wednesday, so I have to look at my work meetings first. I also need to look up articles on introducing a kitten to an older dog, because Buster is going to be so confused.

**PROPOSED: REWRITE** -- Long, many distinct facts (kitten, litter box, food bowls, toys, vet-day hedge, dog introduction) in input order only.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #299 -- topic_switching/hard

**INPUT:** Looking at grandpa's old pocket watch on my desk, it always reminds me of the stories he used to tell about the railroad. Such a different era. Oh, the router light is blinking red again. I need to unplug the modem for 30 seconds and reboot the network, this internet dropping is getting ridiculous.

**NARRATIVE:** Looking at grandpa's old pocket watch on my desk always reminds me of the stories he used to tell about the railroad, which was such a different era. Oh, the router light is blinking red again, so I need to unplug the modem for 30 seconds and reboot the network since this internet dropping is getting ridiculous.

**PROPOSED: REWRITE** -- Two segments (pocket watch reflection, router troubleshooting), each compressible beyond connective changes.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #236 -- time_ambiguous/hard

**INPUT:** need to pick up the dry cleaning before they close at 6 or maybe 7. I think they changed their hours recently. call them around noon to check. also grab milk on the way back.

**NARRATIVE:** I need to pick up the dry cleaning before they close at 6 or maybe 7, as I think they changed their hours recently. I should call them around noon to check, and also grab milk on the way back.

**PROPOSED: ALLOWLIST** -- Natural sequential planning order (deadline hedge, call-to-check plan, milk) -- matches how a person would narrate their own plan.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #462 -- interrupted_thought/easy

**INPUT:** remind Mark about the tickets for Saturday and ask him if—

**NARRATIVE:** I need to remind Mark about the tickets for Saturday and ask him if—

**PROPOSED: ALLOWLIST** -- Minimal pre-cutoff content, single clause.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #390 -- long_rambling/easy

**INPUT:** Thinking about the concept of time and how it seems to move faster the older I get. When I was a kid summer break felt like an entire lifetime. Now a year goes by in a flash. It's probably because we don't have as many novel experiences as adults. We just do the same routine every day. Work, dinner, sleep. The brain just compresses it all. I should try to break the routine more often.

**NARRATIVE:** I was thinking about the concept of time and how it seems to move faster the older I get. When I was a kid, summer break felt like an entire lifetime, but now a year goes by in a flash. It is probably because we don't have as many novel experiences as adults; we just do the same routine every day of work, dinner, and sleep, and the brain just compresses it all. I should try to break the routine more often.

**PROPOSED: ALLOWLIST** -- Reflective monologue in natural chronological/logical order; reordering would be artificial. Matches this category's own easy definition (low structural complexity).

**YOUR CALL:** [ ] A   [ ] O ->

---

## #329 -- topic_switching/medium

**INPUT:** i should probably study French verbs tonight for 20 mins. also need to take the chicken out of the freezer

**NARRATIVE:** I should probably study French verbs tonight for 20 minutes. I also need to take the chicken out of the freezer.

**PROPOSED: ALLOWLIST** -- Very short, two sentences.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #364 -- multi_person_note/hard

**INPUT:** We are trying to figure out the props for the second act and I think we need a vintage lamp but Mark insists we definitely have to use the neon sign from last year's play while Chloe said she would maybe look in her parents basement for an antique chandelier to see if that works better

**NARRATIVE:** We are trying to figure out the props for the second act of the play,. I think we need a vintage lamp, but Mark insists we definitely have to use the neon sign from last year's play. Meanwhile, Chloe said she would maybe look in her parents' basement for an antique chandelier to see if that works better.

**PROPOSED: REWRITE** -- Three people's positions on props, copied in input order with only connective changes -- real reorganization available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #407 -- multi_person_note/easy

**INPUT:** for the escape room on saturday Elise needs to book the tickets online and I should figure out where we are getting dinner beforehand

**NARRATIVE:** For the escape room on Saturday, Elise needs to book the tickets online, and I should figure out where we are getting dinner beforehand.

**PROPOSED: ALLOWLIST** -- Short, single sentence -- already confirmed content-correct in an earlier re-review.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #287 -- interrupted_thought/hard

**INPUT:** Trying to figure out why this Python script keeps throwing a syntax error on line 42. I need to restart my IDE. I checked the indents and they look fine, maybe I missed a parenthesis on the line befo— ah the cat just knocked over my water glass

**NARRATIVE:** I am trying to figure out why this Python script keeps throwing a syntax error on line 42, and I need to restart my IDE. I checked the indents and they look fine, so I was thinking maybe I missed a parenthesis on the line befo— ah, the cat just knocked over my water glass!

**PROPOSED: REWRITE** -- Real debugging narrative (syntax error, IDE restart, indent check, near-miss parenthesis) before the cutoff.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #235 -- multi_person_note/expert

**INPUT:** planning the block party for the 12th. I will handle the permit with the city. greg said he can bring his grill and do the burgers. sarah is supposedly organizing the kids games but I should follow up with her to be sure. ask tom if he still has those folding tables.

**NARRATIVE:** I am planning the block party for the 12th and will handle the permit with the city. Greg said he can bring his grill and do the burgers. Sarah is supposedly organizing the kids' games, but I should follow up with her to be sure. I also need to ask Tom if he still has those folding tables.

**PROPOSED: REWRITE** -- Four people/facts (permit, Greg's grill, Sarah's games, Tom's tables) in input order only -- real reorganization available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #433 -- repeated_reminder/expert

**INPUT:** should probably review the slide deck tonight, or maybe early tomorrow morning before the standup. I really need to go over those slides. tonight might be too late I'll be tired. but don't forget to review the slides at some point, either tonight or morning.

**NARRATIVE:** I should probably review the slide deck tonight, or maybe early tomorrow morning before the standup. I really need to go over those slides. Tonight might be too late because I'll be tired, but I cannot forget to review them at some point, either tonight or in the morning.

**PROPOSED: REWRITE** -- The repeated-reminder collapse rule applies to bullets/action_items, not narrative; narrative here is still copied almost verbatim with real compression available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #272 -- zero_action_items/easy

**INPUT:** the protagonist's motivation feels a bit weak in chapter 3. she needs a stronger reason to leave town.

**NARRATIVE:** I think the protagonist's motivation feels a bit weak in chapter 3, and she needs a stronger reason to leave town.

**PROPOSED: ALLOWLIST** -- Very short, single sentence.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #461 -- interrupted_thought/easy

**INPUT:** grab the folder for the meeting and check if the—

**NARRATIVE:** I need to grab the folder for the meeting and check if the—

**PROPOSED: ALLOWLIST** -- Minimal pre-cutoff content, single clause.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #281 -- long_rambling/medium

**INPUT:** Sorting the attic is so dull. Found three boxes of old clothes from college. Probably should donate them to the shelter downtown. There's a lot of dust up here, might need to get a better mask. Looked through some old notebooks, just scribbles. Saw a dead spider. Need to buy more trash bags before I finish this up. I think I'll just sweep the floor and call it a day soon.

**NARRATIVE:** Sorting the attic is so dull. I found three boxes of old clothes from college that I probably should donate to the shelter downtown. There's a lot of dust up here, so I might need to get a better mask. I looked through some old notebooks that were just scribbles and saw a dead spider. I need to buy more trash bags before I finish this up, but I think I'll just sweep the floor and call it a day soon.

**PROPOSED: REWRITE** -- Long, many discrete items (clothes, dust/mask, notebooks, spider, trash bags, sweeping) -- real reorganization available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #200 -- zero_action_items/medium

**INPUT:** saw the weirdest bird at the feeder today. it had a bright yellow crest but the body of a sparrow. maybe it was a finch? I don't know much about birds. it stayed around for like ten minutes just eating the black oil sunflower seeds and chasing off the squirrels.

**NARRATIVE:** I saw the weirdest bird at the feeder today. It had a bright yellow crest but the body of a sparrow, making me wonder if maybe it was a finch, though I don't know much about birds. It stayed around for about ten minutes, just eating the black oil sunflower seeds and chasing off the squirrels.

**PROPOSED: ALLOWLIST** -- Single continuous observation narrated in the order it happened; reordering an I-saw-X-it-did-Y account doesn't clearly improve it.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #298 -- time_ambiguous/medium

**INPUT:** The kitchen sink is draining so slowly. I have to call the plumber to snake the drain. Maybe I'll call them this afternoon, or I guess tomorrow morning works too since I'll be working from home.

**NARRATIVE:** The kitchen sink is draining so slowly that I have to call the plumber to snake the drain. I am considering calling them this afternoon, or I guess tomorrow morning works too since I'll be working from home.

**PROPOSED: ALLOWLIST** -- Short, sequential logical hedge (drain problem, plumber, when to call).

**YOUR CALL:** [ ] A   [ ] O ->

---

## #338 -- interrupted_thought/expert

**INPUT:** the main character could find a hidden door in the library or maybe she discovers a map inside a book or what if the librarian is a ghost-- oh shoot the timer is going off

**NARRATIVE:** I am brainstorming ideas: the main character could find a hidden door in the library, or maybe she discovers a map inside a book, or what if the librarian is a ghost-- oh shoot the timer is going off.

**PROPOSED: REWRITE** -- Three branching story ideas before a real interruption event -- genuine content to reorganize.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #447 -- multi_person_note/expert

**INPUT:** John said we should move the boxes to the basement. Mary thinks we should leave them in the hallway for now. I don't know what to do with the other ones though, the ones from upstairs. maybe someone should just decide.

**NARRATIVE:** John said we should move the boxes to the basement, but Mary thinks we should leave them in the hallway for now. I don't know what to do with the other boxes from upstairs, though. Maybe someone should just decide.

**PROPOSED: REWRITE** -- Three people's positions copied in input order with only connective changes -- real reorganization available despite being content-correct.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #346 -- contradictory_statement/hard

**INPUT:** the new app update is live for all users. wait the release notes say it only rolled out to beta testers.

**NARRATIVE:** I see the new app update is live for all users, but the release notes say it only rolled out to beta testers.

**PROPOSED: ALLOWLIST** -- Very short, two sentences.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #496 -- contradictory_statement/expert

**INPUT:** david said he paid the internet bill yesterday. check the account because david definitely hasn't paid the internet bill yet.

**NARRATIVE:** David said he paid the internet bill yesterday, but I need to check the account because David definitely hasn't paid the internet bill yet.

**PROPOSED: REWRITE** -- Three facts (David's claim, writer's certainty, need to check) copied in input order -- content-correct (confirmed in the twelfth re-review) but narrative itself is compressible.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #197 -- dangling_reference/hard

**INPUT:** submit the expense report by EOD. make sure to attach the thing they asked for in the all hands meeting. also tell John that his section of the presentation is too long. and find out if we still need to bring that other form to HR.

**NARRATIVE:** I need to submit the expense report by EOD and make sure to attach the thing they asked for in the all hands meeting. I also need to tell John that his section of the presentation is too long, and I need to find out if we still need to bring that other form to HR.

**PROPOSED: REWRITE** -- Four distinct tasks (expense report, attachment, John's section, HR form) -- real list content to reorganize.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #231 -- zero_action_items/hard

**INPUT:** the cat ate all her dry food today which is a good sign. her energy seems much better than yesterday. dr. evans called with the lab results and everything was normal. feeling very relieved.

**NARRATIVE:** The cat ate all her dry food today, which is a good sign, and her energy seems much better than yesterday. Dr. Evans called with the lab results and everything was normal, so I am feeling very relieved.

**PROPOSED: REWRITE** -- Four distinct facts (food, energy, vet call, relief) in input order -- real reorganization available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #365 -- self_correction/medium

**INPUT:** I am definitely free this weekend to help Mark move his couch. I really need to stay home the entire weekend and finish my sociology paper so I have to text Mark that I cannot help him.

**NARRATIVE:** I initially thought I was definitely free this weekend to help Mark move his couch. However, I actually really need to stay home the entire weekend to finish my sociology paper, so I have to text Mark that I cannot help him.

**PROPOSED: REWRITE** -- Real content to reorganize. Separate note, not a copy-ratio issue: the narrative narrates the retraction (I initially thought... however) rather than dropping it, which self_correction's own convention says to avoid -- worth a second look alongside any rewrite here.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #181 -- rapid_branching/hard

**INPUT:** If the bonus comes through we should book the flights, unless prices went up in which case maybe just stay home? If we stay home we need to clear out the guest room. Either way ask Jamie to watch the dog.

**NARRATIVE:** If the bonus comes through we should book the flights, unless prices went up, in which case maybe we just stay home. If we stay home, we need to clear out the guest room. Either way, I need to ask Jamie to watch the dog.

**PROPOSED: ALLOWLIST** -- Already logically ordered conditional chain (if X then Y unless Z then W); reordering would break the logic, not improve it.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #192 -- long_rambling/expert

**INPUT:** so I was looking at the yarn for the cardigan and I realized I probably don't have enough of the blue to finish the sleeves, which is annoying because I bought it on clearance like three years ago. I need to check Ravelry to see if anyone is selling a skein in that dye lot. Or maybe I just make the cuffs a different color? The gray might look okay. I'm so tired of this project honestly I've been knitting it since October. remind me to measure the back panel tomorrow morning before I start the shaping. if the dog hasn't completely tangled the working yarn again.

**NARRATIVE:** While looking at the yarn for my cardigan, I realized I probably don't have enough of the blue to finish the sleeves, which is annoying since I bought it on clearance about three years ago. I need to check Ravelry to see if anyone is selling a skein in that dye lot, or maybe I will just make the cuffs a different color, as the gray might look okay. Honestly, I'm so tired of this project because I've been knitting it since October. I need to measure the back panel tomorrow morning before I start the shaping, assuming the dog hasn't completely tangled the working yarn again.

**PROPOSED: REWRITE** -- Long, many distinct facts (yarn shortage, clearance purchase, Ravelry, cuff color, fatigue, tomorrow's plan, dog/yarn) -- real reorganization available.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #154 -- dangling_reference/hard

**INPUT:** the blue one or maybe Thursday if they still have the wide fitting otherwise just cancel it and use sarah's

**NARRATIVE:** The blue one, or maybe Thursday if they still have the wide fitting — otherwise I'll just cancel it and use Sarah's.

**PROPOSED: ALLOWLIST** -- Single flowing conditional sentence, already well-ordered; ambiguity correctly preserved.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #463 -- interrupted_thought/easy

**INPUT:** I think the dimensions are 4 by 6 but wait let me check the—

**NARRATIVE:** I think the dimensions are 4 by 6, but wait, let me check the—

**PROPOSED: ALLOWLIST** -- Minimal pre-cutoff content, single clause.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #441 -- topic_interleaving/expert

**INPUT:** talked to Mark about renewing the lease for another year, he seems on board. we are almost out of olive oil. Sarah said she might want to move out though. need to get more dish soap too. I should ask Sarah if she's made a firm decision about moving.

**NARRATIVE:** I talked to Mark about renewing the lease for another year, and he seems on board. I noticed we are almost out of olive oil. Sarah, however, said she might want to move out. We also need to get more dish soap. I should ask Sarah if she's made a firm decision about moving.

**PROPOSED: REWRITE** -- Genuine interleaving structure is preserved, but each segment's wording is compressible beyond connective changes.

**YOUR CALL:** [ ] A   [ ] O ->

---

## #253 -- multi_person_note/hard

**INPUT:** flight leaves at 8am. mark is driving us to the airport. sarah said she will book the hotel in rome but we need to pay her back for half. I need to renew my passport.

**NARRATIVE:** Our flight leaves at 8am, and Mark is driving us to the airport. Sarah said she will book the hotel in Rome, but we need to pay her back for half of it. I also need to renew my passport.

**PROPOSED: REWRITE** -- Four distinct facts (flight time, Mark driving, Sarah/hotel/payback, passport) -- real list content to reorganize.

**YOUR CALL:** [ ] A   [ ] O ->

---
