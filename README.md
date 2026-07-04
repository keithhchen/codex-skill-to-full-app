# Codex Skill To Full App Plugin

This repository is a Codex plugin marketplace that distributes the `skill-to-full-app` plugin.

## Install From Another Computer

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

## Use

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
plugins/skill-to-full-app/.codex-plugin/plugin.json
plugins/skill-to-full-app/skills/skill-to-full-app/SKILL.md
```

## Upgrade

When this repository changes, users can pull the latest marketplace snapshot and reinstall:

```bash
codex plugin marketplace upgrade keithhchen-codex-plugins
codex plugin add skill-to-full-app@keithhchen-codex-plugins
```

Use a new Codex thread after reinstalling so updated skills are loaded.

## Troubleshooting

Check that Codex sees the marketplace:

```bash
codex plugin marketplace list
```

Check installed plugins:

```bash
codex plugin list
```

If the plugin does not appear after install, restart Codex and open a new thread.
