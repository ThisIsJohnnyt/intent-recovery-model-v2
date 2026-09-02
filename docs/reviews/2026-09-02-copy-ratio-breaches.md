# Copy-ratio breaches — records above 0.85, for product-owner decision

**Generated:** 2026-09-02 by `training/check_copy_ratio.py` against `datasets/synthetic.jsonl` (525 records).

This is a **report, not a work order.** `docs/datasets/REVIEW_GUIDE.md` governs
whether any of these should change, and the decision is the product owner's.
Two cautions before touching any of them:

1. REVIEW_GUIDE.md's "Fixing voice raises the copy ratio" records that this metric
   and the first-person-voice rule pull against each other — the cheapest way to
   stop describing a note is to start reciting it. Re-measure **both** after any edit.
2. A high ratio is the *correct* answer for a short, already-ordered note. That is
   exactly why #118 and #127 are permanently allowlisted. Some of the 58 below are
   likely the same case and should be allowlisted rather than rewritten.

**58 records** above 0.85, excluding the 2 allowlisted by prior decision.

## By category

| category | breaches |
|---|---|
| `interrupted_thought` | 10 |
| `multi_person_note` | 9 |
| `zero_action_items` | 8 |
| `long_rambling` | 6 |
| `time_ambiguous` | 5 |
| `topic_switching` | 5 |
| `dangling_reference` | 5 |
| `contradictory_statement` | 4 |
| `self_correction` | 2 |
| `voice_to_text_artifact` | 1 |
| `repeated_reminder` | 1 |
| `rapid_branching` | 1 |
| `topic_interleaving` | 1 |

## By difficulty

| difficulty | breaches |
|---|---|
| easy | 12 |
| medium | 13 |
| hard | 20 |
| expert | 13 |

## The records

### line 262 — 0.955 — `interrupted_thought` / medium

- **hash** `ed8b93e5a7cdf974` (use this for allowlisting; line numbers shift)
- **input:** call mom about the thanksgiving menu and ask if she has the recipe for the sweet potato casserole because last year it was so -- wait did i leave the stove on
- **narrative:** I need to call Mom about the Thanksgiving menu and ask if she has the recipe for the sweet potato casserole because last year it was so -- wait did i leave the stove on

### line 340 — 0.955 — `interrupted_thought` / medium

- **hash** `d39881efd1971640` (use this for allowlisting; line numbers shift)
- **input:** need to scrub the bathtub and maybe clean the mirrors if i have time, also vacuum the rug in the hallw-
- **narrative:** I need to scrub the bathtub and maybe clean the mirrors if I have time, and also vacuum the rug in the hallw-

### line 185 — 0.952 — `time_ambiguous` / hard

- **hash** `e8a13fec39707902` (use this for allowlisting; line numbers shift)
- **input:** Send the update tomorrow unless they reply today, but I don't think they're in the office until next week anyway.
- **narrative:** I should send the update tomorrow unless they reply today, but I don't think they're in the office until next week anyway.

### line 180 — 0.950 — `zero_action_items` / easy

- **hash** `b53d08febfdbd9da` (use this for allowlisting; line numbers shift)
- **input:** The sky looks very hazy today. The AQI must be high. Noticing a lot of dust on the windowsills.
- **narrative:** The sky looks very hazy today. The AQI must be high. I am noticing a lot of dust on the windowsills.

### line 292 — 0.946 — `zero_action_items` / medium

- **hash** `d1911e8c4e740fac` (use this for allowlisting; line numbers shift)
- **input:** I was just thinking about Sarah and the summer we spent by the lake. We used to stay up all night talking on that old dock. It's crazy how fast ten years went by. I really miss that sense of freedom we had back then.
- **narrative:** I was just feeling nostalgic thinking about Sarah and the summer we spent by the lake. We used to stay up all night talking on that old dock. It's crazy how fast ten years went by, and I really miss that sense of freedom we had back then.

### line 288 — 0.944 — `topic_switching` / medium

