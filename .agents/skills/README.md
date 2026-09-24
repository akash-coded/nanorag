# Agent skills

Skills that any coding agent working in this repository can load. They follow the
[Agent Skills](https://agentskills.io) layout: one folder per skill, each with a `SKILL.md` whose
frontmatter carries `name` and `description`.

This folder is the only copy. Each agent finds it like this:

| Agent | Reads skills from | How |
|---|---|---|
| Codex (CLI, IDE, app) | `.agents/skills/` | native repo-level location |
| Claude Code | `.claude/skills/` | symlink to `../.agents/skills` |
| Any other agent | `.agents/skills/` | [AGENTS.md](../../AGENTS.md) lists each skill and says when to open it |

Add or change a skill here, never under `.claude/skills/`.

## What is installed

All four are third-party skills, copied unchanged on 24 Sep 2026. Read them as advice. Where a
skill disagrees with the user, with [AGENTS.md](../../AGENTS.md) or with
[CONTRIBUTING.md](../../CONTRIBUTING.md), the skill loses.

| Skill | Use it for | Upstream | Licence |
|---|---|---|---|
| `frontend-anti-slop` | building or restyling any page, artifact or diagram page; picking fonts, palettes, motion; auditing a page for generic AI patterns | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) and [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), packaged with a local `scripts/lookup.py` | MIT |
| `humanizer` | removing AI writing tells from English prose: docs, READMEs, PR bodies, discussion replies | [blader/humanizer](https://github.com/blader/humanizer) v3.0.0 | MIT |
| `humanizer-zh` | the same job for Chinese text | [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh), revision 2026-09-23 | MIT |
| `edit-article` | restructuring a long document section by section | [amazingloft999-droid/mattpocock-skills](https://github.com/amazingloft999-droid/mattpocock-skills), a mirror of Matt Pocock's skills | MIT |

## What was in the download and left out

The source bundle `third-party-skills-2026-09-24.zip` had more files than this folder does.
The rest were left out on purpose:

- `taste/*-SKILL.md` and `uiux/*.csv` are the same text and data already inside
  `frontend-anti-slop` (only the provenance headers differ). A second copy would give two
  skills that trigger on the same prompts.
- `humanizer-SKILL.md` and `uiux/SKILL.md` contain only `404: Not Found`. The download failed.
- `taste-tree.json` is a GitHub API rate-limit error, not data.
- `search-*.json` are raw GitHub search results, and `*-README.md` are upstream READMEs and an
  index of other skills. Both are reference material, not skills.

## Updating a skill

1. Replace the skill's folder with the new upstream version.
2. Read the whole diff before committing. These files become instructions an agent follows.
3. Update the table above: upstream, revision, licence.
4. Run `make check`. markdownlint skips third-party files under `.agents/skills/*/`, but the
   link checker and the mermaid validator still read them.
