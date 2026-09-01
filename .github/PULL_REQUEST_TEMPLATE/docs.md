<!-- For documentation-only changes. Open with ?template=docs.md -->

## What this changes

Closes #

## Type

- [ ] Correcting something that is wrong
- [ ] Adding something missing
- [ ] Restructuring — moving or splitting
- [ ] A new decision record (ADR)

## If you are correcting something

**What did it say, and what is wrong with it?**

<!-- If a number was wrong, say how you found out. Reproducing a documented number and finding it
     does not match is the highest-value contribution here. -->

## If this is an ADR

- [ ] It names the alternative that lost
- [ ] It has a **What would change this** section with a falsifier that could actually be checked

## Checklist

- [ ] `python tools/check_links.py` → `broken: 0`
- [ ] `node tools/validate-mermaid.mjs` passes, if diagrams changed
- [ ] `npx markdownlint-cli2 "**/*.md"` clean
- [ ] Links to GitHub routes (`/discussions`, `/issues`) are **absolute** — relative ones resolve
      differently from `docs/` than from the root