- **hash** `159df986909f368a` (use this for allowlisting; line numbers shift)
- **input:** Folding these towels is taking forever, I should really clean the lint trap too. The washing machine is making a weird squeak. Oh, I just remembered the marketing email draft. I need to review the copy before noon tomorrow and approve the header image.
- **narrative:** Folding these towels is taking forever, and I should really clean the lint trap too. The washing machine is making a weird squeak. Separately, I just remembered the marketing email draft; I need to review the copy before noon tomorrow and approve the header image.

### line 442 — 0.937 — `zero_action_items` / hard

- **hash** `bd0e5f3fa7f4e2cc` (use this for allowlisting; line numbers shift)
- **input:** everything feels too loud today. the hum of the refrigerator is driving me crazy and I just feel completely burned out. I can't even focus on this book I'm trying to read. my brain is just static right now.
- **narrative:** Everything feels too loud today. The hum of the refrigerator is driving me crazy, and I just feel completely burned out. I can't even focus on this book I'm trying to read, as my brain is just static right now.

### line 498 — 0.936 — `topic_switching` / expert

- **hash** `c45b1c9d2282d8af` (use this for allowlisting; line numbers shift)
- **input:** submit the reimbursement form by friday. oh wait, did he ever send the thing over? i can't find it in my email.
- **narrative:** I need to submit the reimbursement form by Friday. Oh wait, did he ever send the thing over? I can't find it in my email.

### line 202 — 0.936 — `time_ambiguous` / hard

- **hash** `7c0c6750c77dd1cb` (use this for allowlisting; line numbers shift)
- **input:** need to pay the property tax bill soon. probably next Friday when I get paid, or maybe the Monday after if the deposit doesn't clear right away. just has to be done before the end of the month so we don't get a penalty.
- **narrative:** I need to pay the property tax bill soon. I will probably do it next Friday when I get paid, or maybe the Monday after if the deposit doesn't clear right away. It just has to be done before the end of the month so we don't get a penalty.

### line 188 — 0.919 — `topic_switching` / medium

- **hash** `70e784aca3b7b102` (use this for allowlisting; line numbers shift)
- **input:** I'll do 20 minutes of scales and then work on the bridge of that jazz piece. after that I should probably look up how to file a tax extension just in case my W2 doesn't arrive.
- **narrative:** I plan to do 20 minutes of scales and then work on the bridge of that jazz piece. After that, I should probably look up how to file a tax extension just in case my W2 doesn't arrive.

### line 339 — 0.912 — `interrupted_thought` / hard

- **hash** `d9e1d3f126d2a509` (use this for allowlisting; line numbers shift)
- **input:** i really want to track down that original pressing of the jazz album, maybe check the local store downtown or I could look on discogs before they-- anyway I need to finish these dishes.
- **narrative:** I really want to track down that original pressing of the jazz album. I could maybe check the local store downtown or look on Discogs before they-- anyway I need to finish these dishes.

### line 465 — 0.909 — `interrupted_thought` / medium

- **hash** `f42e3e3df09802cb` (use this for allowlisting; line numbers shift)
- **input:** the meeting notes from Tuesday said we should review the wireframes before Friday, but didn't Jessica say she was going to— anyway check the shared folder.
- **narrative:** The meeting notes from Tuesday said we should review the wireframes before Friday, but didn't Jessica say she was going to— anyway, I need to check the shared folder.

### line 295 — 0.909 — `multi_person_note` / hard

- **hash** `91407dda0ec0453b` (use this for allowlisting; line numbers shift)
- **input:** We totally nailed the presentation outline! Alex is doing the historical context slides. I need to gather the primary sources tonight. Maria said she will present the conclusion. David is supposed to format the bibliography but I haven't heard from him yet.
- **narrative:** We totally nailed the presentation outline! For next steps, Alex is doing the historical context slides, and I need to gather the primary sources tonight. Maria said she will present the conclusion. David is supposed to format the bibliography, but I haven't heard from him yet.

