# Wiki seed

The ten pages in this directory are the **initial content** for
[the wiki](https://github.com/akash-coded/nanorag/wiki).

## Why they are here and not only there

GitHub creates a wiki's git repository **only after the first page is created through the web
UI**. Turning the Wiki feature on is not enough — `has_wiki: true` with no pages means
`nanorag.wiki.git` does not exist, and there is no REST or GraphQL API for wiki content
(`hasWikiEnabled` is read-only). So the content could not be pushed until somebody clicked once.

Keeping the seed here means it is versioned, reviewable, and not lost in the meantime.

## Seeding it

One manual step, then one command:

1. Open <https://github.com/akash-coded/nanorag/wiki> and **create any page** — the title and body
   do not matter. The script overwrites GitHub's placeholder text and deletes any throwaway page
   whose only job was to create the repository.
2. Then:

```bash
python scripts/sync_wiki.py
```

**Already done.** The wiki was seeded on 1 September 2026 and is live at
<https://github.com/akash-coded/nanorag/wiki>. This directory is kept as the recoverable origin,
not as a mirror — see below.

## After that, the wiki is authoritative

This directory is a **one-time seed, not a mirror.** The whole point of a wiki is that anyone can
fix a wrong error message without opening a pull request, and a two-way sync would take that away.

Once seeded, edit the wiki directly. `sync_wiki.py` refuses to run a second time unless you pass
`--force`, precisely so it cannot silently overwrite somebody's edit.

## What belongs in the wiki rather than in `docs/`

Short version: things that change faster than the code and do not need review — error strings,
platform gotchas, session notes, a glossary anyone can fix. The full rule is in
[Wiki-Conventions.md](Wiki-Conventions.md).
