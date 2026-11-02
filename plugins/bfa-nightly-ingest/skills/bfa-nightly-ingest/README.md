# BFA nightly ingest

A Claude skill that captures your day into your personal BFA Brain wiki while you sleep. It runs
from a scheduled task on claude.ai around midnight, so your computer can be off.

It answers one question for the wiki: **what has happened since the last capture that it has not seen yet?**

## What it captures

| Source | What it takes |
| --- | --- |
| Meetings | Notes and transcript from Granola, Zoom, Google Meet or Gemini notes, or the recap email Fireflies, Otter, Fathom or Read.ai sends |
| Email | Threads you took part in on your BFA account |
| Slack | Your DMs and group DMs, and threads you posted in or were mentioned in |

Each night it looks at the last 14 days, takes the last 36 hours first, then fills any older
gap, at most 15 documents a night. A busy stretch is caught up over a few nights; nothing in
the 14 days is lost. Older history is not part of the nightly run.

It leaves out newsletters, notifications, receipts, meeting reminders and "thanks". A meeting
whose notes are still processing is picked up the next night.

Everything goes to your **personal** wiki. Nothing goes to the shared BFA wiki; adding to that is
a choice you make yourself, in a conversation.

## What it does not do

It never sends, posts, replies or drafts anything, and it writes no pages itself. It hands the
source text to BFA Brain, and the wiki's own ingest writes the pages.

## Confidential material

By default it captures confidential items too (candor about a colleague, a contractor matter, an
unannounced deal, your own personal matters), marked confidential so the wiki keeps them off
other pages. Your personal wiki is yours alone, and leaving them out leaves gaps in your own
record.

To keep them out instead, add one sentence to the task's instruction (see below). They are then
listed by title in the report and nothing is submitted.

## Setting it up

1. In claude.ai, connect **BFA Brain**, **Gmail**, **Slack**, **Google Calendar**, and your
   notes tool (Granola, Zoom, or Google Drive if you use Meet notes).
2. Create a scheduled task, daily at **00:07** your time. Daily, because weekend mail is still
   mail; weekdays only is fine if you prefer.
3. Give it this instruction:

   > Run the bfa-nightly-ingest skill for my account. Capture everything since the last
   > capture (meetings, mail and Slack) into my personal BFA Brain wiki. Nobody is watching: do
   > not ask questions, and if a connector is missing, say so in the report and carry on.

   Optional: *Hold confidential items back and list them in the report.* If the first run
   reports `personal space not found`, add *My wiki space is `<id>`.*
4. Press **Run now** once and read the report.

Each person sets up their own task. Tasks belong to one account and are not shared.

## The report

Every run ends with a short report in the task's history: what it captured, what it looked past
and why, the pages the wiki created or edited, and anything that went wrong. The first line says
`ok`, `partial` or `failed`. Check it when something you expected is missing from the wiki.

**If the status says the wiki is out of credits**, nothing more was submitted that night. Tell
the BFA wiki's operator.

**If a connector shows as off**, it was not signed in for the scheduled run. Open claude.ai's
connectors and sign in again.
