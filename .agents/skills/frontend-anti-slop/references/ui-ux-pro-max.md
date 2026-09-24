# UI UX Pro Max (data tables and checklist)

Provenance: nextlevelbuilder/ui-ux-pro-max-skill on GitHub, MIT licence, fetched 24 Sep 2026. The repository's SKILL.md returned a 404 at fetch time, so what is bundled here is the README (curated) plus four of its data tables. The README sections on installation, the CLI, sponsors, the premium tier and troubleshooting are not reproduced because they do not apply inside this package. Every quoted block below is verbatim from the README.

## What is bundled and what is not

| Table | Rows | What each row gives | In this package |
|---|---|---|---|
| `data/typography.csv` | 74 | a named font pairing, category, heading and body font, mood keywords, best-for list, Google Fonts URL, CSS import, Tailwind config, notes | yes |
| `data/colors.csv` | 192 | one palette per product type: primary, secondary, accent, background, foreground, card, muted, border, destructive, ring, each with its on-colour, plus a note on the mood | yes |
| `data/motion.csv` | 17 | a motion pattern with intensity tier, trigger, duration, easing, a GSAP snippet, framework notes, a do, a don't, and performance notes | yes |
| `data/ux-guidelines.csv` | 119 | a UX rule with category, platform, severity, a do, a don't, and good and bad code examples | yes |
| styles.csv (79 UI styles), landing patterns (34), product-type reasoning rules (192), chart types (25), stack guidelines (22), the BM25 search scripts | not fetched | the parts of the upstream reasoning engine that produce the "design system" output | no |

So this package can answer "which fonts, which palette, which motion spec, which UX rules" for a brief. It cannot run the upstream design-system generator. Where a style name or landing pattern is needed, use Section 10 of `taste-skill.md` instead.

## How to query the tables

Run `scripts/lookup.py` rather than reading a CSV into context; the colour table alone is 38 KB.

```
python3 scripts/lookup.py typography luxury editorial
python3 scripts/lookup.py colors fintech --full
python3 scripts/lookup.py motion "scroll reveal"
python3 scripts/lookup.py ux form validation --platform Web
python3 scripts/lookup.py ux --category Accessibility --top 30
python3 scripts/lookup.py colors --list-categories
```

Scoring is a keyword count with the name column weighted, so two or three brief-specific words work better than a sentence. `--full` prints the long columns (CSS imports, GSAP snippets, code examples).

## The upstream workflow, as described in the README

### How Design System Generation Works

```
┌─────────────────────────────────────────────────────────────────┐
│  1. USER REQUEST                                                │
│     "Build a landing page for my beauty spa"                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. MULTI-DOMAIN SEARCH (5 parallel searches)                   │
│     • Product type matching (192 categories)                    │
│     • Style recommendations (79 searchable; 50 active)          │
│     • Color palette selection (192 palettes)                    │
│     • Landing page patterns (34 patterns)                       │
│     • Typography pairing (74 font combinations)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. REASONING ENGINE                                            │
│     • Match product → UI category rules                         │
│     • Apply style priorities (BM25 ranking)                     │
│     • Filter anti-patterns for industry                         │
│     • Process decision rules (JSON conditions)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. COMPLETE DESIGN SYSTEM OUTPUT                               │
│     Pattern + Style + Colors + Typography + Effects             │
│     + Anti-patterns to avoid + Pre-delivery checklist           │
└─────────────────────────────────────────────────────────────────┘
```

The intent to keep from that diagram: a brief is decomposed into product type, style, palette, pattern and typography before any code is written, and anti-patterns for the industry are filtered out at the same stage. With only four tables bundled, do the product-type and style reasoning yourself using `taste-skill.md` Sections 0 to 2, then pull palette, typography, motion and UX rules from the tables.

### 192 Industry-Specific Reasoning Rules

The reasoning engine includes specialized rules for:

| Category | Examples |
|----------|----------|
| **Tech & SaaS** | SaaS, Micro SaaS, B2B Service, Developer Tool / IDE, AI/Chatbot Platform, Cybersecurity Platform |
| **Finance** | Fintech/Crypto, Banking, Insurance, Personal Finance Tracker, Invoice & Billing Tool |
| **Healthcare** | Medical Clinic, Pharmacy, Dental, Veterinary, Mental Health, Medication Reminder |
| **E-commerce** | General, Luxury, Marketplace (P2P), Subscription Box, Food Delivery |
| **Services** | Beauty/Spa, Restaurant, Hotel, Legal, Home Services, Booking & Appointment |
| **Creative** | Portfolio, Agency, Photography, Gaming, Music Streaming, Photo/Video Editor |
| **Lifestyle** | Habit Tracker, Recipe & Cooking, Meditation, Weather, Diary, Mood Tracker |
| **Emerging Tech** | Web3/NFT, Spatial Computing, Quantum Computing, Autonomous Drone Fleet |

Each rule includes:
- **Recommended Pattern** - Landing page structure
- **Style Priority** - Best matching UI styles
- **Color Mood** - Industry-appropriate palettes
- **Typography Mood** - Font personality matching
- **Key Effects** - Animations and interactions
- **Anti-Patterns** - What NOT to do (e.g., "AI purple/pink gradients" for banking)

## Pre-delivery checklist (verbatim, from the README's sample output)

- [ ] No emojis as icons (use SVG: Heroicons/Lucide)
- [ ] cursor-pointer on all clickable elements
- [ ] Interaction timing follows the platform, component, and user preference
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] prefers-reduced-motion respected
- [ ] Text, chips, and badges reflow without clipping or broken labels
- [ ] Responsive: 375px, 768px, 1024px, 1440px

### Resilient Text and Compact UI

The guidance now covers common production failures around headings, long tokens,
chips, badges, and interrupted micro-interactions:

- Balanced heading wrapping is a progressive enhancement, not a guarantee that a
  specific word will remain on the last line. Designs must still work with natural
  wrapping across widths, fonts, and locales.
- Essential text must reflow without clipping at narrow widths, browser zoom, text
  scaling, and user spacing overrides. Long URLs and identifiers may wrap safely.
- Chip and tag collections should wrap or use an operable `+n` disclosure. A compact
  label should remain whole when practical; unavoidable truncation needs an accessible
  full-value path for keyboard, pointer, and touch users.
- Badge meaning cannot rely on color alone. Interactive chips need native semantics,
  visible focus, and programmatic state; live counts need meaningful context.
- Rapid interactions may cancel animation, but the final semantic state, focus, and
  content must remain correct. Timing is selected for the platform and component,
  with reduced-motion preferences respected.

## Features

- **79 Searchable UI Styles (50 active)** - Glassmorphism, Claymorphism, Minimalism, Brutalism, Neumorphism, Bento Grid, Dark Mode, AI-Native UI, and more
- **192 Color Palettes** - Industry-specific palettes aligned 1:1 with the 192 product types
- **74 Font Pairings** - Curated typography combinations with Google Fonts imports
- **25 Chart Types** - Recommendations for dashboards and analytics
- **22 Tech Stacks** - React, Next.js, Astro, Vue, Nuxt.js, Nuxt UI, Svelte, SwiftUI, React Native, Flutter, HTML+Tailwind, shadcn/ui, Jetpack Compose, Angular, Laravel, Three.js, JavaFX, WPF, WinUI 3, UWP, Avalonia, Uno Platform
- **119 UX Guidelines** - Best practices, anti-patterns, accessibility rules, resilient text layout, compact labels, and cancellable interactions
- **192 Reasoning Rules** - Industry-specific design system generation (NEW in v2.0)