### line 282 — 0.909 — `long_rambling` / hard

- **hash** `34448ab0d1a8d566` (use this for allowlisting; line numbers shift)
- **input:** Found grandma's old recipe box. It smells like her kitchen. Most of these are written on index cards, I think I should scan them so they don't fade. The date on the pie recipe is 1982. There's a picture of her in here too, I want to get a nice wooden frame for it. Also need to ask mom if she remembers the secret ingredient for the gravy, it just says 'spices'. I miss those Sunday dinners.
- **narrative:** I found grandma's old recipe box, and it smells just like her kitchen. Most of the recipes are written on index cards, and I think I should scan them so they don't fade. I noticed the date on the pie recipe is 1982. There's a picture of her in here too, and I want to get a nice wooden frame for it. I also need to ask mom if she remembers the secret ingredient for the gravy, as it just says 'spices'. I really miss those Sunday dinners.

### line 409 — 0.906 — `multi_person_note` / medium

- **hash** `e5a7cbec78b7c9c3` (use this for allowlisting; line numbers shift)
- **input:** Liam is supposed to draft the opening statement by Wednesday and I have to review the witness list by then maybe Sam can pull the previous case files if he has time
- **narrative:** Liam is supposed to draft the opening statement by Wednesday, and I have to review the witness list by then. Maybe Sam can pull the previous case files if he has time.

### line 333 — 0.905 — `dangling_reference` / hard

- **hash** `57570b26ebded959` (use this for allowlisting; line numbers shift)
- **input:** i think sarah is mad at me about what happened yesterday. probably should text her. honey left his jacket here.
- **narrative:** I think Sarah is mad at me about what happened yesterday, and I probably should text her. Honey left his jacket here.

### line 166 — 0.905 — `interrupted_thought` / easy

- **hash** `ff97c2128eba856d` (use this for allowlisting; line numbers shift)
- **input:** need to pick up milk and bread from the store. also check if they have the good brand of
- **narrative:** I need to pick up milk and bread from the store. I also need to check if they have the good brand of

### line 489 — 0.903 — `multi_person_note` / easy

- **hash** `20718ddf7c2da9e5` (use this for allowlisting; line numbers shift)
- **input:** jessica is drafting the email. i need to pull the analytics for her by noon.
- **narrative:** Jessica is drafting the email, and I need to pull the analytics for her by noon.

### line 335 — 0.900 — `self_correction` / expert

- **hash** `ac98c375b6faa336` (use this for allowlisting; line numbers shift)
- **input:** mark is handling the server migration on tuesday, actually no wait make that wednesday. sarah said she would check the backups, and i probably should email the client. order pizza for the team.
- **narrative:** Mark is handling the server migration on Wednesday. Sarah said she would check the backups, and I probably should email the client. Order pizza for the team.

### line 334 — 0.900 — `dangling_reference` / medium

- **hash** `df27585ea26cdbcd` (use this for allowlisting; line numbers shift)
- **input:** saw that cool thing at the antique store on 4th street maybe i should go back and buy it.
- **narrative:** I saw that cool thing at the antique store on 4th street, and maybe I should go back and buy it.

### line 290 — 0.899 — `dangling_reference` / easy

- **hash** `2141a4d2d3d72d88` (use this for allowlisting; line numbers shift)
- **input:** Reviewing the meeting notes. I really doubt the new timeline is feasible. Need to ask Mark about that specific issue he raised yesterday, I'm not sure what it means for my deliverables.
- **narrative:** I am reviewing the meeting notes and I really doubt the new timeline is feasible. I need to ask Mark about that specific issue he raised yesterday, because I'm not sure what it means for my deliverables.

### line 386 — 0.894 — `zero_action_items` / expert

