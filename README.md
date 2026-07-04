# Codex Skill To Full App Plugin

This repository is a Codex plugin marketplace that distributes the `skill-to-full-app` plugin.

It also includes a Claude Code plugin marketplace for the same skill.

## Install In Codex

Prerequisites:

- Codex installed and signed in.
- Network access to GitHub.

Run:

```bash
codex plugin marketplace add keithhchen/codex-skill-to-full-app --ref main
codex plugin marketplace upgrade keithhchen-codex-plugins
codex plugin add skill-to-full-app@keithhchen-codex-plugins
```

Then start a new Codex thread so the plugin skill is loaded.

## Install In Claude Code

Prerequisites:

- Claude Code installed and authenticated.
- Claude Code version with `/plugin` support.
- Network access to GitHub.

From the Claude Code terminal:

```bash
claude plugin marketplace add keithhchen/codex-skill-to-full-app
claude plugin install skill-to-full-app@keithhchen-claude-plugins
```

Or inside an interactive Claude Code session:

```text
/plugin marketplace add keithhchen/codex-skill-to-full-app
/plugin install skill-to-full-app@keithhchen-claude-plugins
/reload-plugins
```

Claude Code plugin skills are namespaced by plugin name. Invoke this skill as:

```text
/skill-to-full-app:skill-to-full-app
```

## Use In Codex

```text
Use $skill-to-full-app to turn this Skill into a real AI-native app.
```

Example prompts:

```text
Use $skill-to-full-app to convert this SKILL.md into a production app plan.
```

```text
Use $skill-to-full-app to turn this SOP into an AI-native workflow app with tools, state, evals, and review.
```

## Repository Layout

```text
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
plugins/skill-to-full-app/.codex-plugin/plugin.json
plugins/skill-to-full-app/.claude-plugin/plugin.json
plugins/skill-to-full-app/skills/skill-to-full-app/SKILL.md
```

## Upgrade

When this repository changes, users can pull the latest marketplace snapshot and reinstall:

```bash
codex plugin marketplace upgrade keithhchen-codex-plugins
codex plugin add skill-to-full-app@keithhchen-codex-plugins
```

Claude Code users can update with:

```bash
claude plugin marketplace update keithhchen-claude-plugins
claude plugin update skill-to-full-app@keithhchen-claude-plugins
```

Use a new Codex thread or run `/reload-plugins` in Claude Code after reinstalling so updated skills are loaded.

## Troubleshooting

Check that Codex sees the marketplace:

```bash
codex plugin marketplace list
```

Check installed plugins:

```bash
codex plugin list
```

Check that Claude Code sees the marketplace:

```bash
claude plugin marketplace list
claude plugin list
```

If the plugin does not appear after install, restart Codex and open a new thread.
