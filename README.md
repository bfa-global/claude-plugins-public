# BFA Claude plugins

BFA Global's public plugin marketplace for Claude. It is for people who work with BFA on their own
Claude plan, such as contractors. BFA staff don't need it: BFA's Claude workspace already gives them
the same plugins.

| Plugin | What it does |
|---|---|
| [`cloud-brain-bfa`](plugins/cloud-brain-bfa/) (BFA Brain) | The BFA wiki's connector plus the skill that tells Claude how to use it |

A plugin here holds instructions and a connector address, nothing else. The services a plugin
connects to keep their own sign-in, and BFA decides who can use them. Installing a plugin gives you
no access on its own.

## Add the marketplace

**In claude.ai or the Claude desktop app** (Pro or Max plan):

1. Go to **Customize > Plugins**.
2. Select **Add > Add marketplace** and enter `bfa-global/claude-plugins-public`.
3. Find the plugin you need and select **Add**.

A plugin you add there is saved to your Claude account, so it also appears in Cowork and in Claude
Code when you are signed in with the same account. If you use Claude through another company's Team
or Enterprise workspace, its Owner may not allow adding marketplaces; ask them, or use a personal
account.

**In Claude Code only:**

```
/plugin marketplace add bfa-global/claude-plugins-public
/plugin install cloud-brain-bfa@bfa-global-plugins
```

Each plugin's README says what else it needs, such as connecting its connector.

## Updates

Plugins update from this repository's `main` branch. In claude.ai, select **Check for updates** on
the marketplace, or turn on **Sync automatically**. In Claude Code, run
`/plugin marketplace update bfa-global-plugins`.

## For maintainers

This repository is public. Before you merge anything, check that it contains:

- **Nothing confidential**: no client names, project details, internal figures, people's contact
  details or examples taken from real BFA material.
- **No secrets**: no tokens, keys or passwords. Everyone who installs a plugin receives all its files.
- **Nothing proprietary** that BFA would not publish.

Git history is public too, so a secret committed and then removed is still exposed. Rotate it.

BFA's own Claude workspace syncs a separate, private marketplace (`bfa-global/claude-plugins`),
because workspace sync refuses a public repository. That marketplace takes its plugins from this
one, so a plugin is written once, here. A change merged here reaches BFA staff after a workspace
Owner selects **Re-sync** on that marketplace, or after the next push to it.

Rules for every plugin:

- List it by a relative path (`./plugins/<name>`) in `marketplace.json`, and keep the entry `name`
  equal to the plugin's own `name`.
- Never change a plugin's `name` once released. Change `displayName` instead.
- Raise `version` in `plugin.json` on every change.
- No top-level `bin/` directory. claude.ai rejects a plugin that has one.

Check the catalogue and every plugin before you push:

```bash
claude plugin validate .
claude plugin validate ./plugins/<name>
```

### Updating `cloud-brain-bfa`

The skill's source is `skills/cloud-brain-bfa/` in cloud-brain. Copy it from that repo's `release`
branch, which is the version deployed at `cloud-brain.bfaglobal.com`, so the skill never describes
a tool the server doesn't have yet. Then raise the plugin's `version` and open a pull request.