- **hash** `b73d0cc2bb635cd8` (use this for allowlisting; line numbers shift)
- **input:** I really want to go to the gym later. I always feel better after I lift. But my lower back is feeling weirdly tight today. So maybe I should just rest it. Rest is important for recovery. Although if I don't go I'll feel lazy and I haven't gone since Tuesday. But injuring myself would be worse. I don't know.
- **narrative:** I really want to go to the gym later because I always feel better after I lift, but my lower back is feeling weirdly tight today. So maybe I should just rest it, since rest is important for recovery. Although if I don't go I'll feel lazy, especially since I haven't gone since Tuesday. But injuring myself would be worse. I don't know.

### line 457 — 0.893 — `contradictory_statement` / expert

- **hash** `a8cfbfc88ae7c9cc` (use this for allowlisting; line numbers shift)
- **input:** I should definitely sign up for that pottery class next week or maybe wait until fall because summer is too crazy, although taking it now might be good.
- **narrative:** I should definitely sign up for that pottery class next week, or maybe wait until fall because summer is too crazy. Although, taking it now might be good.

### line 284 — 0.893 — `long_rambling` / hard

- **hash** `d7c59f893e65af7c` (use this for allowlisting; line numbers shift)
- **input:** Three syllabi to read, I'm already behind. History book is out of stock at the bookstore, need to find a PDF online. The dates for the sociology essays are all clustered in November, I should put those in my calendar right now. Physics has a group project, I need to email the TA to see how groups are assigned. Plus office hours are on Thursdays, which conflicts with my shift. Have to talk to my manager about swapping days.
- **narrative:** I have three syllabi to read and I'm already feeling behind. The history book is out of stock at the bookstore, so I need to find a PDF online. The dates for the sociology essays are all clustered in November, which I should put in my calendar right now. Physics has a group project, and I need to email the TA to see how groups are assigned. Plus, office hours are on Thursdays, which conflicts with my shift, so I have to talk to my manager about swapping days.

### line 471 — 0.892 — `zero_action_items` / hard

- **hash** `d1bad3a1d3835fa8` (use this for allowlisting; line numbers shift)
- **input:** The therapist said I should try journaling my dreams but frankly it sounds exhausting to write right after waking up, though maybe it would help with the nightmares, I really don't know if I'll actually do it.
- **narrative:** The therapist said I should try journaling my dreams, but frankly, it sounds exhausting to write right after waking up. Though maybe it would help with the nightmares. I really don't know if I'll actually do it.

### line 488 — 0.889 — `multi_person_note` / easy

- **hash** `38aec1099460c13b` (use this for allowlisting; line numbers shift)
- **input:** i'll vacuum the living room and alex is going to clean the bathrooms.
- **narrative:** I will vacuum the living room and Alex is going to clean the bathrooms.

### line 448 — 0.889 — `time_ambiguous` / expert

- **hash** `6322440322fe615a` (use this for allowlisting; line numbers shift)
- **input:** schedule the vet appointment for Buster for Tuesday morning. or maybe afternoon would be better. actually wait, they might be closed on Tuesdays. I should probably check their hours first before trying to call.
- **narrative:** I wanted to schedule the vet appointment for Buster for Tuesday morning, or maybe the afternoon would be better. Actually, wait, they might be closed on Tuesdays. I should probably check their hours first before trying to call.

### line 389 — 0.889 — `contradictory_statement` / easy

- **hash** `60c1d61fab759d39` (use this for allowlisting; line numbers shift)
- **input:** Going to sell my old tablet online. I haven't turned it on in a year. But what if I need a backup device if my laptop breaks? It's good to have a backup. But it is just gathering dust. I can't decide if I want to get rid of it.
- **narrative:** I am going to sell my old tablet online since I haven't turned it on in a year. But what if I need it as a backup device if my laptop ever breaks? It's good to have a backup. But it is just gathering dust. I can't decide if I want to get rid of it or not.

### line 226 — 0.887 — `voice_to_text_artifact` / expert

- **hash** `d62451bdb93ad62a` (use this for allowlisting; line numbers shift)
- **input:** the landlord is being ridiculous I need to read the least agreement to see what the exact claws is regarding guests. mark said he might have a digital copy I think. text mark to send me his copy if he can find it, unless he deleted it.
- **narrative:** The landlord is being ridiculous, so I need to read the lease agreement to see what the exact clause is regarding guests. Mark said he might have a digital copy, I think. I should text Mark to send me his copy if he can find it, unless he deleted it.

