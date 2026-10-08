---
name: cloud-brain-bfa
description: >-
  Work with the user's BFA wiki (BFA Brain, the cloud-brain deployment for BFA Global) over MCP
  (the `wiki_*` tools): answer questions from what the wiki already knows, and capture new sources
  into it so the wiki's own ingest can write the pages. Use this whenever the user asks what the
  wiki or "the brain" knows about something, wants a meeting, email thread, document, article or
  conversation remembered or "added to the wiki", asks what they have missed lately, wants to
  update or remove something they submitted, or mentions the wiki, ingest, submit, a source id, or
  a job id, even when they do not name the tools.
metadata:
  version: "1.4.2"
---

# The BFA wiki

This is version 1.4.2 of the BFA wiki skill. When the user asks which version of the skill they have, tell them this number.

The wiki is a knowledge base that the wiki's ingest writes and a person steers. You are the person's hands: you decide what is worth keeping, you hand the source text over, and you answer questions from what is there. The wiki's own ingest, running on the server, reads every source you submit and writes or revises the pages. You never write a page. What the wiki ends up saying about a source is the pipeline's decision, the same as for any other source it has taken in. That split is what keeps every claim traceable to a source and every page consistent with the ones around it.

Eight MCP tools carry the whole relationship. Four read: `wiki_search`, `wiki_index`, `wiki_read_page`, `ping`. Four write, all of them about sources rather than pages: `wiki_submit`, `wiki_job_status`, `wiki_documents`, `wiki_remove_document`. Their own descriptions are precise about arguments and refusals; this skill is about judgment, which is the part a tool description cannot carry: when to look, what to keep, how to hand it over, and what to say afterwards.

One fact shapes everything below: **the server only ever sees the text you send it.** It has no access to the user's mail, meetings, chats, drives or files, it cannot follow a link, and it cannot open a binary. Capturing a source means putting its text into `wiki_submit`.

## Orientation

Before the first read or write in a session, learn the lie of the land once:

- `wiki_documents()` with no arguments lists every wiki (a "space") the user may submit to, and what this identity has already submitted. The `spaces` list is where the `space` value for a submission comes from.
- `wiki_index()` shows what pages exist. If more than one space is readable, sections are headed `# Space: <name>`.

Everyone at BFA has a personal wiki, and there is one shared BFA wiki that members of staff can read and write. They are different spaces, one submission goes to exactly one of them, and the same source in both is two independent documents. **The personal wiki is always the default.** Submit to the BFA wiki only when the user names it: it is where the organisation's knowledge is meant to accumulate, and it is read by colleagues, so what goes there is a deliberate choice, never a default.

## Answering from the wiki

Treat the wiki as the first place to look for anything that could have been captured before: a person, an organisation, a decision, a number, a meeting. Look before you speculate.

