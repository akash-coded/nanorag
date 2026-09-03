# Wiki mirror

The **live wiki** at <https://github.com/akash-coded/nanorag/wiki> is the canonical copy. It is
what readers see and what maintainers edit in the GitHub UI. This folder is a read-only mirror,
kept so the pages show up in code search, in pull-request diffs and in offline clones.

- Edit pages on the wiki, not here. An edit made here does not reach the wiki.
- After editing the wiki, refresh the mirror with `make wiki-pull` and commit the result.
- The mirror is deliberately not pushed to the wiki by a workflow: a push-direction sync would
  silently overwrite edits made in the wiki UI.
- The mirror is exempt from markdownlint on purpose, being a verbatim copy. Fix style on the wiki.