### line 285 — 0.883 — `long_rambling` / hard

- **hash** `80f8128823bae979` (use this for allowlisting; line numbers shift)
- **input:** So excited about the new kitten! Got the litter box set up in the bathroom. The food bowls are ceramic, which is good. Need to buy those feather toys she liked at the shelter. Not sure if I should schedule the vet check for Tuesday or Wednesday, have to look at my work meetings. Also need to look up articles on introducing a kitten to an older dog, Buster is going to be so confused.
- **narrative:** I am so excited about the new kitten! I got the litter box set up in the bathroom, and the ceramic food bowls are ready, which is good. I need to buy those feather toys she liked at the shelter. I am not sure if I should schedule the vet check for Tuesday or Wednesday, so I have to look at my work meetings first. I also need to look up articles on introducing a kitten to an older dog, because Buster is going to be so confused.

### line 299 — 0.883 — `topic_switching` / hard

- **hash** `72457eb19d9057a8` (use this for allowlisting; line numbers shift)
- **input:** Looking at grandpa's old pocket watch on my desk, it always reminds me of the stories he used to tell about the railroad. Such a different era. Oh, the router light is blinking red again. I need to unplug the modem for 30 seconds and reboot the network, this internet dropping is getting ridiculous.
- **narrative:** Looking at grandpa's old pocket watch on my desk always reminds me of the stories he used to tell about the railroad, which was such a different era. Oh, the router light is blinking red again, so I need to unplug the modem for 30 seconds and reboot the network since this internet dropping is getting ridiculous.

### line 462 — 0.880 — `interrupted_thought` / easy

- **hash** `a9a8ae729ff40367` (use this for allowlisting; line numbers shift)
- **input:** remind Mark about the tickets for Saturday and ask him if—
- **narrative:** I need to remind Mark about the tickets for Saturday and ask him if—

### line 236 — 0.880 — `time_ambiguous` / hard

- **hash** `4f5b3aa44ba323df` (use this for allowlisting; line numbers shift)
- **input:** need to pick up the dry cleaning before they close at 6 or maybe 7. I think they changed their hours recently. call them around noon to check. also grab milk on the way back.
- **narrative:** I need to pick up the dry cleaning before they close at 6 or maybe 7, as I think they changed their hours recently. I should call them around noon to check, and also grab milk on the way back.

### line 390 — 0.879 — `long_rambling` / easy

- **hash** `6cbdf84c5ab0ee34` (use this for allowlisting; line numbers shift)
- **input:** Thinking about the concept of time and how it seems to move faster the older I get. When I was a kid summer break felt like an entire lifetime. Now a year goes by in a flash. It's probably because we don't have as many novel experiences as adults. We just do the same routine every day. Work, dinner, sleep. The brain just compresses it all. I should try to break the routine more often.
- **narrative:** I was thinking about the concept of time and how it seems to move faster the older I get. When I was a kid, summer break felt like an entire lifetime, but now a year goes by in a flash. It is probably because we don't have as many novel experiences as adults; we just do the same routine every day of work, dinner, and sleep, and the brain just compresses it all. I should try to break the routine more often.

### line 329 — 0.878 — `topic_switching` / medium

- **hash** `88cd4e66bf16e56b` (use this for allowlisting; line numbers shift)
- **input:** i should probably study French verbs tonight for 20 mins. also need to take the chicken out of the freezer
- **narrative:** I should probably study French verbs tonight for 20 minutes. I also need to take the chicken out of the freezer.

### line 364 — 0.877 — `multi_person_note` / hard