- For a factual or keyword-shaped question, call `wiki_search(query, include_content=True)`. The top hits come with their full page text, so most questions are answered in one call. Read the `space` field on each hit rather than assuming which wiki it came from. Search with the words a page would use (names, nouns, the source's own terms) rather than the user's whole question: a page must contain every word to match, and only when none does are pages with some of the words returned. If a search finds nothing, try again with fewer or different words before concluding the wiki is silent.
- Pages are written in the wiki's own language, and a page made from a source in another language keeps the source's key terms and names beside their translation (for example `fishers (pescadores)`). When the user asks in a different language from the wiki's, search in both: once with the words the wiki's pages use and once with the user's or the source's own words, because a search matches words exactly.
- For a browse-shaped question ("what do we have on X", "what is in the reference section"), call `wiki_index()`, pick the paths, then `wiki_read_page` with all of them in one list call.
- When you need one known page, `wiki_read_page(path)`; a bare page name works when it is unique, the full path when it is not.

Cite what you used: name the page (its path) and the space when there is more than one. Quote rather than paraphrase where the wording matters. When the wiki contradicts itself, say so and name both pages; when it is silent, say that too, and then look elsewhere. Silence from the wiki, once a search with fewer words has also come back empty, is information: it may mean the source was never captured, which is a prompt to offer capturing it.

Answers can compound. When an answer you have just given is plainly worth keeping (a comparison, an analysis, a connection nobody had drawn), offer once to keep it: submitting the answer text itself as a source with `source_type="note"` lets the ingest file it as a page, so the next question finds it instead of redoing the work. Only submit it if the user agrees, and never submit chat as a matter of course.

## Capturing sources

This is the half that makes the wiki worth having, and the half where judgment matters most.

### What counts as a source

Bring something forward when it carries at least one of:

- a decision, a policy, a commitment, or a stated default
- a number attached to something real (time saved, a price, a headcount, a date)
- a deliverable or a document the user will refer back to
- a person, organisation, product or place the wiki does not yet know
- a claim that contradicts a page the wiki already has
- an introduction, or a change in a relationship

Leave out logistics: meeting reminders, calendar invites, "thanks", "recording uploaded", newsletters, receipts, notifications, and anything automated or bulk. A long backlog means the bar was set too low, not that the week was busy.

### Discuss before submitting

The default is to present before you file. Show what you propose to capture, one line each, grouped by where it came from, and ask which to take. Submitting is not free: each source costs the account an ingest run on its own credential, and the wiki is easier to keep clean than to clean up. Skip the discussion only when the user asks for batch mode, and say what you submitted when you are done.

Never submit something the user has not asked to keep. A submission leaves their machine and lands in a wiki that, in the shared case, other people read.

### How to hand a source over

Give the wiki the source itself, not your summary of it: `text` is always the verbatim source, never a paraphrase, because the wiki's value rests on being checkable. Keep the wording, the names, the numbers and the dates as the source has them. Prepend a short header that says what the capture is (`references/capture-formats.md` has the header for each kind of source), then the verbatim text. Do not pass `distillation`: BFA wikis run on the plan-direct engine, which reads `text` in full.

Because the server needs the text itself, convert first: a document becomes its text, a thread becomes its messages in order, a meeting becomes its notes and its transcript. A PDF, spreadsheet, image or scan can only be captured if you can extract its text faithfully; if you cannot, say so rather than submitting a description of it.

Then call `wiki_submit` with:

- `space`: the wiki it belongs in (the personal one unless the user says otherwise).
- `title`: a human-readable title, dated where the source has a date: `2026-09-08 Alex - Quarterly planning meeting`, `2026-09-02 Sam - Proposal timeline (thread)`.
- `text`: the header plus the verbatim source, markdown or plain text, at most 256 KiB. `text_format="text"` for a raw transcript with no markup.
- `source_id`: the source's own stable id, always, when it has one. The shape is `<type>:<native id>`: `gmail:<message id>`, `granola:<meeting id>`, `gdrive:<file id>`, `slack:<channel id>-<thread ts>`, `web:<canonical url without scheme>`. This id is the document's identity for good. Submit the same id again with changed text and the wiki produces a new version of the same document; submit it with identical text and nothing happens. That is what makes re-capturing on a schedule safe. Leave it out only for text with no native identity, and then know that a changed version is a new document unless you name the old one in `replaces`. Never invent a `sha256:` id; that label is the server's.
- `source_url`: a link back to the original when there is one.
- `source_type`: a lowercase label for the channel: `gmail`, `granola`, `gdrive`, `slack`, `web`, `note`, `file`. Lowercase letters, digits and hyphens only.
- `source_modified_at`: the source's own last-modified time in ISO 8601 when the channel reports one (a meeting's end, a message's sent time, a document's modified time). It is recorded as your claim and never verified, and it is what a later sweep compares against.
- `note`: a one-line hint for the ingest when context helps it file well, for example who the people are, which project this belongs to, or that a transcript's speaker labels are unreliable.
- `related_pages`: page names from `wiki_search` or `wiki_index` in this same wiki that the source likely touches, only ones that already exist. The wiki's ingest treats the list as a suggestion of where to look first, not a fact, and still looks across the wiki itself.
- `confidential`: set `true` when the title or text names something that must not spread to other pages (a codename, an unannounced deal). The wiki then names the source's own page by its date and kind of source (for example `2026-10-01 meeting`) instead of the title, and other pages cite it only by that name. It does not hide the source's text or title from anyone who can read the document record. The flag covers one submission only, the server does not carry it over, and `wiki_documents` does not show it: whenever you resubmit a document that was submitted as confidential (a new version under the same `source_id`, a refresh during a sweep, or a `replaces` submission), pass `confidential=true` again. If you cannot tell whether it was, decide as for a new source.

The call returns at once with a `job_id` and an `outcome`. `already_current` means this exact text is already in the wiki: nothing was queued, and that is success. `duplicate` means a different document already holds byte-identical content: nothing was queued; resubmit with `allow_duplicate=True` only if the user really wants two documents.

### Following the job

Ingest takes a minute or more per source. Call `wiki_job_status(job_id)` after a capture, or when the user asks. `done` comes with `created_pages` and `edited_pages`: report those paths, because they are what the user will want to read. `failed` comes with `error`: report it plainly and do not resubmit in a loop.

