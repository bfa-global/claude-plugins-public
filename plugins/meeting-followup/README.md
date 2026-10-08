# Meeting follow-up (`meeting-followup`)

Turns a meeting that has just happened into the follow-up that goes out afterwards. Ask "write up
the call" or "send the follow-up for my 2pm", and Claude reads the meeting's notes itself and gives
you what was agreed, with an owner and a date on every item, the questions nobody answered, and a
drafted follow-up email or Slack message.

## What it needs

Connect these under **Customize > Connectors**, with your own accounts:

- **Google Calendar**, to find the meeting.
- Meeting notes from **Granola**, **Zoom**, or Google Meet notes saved in **Google Drive**.
- **Gmail**, for recap emails others already sent, and to save a draft if you ask for one.

If no notes can be found, Claude says so rather than inventing what was agreed.

## What it does with your data

It reads the accounts you connected. Its only write is a Gmail draft, and only when you ask for one.
Nothing is sent: you review the draft and send it yourself.