- **hash** `f76083d4a510a019` (use this for allowlisting; line numbers shift)
- **input:** We are trying to figure out the props for the second act and I think we need a vintage lamp but Mark insists we definitely have to use the neon sign from last year's play while Chloe said she would maybe look in her parents basement for an antique chandelier to see if that works better
- **narrative:** We are trying to figure out the props for the second act of the play,. I think we need a vintage lamp, but Mark insists we definitely have to use the neon sign from last year's play. Meanwhile, Chloe said she would maybe look in her parents' basement for an antique chandelier to see if that works better.

### line 407 — 0.875 — `multi_person_note` / easy

- **hash** `4fb0a1917cbdb77c` (use this for allowlisting; line numbers shift)
- **input:** for the escape room on saturday Elise needs to book the tickets online and I should figure out where we are getting dinner beforehand
- **narrative:** For the escape room on Saturday, Elise needs to book the tickets online, and I should figure out where we are getting dinner beforehand.

### line 287 — 0.874 — `interrupted_thought` / hard

- **hash** `b53d33812865df6a` (use this for allowlisting; line numbers shift)
- **input:** Trying to figure out why this Python script keeps throwing a syntax error on line 42. I need to restart my IDE. I checked the indents and they look fine, maybe I missed a parenthesis on the line befo— ah the cat just knocked over my water glass
- **narrative:** I am trying to figure out why this Python script keeps throwing a syntax error on line 42, and I need to restart my IDE. I checked the indents and they look fine, so I was thinking maybe I missed a parenthesis on the line befo— ah, the cat just knocked over my water glass!

### line 235 — 0.873 — `multi_person_note` / expert

- **hash** `e22aae28ffcbd1ed` (use this for allowlisting; line numbers shift)
- **input:** planning the block party for the 12th. I will handle the permit with the city. greg said he can bring his grill and do the burgers. sarah is supposedly organizing the kids games but I should follow up with her to be sure. ask tom if he still has those folding tables.
- **narrative:** I am planning the block party for the 12th and will handle the permit with the city. Greg said he can bring his grill and do the burgers. Sarah is supposedly organizing the kids' games, but I should follow up with her to be sure. I also need to ask Tom if he still has those folding tables.

### line 433 — 0.872 — `repeated_reminder` / expert

- **hash** `8ceea5ffe4c3fd68` (use this for allowlisting; line numbers shift)
- **input:** should probably review the slide deck tonight, or maybe early tomorrow morning before the standup. I really need to go over those slides. tonight might be too late I'll be tired. but don't forget to review the slides at some point, either tonight or morning.
- **narrative:** I should probably review the slide deck tonight, or maybe early tomorrow morning before the standup. I really need to go over those slides. Tonight might be too late because I'll be tired, but I cannot forget to review them at some point, either tonight or in the morning.

### line 272 — 0.872 — `zero_action_items` / easy

- **hash** `1e2fe17ce35e0ee3` (use this for allowlisting; line numbers shift)
- **input:** the protagonist's motivation feels a bit weak in chapter 3. she needs a stronger reason to leave town.
- **narrative:** I think the protagonist's motivation feels a bit weak in chapter 3, and she needs a stronger reason to leave town.

### line 461 — 0.870 — `interrupted_thought` / easy

- **hash** `137af4005bb77a89` (use this for allowlisting; line numbers shift)
- **input:** grab the folder for the meeting and check if the—
- **narrative:** I need to grab the folder for the meeting and check if the—

### line 281 — 0.868 — `long_rambling` / medium

- **hash** `a94a5580453f0025` (use this for allowlisting; line numbers shift)
- **input:** Sorting the attic is so dull. Found three boxes of old clothes from college. Probably should donate them to the shelter downtown. There's a lot of dust up here, might need to get a better mask. Looked through some old notebooks, just scribbles. Saw a dead spider. Need to buy more trash bags before I finish this up. I think I'll just sweep the floor and call it a day soon.
- **narrative:** Sorting the attic is so dull. I found three boxes of old clothes from college that I probably should donate to the shelter downtown. There's a lot of dust up here, so I might need to get a better mask. I looked through some old notebooks that were just scribbles and saw a dead spider. I need to buy more trash bags before I finish this up, but I think I'll just sweep the floor and call it a day soon.

