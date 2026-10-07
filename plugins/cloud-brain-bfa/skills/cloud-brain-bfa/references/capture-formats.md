# Capture formats

The header goes at the top of `text`, above the verbatim source. It exists so the wiki's ingest and any later reader know what the capture is, where it came from, and what was and was not included. Keep it short and factual; the source text below it is never edited.

## Meeting (notes)

```
# 2026-09-08 <you> - BFA management meeting

Meeting: BFA management meeting, next 90-day plan
When: 2026-09-08 09:00 to 11:30 EAT
Participants: <the people in the room, as Granola lists them>
Captured from: Granola, meeting id <id>, on 2026-09-08
Contents: Granola's notes as generated. The transcript is a separate document.

<notes verbatim>
```

`source_id`: `granola:<meeting id>` · `source_type`: `granola` · `source_modified_at`: the meeting's end time.

## Meeting (transcript)

```
# 2026-09-08 <you> - BFA management meeting (transcript)

Meeting: as above
Captured from: Granola, meeting id <id>, on 2026-09-08
Contents: the full transcript as Granola produced it. Speaker labels are Granola's and may be wrong.

<transcript verbatim>
```

`source_id`: `granola:<meeting id>:transcript` · `text_format`: `text` unless the transcript is markdown.

## Email thread

```
# 2026-09-02 <colleague> - Proposals I owe you (thread)

From: <colleague> <…@bfaglobal.com>
To: <you> <…@bfaglobal.com>
Sent: 2026-09-02 08:14 EAT (newest message)
Gmail message id: <id>   thread id: <id>
Captured from: <you>@bfaglobal.com on 2026-09-02
Contents: the whole thread, oldest first, quoted-reply blocks removed where they repeat an earlier message verbatim.

<messages in order, each with its From / Sent line>
```

`source_id`: `gmail:<newest message id>` · `source_type`: `gmail` · `source_modified_at`: the newest message's sent time · `source_url`: the Gmail permalink if the connector gives one.

## Chat channel or direct message

```
# 2026-09-02 BFA Slack DM - <colleague> (Aug 31 - Sep 2)

Workspace: bfa-org.slack.com
Conversation: DM with <colleague> (U…), conversation id D…
Range: 2026-08-31 to 2026-09-02, captured 2026-09-02
Contents: every message in the range, oldest first, Slack's <@U…|Name> and <url|label> markup left as Slack wrote it. Threads read in full are appended at the end.

<messages>
```

`source_id`: `slack:<conversation id>-<newest message ts>` · `source_type`: `slack` · `source_modified_at`: the newest message's time. A group conversation's header lists every participant and user id as the connector gave them.

## Web page or article

```
# 2026-08-04 LLMs reward expertise

Source: https://example.com/post   (author, publication, published 2026-08-04)
Captured: 2026-08-26
Contents: the article's text; navigation, comments and adverts removed.

<article text>
```

`source_id`: `web:example.com/post` · `source_type`: `web` · `source_modified_at`: the publication date · `source_url`: the URL.

## A file or pasted text

```
# 2026-09-10 BFA SME AI survey - draft v0.1

File: BFA SME AI survey - draft v0.1.md, from <you>, 2026-09-10
Contents: the file's text as given.

<text>
```

`source_id`: `file:<filename>` unless the file has a native id (a Drive file id, a document number) · `source_type`: `file`.

## A durable answer kept as a note

```
# 2026-09-18 Note - How BFA's wiki tiers compare

Written by: the assistant, from the wiki, at <you>'s request on 2026-09-18
Draws on: <the pages cited in the answer>

<the answer as given>
```

`source_id`: `note:<yyyy-mm-dd>-<short-slug>` · `source_type`: `note` · personal space unless the user says otherwise.
