# Codex Skill To Full App Plugin

This repository is a Codex plugin marketplace that distributes the `skill-to-full-app` plugin.

## Install

After this repository is pushed to GitHub:

```bash
codex plugin marketplace add keithhchen/codex-skill-to-full-app
codex plugin marketplace upgrade keithhchen-codex-plugins
codex plugin add skill-to-full-app@keithhchen-codex-plugins
```

Then start a new Codex thread and invoke:

```text
Use $skill-to-full-app to turn this Skill into a real AI-native app.
```

## Repository Layout

```text
.agents/plugins/marketplace.json
plugins/skill-to-full-app/.codex-plugin/plugin.json
plugins/skill-to-full-app/skills/skill-to-full-app/SKILL.md
```

## Update

After changing plugin files:

```bash
git add .
git commit -m "Update skill-to-full-app plugin"
git push
codex plugin marketplace upgrade keithhchen-codex-plugins
codex plugin add skill-to-full-app@keithhchen-codex-plugins
```

Use a new Codex thread after reinstalling so updated skills are loaded.
