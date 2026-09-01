# Wiki conventions

## What belongs here

Things that **change faster than the code** and do not need review:

- An error string and its fix
- A platform gotcha
- Notes from a session
- A term somebody had to look up
- A field report

## What does not

| Belongs in `docs/` instead | Why |
|---|---|
| Architecture, decisions, ADRs | Must be versioned **with the code they describe** |
| The curriculum, exercises, labs | Referenced by CI and by `scripts/lab.py`; a broken link fails a build |
| Anything published on [the docs site](https://akash-coded.github.io/nanorag/) | The site builds from `docs/`, not from here |
| Anything with a measurement that gates a decision | Numbers that matter get a PR and a reviewer |

**The test:** if being wrong here for a month would mislead somebody making a decision, it belongs
in `docs/` where a reviewer sees it.

## What does not belong anywhere public

- Client corpora, real user queries, internal metrics
- Anything under NDA
- Credentials, tokens, endpoints

The wiki is public and its history is permanent.

## Editing

Edit directly. No PR, no review, no CI. That is the point.

**Conventions worth keeping:**

- **Add, do not rewrite.** If an entry is wrong, correct it and say what changed rather than
  deleting the old text — somebody searched those words once
- **Error strings verbatim.** Do not paraphrase a message. People search for the exact text
- **Date session notes.** [Office Hours Log](Office-Hours-Log) is chronological and useless without
  dates
- **Link into the repo, not out of it.** A wiki page that duplicates a doc will drift; link instead

## Page naming

Wiki links use the filename with hyphens. `Common-Errors.md` is linked as `[Common Errors](Common-Errors)`.

Keep names short and noun-shaped. `Troubleshooting`, not `How-To-Troubleshoot-Problems`.

## If a page grows past about 200 lines

Split it, or move it to `docs/`. A long wiki page is usually a doc that has not admitted it yet —
and once something is long enough to need a table of contents, it is long enough to want a
reviewer.
