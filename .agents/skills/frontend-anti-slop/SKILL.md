---
name: frontend-anti-slop
description: Third-party anti-slop rules and data tables for premium front-end work, packaged for reference. Contains Leonxlnx's taste-skill (brief read, three dials, AI-tell list, redesign protocol, pre-flight check) with its minimalist and redesign variants, and ui-ux-pro-max's tables of 74 font pairings, 192 colour palettes, 17 motion specs and 119 UX rules with a lookup script. Use whenever building or restyling a landing page, portfolio, marketing site, learning companion, single-file HTML page, published artifact or app screen; whenever choosing a font pairing, palette, motion timing or hover and scroll animation; whenever auditing an existing page for generic AI patterns; and whenever a draft has been rejected as templated, bland, childish or slop. Read it even when the user only says make it look premium, less generic, or more polished.
license: MIT
---

# Frontend anti-slop reference pack

This skill packages other people's front-end rules so they can be read on demand instead of re-fetched. The rules are advice, not authority: where a reference conflicts with the user's stated preferences or with a house skill the user already runs (for example a skill that fixes fonts, chrome icons or the illustration grammar), the user's rule wins and the reference is used only for what the house rule does not cover. None of the bundled text was edited beyond removing frontmatter and adding a provenance line.

## What is in the pack

| File | Source | What it is for | Read it when |
|---|---|---|---|
| `references/taste-skill.md` | Leonxlnx/taste-skill, design-taste-frontend v2 | the main protocol: infer the brief, set three dials (variance, motion, density), map the brief to a design system or an aesthetic, the AI-tell list, the pattern vocabulary, dark mode, performance guardrails and a pre-flight check | any new page, or any page whose look is being decided from scratch |
| `references/minimalist-ui.md` | Leonxlnx/taste-skill, minimalist-ui | a narrower protocol for editorial and workspace-style interfaces: warm monochrome, typographic contrast, flat bento grids, no gradients | the brief says minimal, editorial, document-like, Notion-like, calm |
| `references/redesign-existing.md` | Leonxlnx/taste-skill, redesign-existing-projects | scan, diagnose, fix in place: an audit of typography, colour, layout, states, content, icons and code quality, with a fix priority | a page or codebase already exists and must be made premium without a rewrite |
| `references/ui-ux-pro-max.md` | nextlevelbuilder/ui-ux-pro-max-skill README | what the four data tables contain, how to query them, the pre-delivery checklist and the resilient-text rules | before running the lookup script for the first time in a session |
| `data/typography.csv`, `data/colors.csv`, `data/motion.csv`, `data/ux-guidelines.csv` | nextlevelbuilder/ui-ux-pro-max-skill | 74 font pairings with Google Fonts imports, 192 palettes keyed by product type, 17 motion specs with GSAP snippets, 119 UX rules with good and bad code | never read whole; query them with the script |
| `scripts/lookup.py` | original, written for this pack | keyword search over the four tables, printing only the matching rows | whenever a font, palette, motion timing or UX rule is needed |

## Workflow

Follow this order for a new page. Each step names the exact place to read.

1. Read the brief before touching code. Section 0 of `taste-skill.md` lists the signals to read (page kind, vibe words, references, audience, existing brand assets, quiet constraints) and asks for a one-line design read before generating. Write that line.
2. Set the three dials from Section 1 of `taste-skill.md`, using the use-case presets table. State the three numbers so the user can override them.
3. Decide whether a real design system applies (Section 2 of `taste-skill.md`). If the brief names an enterprise system, install the official package; if it names an aesthetic, build it honestly with native CSS and say so. If the brief reads as editorial or minimal, switch to `minimalist-ui.md` from here on.
4. Pull the data. Run `python3 scripts/lookup.py` for typography, colours, motion and UX with two or three words from the brief. Take the Google Fonts import and the palette tokens from the results rather than inventing them.
5. Build against the directives in Section 4 of `taste-skill.md` (typography, colour calibration, layout diversification, states, hard layout rules, image strategy, content density, theme lock) and the guardrails in Section 6 (reduced motion, dark mode, web vitals, DOM cost).
6. Before delivering, run the pre-flight check in Section 14 of `taste-skill.md`, then the eight-item pre-delivery checklist in `ui-ux-pro-max.md`. Section 9 of `taste-skill.md` is the AI-tell list; scan the page against it once more at the end, since those are the patterns reviewers reject first.

For an existing page, start with `redesign-existing.md` instead: scan, diagnose against its audit, then fix by its priority order, and use the data tables at the fix step for replacement fonts and palettes.

## Fast path for the common asks

| The user asks for | Read | Run |
|---|---|---|
| a font pairing, or a font was rejected | `taste-skill.md` Section 4.1 | `lookup.py typography` with the mood words |
| a palette for a product type | nothing first | `lookup.py colors` with the product type, add `--full` for the token set |
| hover, scroll-reveal, stagger or page-transition timing | nothing first | `lookup.py motion` with the interaction name |
| an accessibility or UX audit of a page | `redesign-existing.md` audit | `lookup.py ux --category Accessibility --top 30` |
| "why does this look like AI made it" | `taste-skill.md` Section 9 and Section 0.D | nothing |
| a minimalist or editorial page | `minimalist-ui.md` | `lookup.py typography serif editorial` |

## Known gaps

State these honestly rather than working around them silently.

- `taste-skill.md` Section 12 describes a library of implemented blocks that lives in the upstream repository. It is not bundled, so the pattern names in Section 10 are the usable vocabulary and any block must be written from scratch.
- ui-ux-pro-max upstream has more tables than the four bundled here (79 UI styles, 34 landing patterns, 192 product-type reasoning rules, 25 chart types, 22 stack guides) and a BM25 search engine. None of those were fetched. This pack therefore cannot generate the upstream "design system" printout; do the style and pattern reasoning with `taste-skill.md` and pull only fonts, colours, motion and UX rules from the tables.
- The dial numbers, use-case presets, AI-tell list and fix priorities are the authors' own constructions, not published standards. Present them as one practitioner's rules when the user asks where a rule came from.