A new account may have no Anthropic credential set yet. Then a submission is recorded but no pages are written until the key is set; setting it queues an ingest for everything recorded in the meantime, so nothing is lost and there is no need to hold submissions back. The account's owner sets the key on the wiki's console under "Anthropic key" (BFA staff sign in to the console with their Google account); tell the user that once, and carry on capturing. If they do not know where the key comes from, the BFA wiki's operator does.

### Meetings

A meeting arrives as notes and a transcript. Submit them as two documents so each has its own identity: the notes under `granola:<meeting id>` and the transcript under `granola:<meeting id>:transcript`, both with the meeting's end time as `source_modified_at`. Never soften or trim what the transcript says; quote it verbatim or leave it out. A `note` naming the participants helps the ingest attach the right entities.

### Email

One thread is one document under the thread's newest message id, with From, To, Sent and the message and thread ids in the header, and the messages in order. BFA mail lives on `@bfaglobal.com` Google Workspace accounts, which is where the Gmail connector reads. Newsletters and notifications are not sources. The assistant's own mailbox, if it has one, is never a source.

### Documents and files

Text the user pastes or uploads is a source under `file:<filename>`, or a better native id if the document has one (a Drive file id, a document number). Send the document's text, not a link to it.

### Web pages and chat

An article is a source under `web:<canonical url>` with its publication date as `source_modified_at` and the URL as `source_url`. BFA's Slack workspace (`bfa-org.slack.com`) is captured verbatim, one document per channel-and-range or per thread, with the workspace, channel, id and range in the header, and Slack's own markup left as it is. Most channel traffic is logistics and not a source; a channel earns a capture when someone shows what they built, states a decision or a default, closes an action the wiki still has open, or contradicts a page. Private direct messages are where confidential material lives: a candid remark about a named colleague or client given to the user in confidence goes to the personal wiki with the header saying it was said in confidence, and never into the BFA wiki. That governs where it goes and how it is written up, not whether it can be read.

## Sweeps: "what have I missed?"

The server does not poll sources and will not remind anyone. When the user asks what is waiting, or on a cadence they set, sweep:

1. Call `wiki_documents()` and, per `source_type`, note the newest `source_modified_at`. That is the watermark for that channel.
2. Enumerate each channel the user's connectors reach (meetings, mail, chat) from its watermark to now, and drop anything whose source id is already listed.
3. Apply the bar above. Present the backlog grouped by channel, one line each, and say how many items you looked past.
4. Submit what the user picks, then report the job ids and, when they finish, the pages.

A channel with nothing captured yet has no watermark; that is how a new channel starts, not an error. If a connector is missing, say so in one line and sweep the rest.

Sweeps also find stale documents. A document whose stated `source_modified_at` is older than the live source (the file was edited, the thread got a reply) is resubmitted under the same `source_id` with the new text (with `confidential=true` again if it was submitted as confidential); the wiki makes a new version and retires the old pages. Identical text costs nothing, so resubmitting everything a channel has is a safe way to refresh.

## Updating, replacing, removing

- Same source, new content: resubmit under the same `source_id`, with `confidential=true` again if the earlier version had it. Nothing else to do.
- A source that moved (the notes were a shared doc and are now a file elsewhere): submit the new one with `replaces=<old source id>` (again with `confidential=true` if the old one had it); the old document is retired and the two are linked.
- Removal: `wiki_remove_document(space, source_id, confirm=True)` queues a removal that deletes the pages the document created and strips its claims from pages it edited. Only a document this identity submitted can be removed; write access lets anyone update anything, but not delete what others added. Removing someone else's document is an administrator's action. Call `wiki_documents` first to see what is removable, confirm with the user before passing `confirm=True`, and follow the job.

Worth knowing before it surprises anyone: a person's Google sign-in and their API token are different principals to the server. A document submitted under one cannot be listed or removed under the other, even by the same human.

## Limits and refusals

- Text only, 256 KiB per submission. Split a longer text into parts with their own ids (`...:part-2`) only when the parts stand alone.
- Every `related_pages` name must already exist as a page in the target wiki, or the whole call is refused before anything is written -- pass only names `wiki_search` or `wiki_index` actually reported.
- The account may hold fifty queued submissions at a time. A refusal naming that bound means wait for jobs to finish, not resubmit.
- Refusals name what was wrong (a malformed source id, an over-long note, a space this identity cannot write). Fix the input; do not retry the same call.
- An unknown job id and a job in a wiki this identity cannot read give the same answer. That is by design, not a bug to work around.

## Reporting

After a capture session, report what was submitted and where, one line per document: title, source id, space, job id, and once known the pages created or edited. After a sweep, also say what was looked past and why. After answering from the wiki, the citations are the report.

Keep it short. The wiki is meant to reduce what the user has to hold in their head, and a long report does the opposite.
