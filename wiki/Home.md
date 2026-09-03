# nanorag wiki

**This is not a copy of the docs.** If it were, it would drift, and two sources of truth are worse
than one.

|  | [`docs/`](https://github.com/akash-coded/nanorag/tree/main/docs) | this wiki |
|---|---|---|
| **Changes** | through a pull request, reviewed | directly, by anyone with access |
| **Versioned with the code** | yes — a doc and the code it describes move together | no |
| **In CI** | link checker, markdown lint, mermaid parser | nothing |
| **Published** | [the docs site](https://akash-coded.github.io/nanorag/) | here only |
| **Holds** | decisions, architecture, curriculum, the labs | things that change faster than the code |

So the rule is:

> **If it should still be true in six months and belongs next to a commit, it goes in `docs/`.**
> **If it is a symptom, a gotcha, a note from a session, or something that will be edited five
> times this month, it goes here.**

## Pages

| | |
|---|---|
| **[Common Errors](Common-Errors)** | Literal error strings → what caused them → the fix. Search this first |
| **[Troubleshooting](Troubleshooting)** | Symptom → cause → fix, for things that produce no error at all |
| **[Environment Setup](Environment-Setup)** | Per-platform gotchas — macOS, Linux, WSL, Colab, devcontainer |
| **[Glossary](Glossary)** | Every term used across the repo. Edit freely |
| **[Arena FAQ](Arena-FAQ)** | The first ten minutes of the L.A.B. simulator, answered |
| **[Session Runbook](Session-Runbook)** | Assign, run, read the board — for whoever runs a cohort |
| **[Office Hours Log](Office-Hours-Log)** | Running notes from sessions |
| **[Interview Field Reports](Interview-Field-Reports)** | What people were actually asked, with a template |
| **[Wiki Conventions](Wiki-Conventions)** | How to edit, and what does **not** belong here |

## If you are new

Start in the repository, not here:

1. [`docs/00-orientation/start-here.md`](https://github.com/akash-coded/nanorag/blob/main/docs/00-orientation/start-here.md) — ten minutes
2. [The L.A.B. simulator](https://github.com/akash-coded/nanorag/blob/main/docs/80-lab/README.md) — twelve auto-graded labs
3. [Discussions](https://github.com/akash-coded/nanorag/discussions) — 88 threads, and [a map of them](https://github.com/akash-coded/nanorag/blob/main/docs/50-community/discussion-map.md)

Come back here when something breaks.

## The most useful thing you can add

**An error string nobody has written down yet.** [Common Errors](Common-Errors) is searchable, and
the value of a page like that is entirely in its coverage. If you hit something, spent twenty
minutes on it, and solved it — that twenty minutes belongs here.
