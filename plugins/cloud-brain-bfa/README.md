# BFA Brain (`cloud-brain-bfa`)

Connects Claude to the BFA wiki and tells it how to use it. Ask Claude what the wiki knows about a
project, a partner or a decision, or ask it to add a meeting, an email thread, a document or a
conversation to the wiki. The wiki's own ingest reads what you add and writes the pages.

The plugin holds two things:

- **The connector** to `https://cloud-brain.bfaglobal.com/mcp`, the BFA deployment of cloud-brain.
- **The `cloud-brain-bfa` skill**, which tells Claude when to look things up, what is worth adding
  and how to hand it over.

Installing the plugin does not sign you in or give you access. BFA decides who can use the wiki.

## Connect it with a BFA Google account

If you have an `@bfaglobal.com` Google account, connect once, after the plugin appears under
**Customize > Plugins**:

1. Open **BFA Brain** and go to its **Connectors** tab.
2. Select **Connect** and sign in with your `@bfaglobal.com` Google account.

The sign-in lasts up to 7 days; after that Claude asks you to reconnect, which re-checks that you
are still in BFA's Google Workspace.

## Connect it with a personal token (contractors)

If you work with BFA but have no `@bfaglobal.com` Google account, the Google sign-in will refuse
you. BFA gives you a personal token instead. Keep it to yourself: the wiki treats anyone who holds it
as you. BFA turns it off when your work with BFA ends.

Don't use the plugin's **Connectors** tab. Add the connector yourself, with the token.

**In claude.ai or the Claude desktop app:**

1. Go to **Customize > Connectors** and select **Add custom connector**.
2. Name it `BFA Brain` and enter the URL `https://cloud-brain.bfaglobal.com/mcp`.
3. For **Authentication**, choose **No sign-in**.
4. Under **Request headers**, choose `authorization` and enter `Bearer ` followed by your token,
   with the space.
5. Select **Add**.

**Request headers** is a beta feature that not every Claude account has yet. If the dialog doesn't
show it, you can still use the wiki from Claude Code, below, and tell your BFA contact.

**In Claude Code:**

```bash
claude mcp add --transport http cloud-brain-bfa https://cloud-brain.bfaglobal.com/mcp \
  --header "Authorization: Bearer <your token>"
```

The plugin's Connectors tab will keep showing its own connector as not added. That is expected:
the skill works with the connector you added.

## If you had the skill before

If you installed the `cloud-brain-bfa` skill by hand before, remove that copy under
**Customize > Skills**, so Claude does not see the skill twice.

## What it sends

Claude sends the wiki the text of what you ask it to add, and your questions when it searches. The
wiki keeps what you add on BFA's cloud-brain deployment. Nothing is sent anywhere else by this
plugin.
