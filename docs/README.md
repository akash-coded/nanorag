# Documentation

Seven groups, numbered in reading order. Nothing here is longer than it needs to be; if a
document grows past about 250 lines it gets split.

| I want to… | Start here |
|---|---|
| understand what this is in ten minutes | [`00-orientation/start-here.md`](00-orientation/start-here.md) |
| follow the material in order | [`00-orientation/curriculum.md`](00-orientation/curriculum.md) |
| change code in `nanorag/` | [`10-architecture/overview.md`](10-architecture/overview.md) |
| know **why** something is the way it is | [`20-decisions/`](20-decisions/) |
| practise | [`30-learning/exercises/`](30-learning/exercises/) |
| prepare for an interview | [`30-learning/interview-prep/`](30-learning/interview-prep/) |
| read the papers behind it | [`30-learning/reading-list.md`](30-learning/reading-list.md) |
| run, release or operate this | [`40-operations/runbook.md`](40-operations/runbook.md) |
| take part in Discussions | [`50-community/discussions-guide.md`](50-community/discussions-guide.md) |
| find a thread that already answered this | [`50-community/discussion-map.md`](50-community/discussion-map.md) |
| **hit an error and want the fix** | [the wiki](https://github.com/akash-coded/nanorag/wiki/Common-Errors) |
| **carry one page into a meeting** | [`60-cheatsheets/`](60-cheatsheets/) |
| **practise, one lab at a time** | [`80-lab/`](80-lab/) — the L.A.B. simulator |
| see what is being built next | [`70-extension/`](70-extension/) |
| understand the casebook threads | [`50-community/casebook-convention.md`](50-community/casebook-convention.md) |
| look up notation or a term | [`90-reference/notation.md`](90-reference/notation.md) |
| see what has already been answered | [`90-reference/faq.md`](90-reference/faq.md) |

---

## The groups

| Group | Contains | Audience |
|---|---|---|
| [`00-orientation/`](00-orientation/) | Start here, curriculum, putting this on a CV | Anyone arriving |
| [`10-architecture/`](10-architecture/) | HLD, the seams, the diagrams | Anyone changing the toolkit |
| [`20-decisions/`](20-decisions/) | Architecture decision records, with the alternative that lost | Reviewers, interviewers |
| [`30-learning/`](30-learning/) | 22 exercises, 18 interview questions, the reading list | Students |
| [`40-operations/`](40-operations/) | Runbook, release process, board, GitHub setup | Maintainers |
| [`50-community/`](50-community/) | How Discussions work here, and the casebook convention | Contributors |
| [`60-cheatsheets/`](60-cheatsheets/) | Frameworks, playbooks, interview sheets — one page each | Learners and practitioners |
| [`70-extension/`](70-extension/) | The follow-on project: does any of this transfer to a real corpus? | Contributors, anyone assessing the work |
| [`80-lab/`](80-lab/) | The L.A.B. simulator — 12 auto-graded labs on a prerequisite DAG | Learners of every level |
| [`90-reference/`](90-reference/) | Notation, glossary | Everyone, occasionally |

---

## Docs, or wiki?

|  | `docs/` (here) | [the wiki](https://github.com/akash-coded/nanorag/wiki) |
|---|---|---|
| **Changes** | through a reviewed pull request | directly, by anyone with access |
| **Versioned with the code** | yes | no |
| **In CI** | links, markdown, mermaid all checked | nothing |
| **Holds** | decisions, architecture, curriculum, labs | error strings, platform gotchas, session notes, the glossary |

**The test:** if being wrong for a month would mislead somebody making a decision, it belongs here
where a reviewer sees it. If it is a symptom or a gotcha that will be edited five times this
month, it belongs in the wiki.