### line 200 — 0.868 — `zero_action_items` / medium

- **hash** `4a05f1d8dba111a4` (use this for allowlisting; line numbers shift)
- **input:** saw the weirdest bird at the feeder today. it had a bright yellow crest but the body of a sparrow. maybe it was a finch? I don't know much about birds. it stayed around for like ten minutes just eating the black oil sunflower seeds and chasing off the squirrels.
- **narrative:** I saw the weirdest bird at the feeder today. It had a bright yellow crest but the body of a sparrow, making me wonder if maybe it was a finch, though I don't know much about birds. It stayed around for about ten minutes, just eating the black oil sunflower seeds and chasing off the squirrels.

### line 338 — 0.865 — `interrupted_thought` / expert

- **hash** `46668ac354c93b90` (use this for allowlisting; line numbers shift)
- **input:** the main character could find a hidden door in the library or maybe she discovers a map inside a book or what if the librarian is a ghost-- oh shoot the timer is going off
- **narrative:** I am brainstorming ideas: the main character could find a hidden door in the library, or maybe she discovers a map inside a book, or what if the librarian is a ghost-- oh shoot the timer is going off.

### line 298 — 0.865 — `time_ambiguous` / medium

- **hash** `26c04e3b8daf0666` (use this for allowlisting; line numbers shift)
- **input:** The kitchen sink is draining so slowly. I have to call the plumber to snake the drain. Maybe I'll call them this afternoon, or I guess tomorrow morning works too since I'll be working from home.
- **narrative:** The kitchen sink is draining so slowly that I have to call the plumber to snake the drain. I am considering calling them this afternoon, or I guess tomorrow morning works too since I'll be working from home.

### line 447 — 0.864 — `multi_person_note` / expert

- **hash** `10e04402efca0691` (use this for allowlisting; line numbers shift)
- **input:** John said we should move the boxes to the basement. Mary thinks we should leave them in the hallway for now. I don't know what to do with the other ones though, the ones from upstairs. maybe someone should just decide.
- **narrative:** John said we should move the boxes to the basement, but Mary thinks we should leave them in the hallway for now. I don't know what to do with the other boxes from upstairs, though. Maybe someone should just decide.

### line 496 — 0.864 — `contradictory_statement` / expert

- **hash** `3f321abf42f3466c` (use this for allowlisting; line numbers shift)
- **input:** david said he paid the internet bill yesterday. check the account because david definitely hasn't paid the internet bill yet.
- **narrative:** David said he paid the internet bill yesterday, but I need to check the account because David definitely hasn't paid the internet bill yet.

### line 346 — 0.864 — `contradictory_statement` / hard

- **hash** `dd7b5b9d1dda8d76` (use this for allowlisting; line numbers shift)
- **input:** the new app update is live for all users. wait the release notes say it only rolled out to beta testers.
- **narrative:** I see the new app update is live for all users, but the release notes say it only rolled out to beta testers.

### line 197 — 0.863 — `dangling_reference` / hard

- **hash** `b651929c4e911924` (use this for allowlisting; line numbers shift)
- **input:** submit the expense report by EOD. make sure to attach the thing they asked for in the all hands meeting. also tell John that his section of the presentation is too long. and find out if we still need to bring that other form to HR.
- **narrative:** I need to submit the expense report by EOD and make sure to attach the thing they asked for in the all hands meeting. I also need to tell John that his section of the presentation is too long, and I need to find out if we still need to bring that other form to HR.

### line 231 — 0.861 — `zero_action_items` / hard

- **hash** `085e231aee792911` (use this for allowlisting; line numbers shift)
- **input:** the cat ate all her dry food today which is a good sign. her energy seems much better than yesterday. dr. evans called with the lab results and everything was normal. feeling very relieved.
- **narrative:** The cat ate all her dry food today, which is a good sign, and her energy seems much better than yesterday. Dr. Evans called with the lab results and everything was normal, so I am feeling very relieved.

### line 365 — 0.861 — `self_correction` / medium

- **hash** `510a00ca3d838012` (use this for allowlisting; line numbers shift)
- **input:** I am definitely free this weekend to help Mark move his couch. I really need to stay home the entire weekend and finish my sociology paper so I have to text Mark that I cannot help him.
- **narrative:** I initially thought I was definitely free this weekend to help Mark move his couch. However, I actually really need to stay home the entire weekend to finish my sociology paper, so I have to text Mark that I cannot help him.

### line 181 — 0.860 — `rapid_branching` / hard

- **hash** `ffdac11711824e66` (use this for allowlisting; line numbers shift)
- **input:** If the bonus comes through we should book the flights, unless prices went up in which case maybe just stay home? If we stay home we need to clear out the guest room. Either way ask Jamie to watch the dog.
- **narrative:** If the bonus comes through we should book the flights, unless prices went up, in which case maybe we just stay home. If we stay home, we need to clear out the guest room. Either way, I need to ask Jamie to watch the dog.

### line 192 — 0.860 — `long_rambling` / expert

- **hash** `1d954778d0d00987` (use this for allowlisting; line numbers shift)
- **input:** so I was looking at the yarn for the cardigan and I realized I probably don't have enough of the blue to finish the sleeves, which is annoying because I bought it on clearance like three years ago. I need to check Ravelry to see if anyone is selling a skein in that dye lot. Or maybe I just make the cuffs a different color? The gray might look okay. I'm so tired of this project honestly I've been knitting it since October. remind me to measure the back panel tomorrow morning before I start the shaping. if the dog hasn't completely tangled the working yarn again.
- **narrative:** While looking at the yarn for my cardigan, I realized I probably don't have enough of the blue to finish the sleeves, which is annoying since I bought it on clearance about three years ago. I need to check Ravelry to see if anyone is selling a skein in that dye lot, or maybe I will just make the cuffs a different color, as the gray might look okay. Honestly, I'm so tired of this project because I've been knitting it since October. I need to measure the back panel tomorrow morning before I start the shaping, assuming the dog hasn't completely tangled the working yarn again.

### line 463 — 0.857 — `interrupted_thought` / easy

- **hash** `42290905cb98eb65` (use this for allowlisting; line numbers shift)
- **input:** I think the dimensions are 4 by 6 but wait let me check the—
- **narrative:** I think the dimensions are 4 by 6, but wait, let me check the—

### line 154 — 0.857 — `dangling_reference` / hard

- **hash** `b22ea34135ac1f82` (use this for allowlisting; line numbers shift)
- **input:** the blue one or maybe Thursday if they still have the wide fitting otherwise just cancel it and use sarah's
- **narrative:** The blue one, or maybe Thursday if they still have the wide fitting — otherwise I'll just cancel it and use Sarah's.

### line 441 — 0.854 — `topic_interleaving` / expert

- **hash** `ad05fb831c86e9b6` (use this for allowlisting; line numbers shift)
- **input:** talked to Mark about renewing the lease for another year, he seems on board. we are almost out of olive oil. Sarah said she might want to move out though. need to get more dish soap too. I should ask Sarah if she's made a firm decision about moving.
- **narrative:** I talked to Mark about renewing the lease for another year, and he seems on board. I noticed we are almost out of olive oil. Sarah, however, said she might want to move out. We also need to get more dish soap. I should ask Sarah if she's made a firm decision about moving.

### line 253 — 0.853 — `multi_person_note` / hard

- **hash** `e5de6cb8e6801601` (use this for allowlisting; line numbers shift)
- **input:** flight leaves at 8am. mark is driving us to the airport. sarah said she will book the hotel in rome but we need to pay her back for half. I need to renew my passport.
- **narrative:** Our flight leaves at 8am, and Mark is driving us to the airport. Sarah said she will book the hotel in Rome, but we need to pay her back for half of it. I also need to renew my passport.
