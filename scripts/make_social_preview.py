#!/usr/bin/env python3
"""Generate the repository's social preview card.

Drawn rather than downloaded: an original image has no licensing question attached
to it, and matplotlib is already this repository's diagram tool for the reason in
ADR-0006 — a figure that is generated from code can be regenerated when the numbers
change, and a stock image cannot.

The curve on the right is real. It is the ANN recall collapse from issue #2: a pure
k-NN graph with no long-range links, where greedy search cannot escape the local
basin, against the same graph with Kleinberg long-range links added. Both series are
the measured numbers, not an illustration.

GitHub renders the social preview at 1280x640 and crops toward the centre, so the
composition keeps its content inside a safe margin.

    python scripts/make_social_preview.py        # -> assets/social-preview.png
"""
from __future__ import annotations

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# The palette is the repo's own — the same values the mermaid classDefs use.
INK_BG    = "#0F1417"
PANEL     = "#161D21"
AMBER     = "#E9A83C"
TEAL      = "#4FBFAE"
RUST      = "#E58A66"
TEXT      = "#F2F5F3"
MUTED     = "#8C9B95"
RULE      = "#26312F"

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "social-preview.png"

# Measured in notebook 04 §4.6 — recall@20 against exhaustive search.
EF          = [8, 16, 32, 64, 128, 256, 512]
KNN_ONLY    = [0.00, 0.00, 0.00, 0.00, 0.12, 0.31, 0.55]
WITH_LONG   = [0.71, 0.88, 0.95, 0.98, 1.00, 1.00, 1.00]


def main() -> None:
    fig = plt.figure(figsize=(12.8, 6.4), dpi=100)
    fig.patch.set_facecolor(INK_BG)

    # ── left: the wordmark and the claim ──────────────────────────────────
    fig.text(0.055, 0.775, "nanorag", color=TEXT, fontsize=76,
             fontweight="bold", va="center", family="DejaVu Sans")
    fig.text(0.058, 0.645,
             "The whole retrieval stack. Nothing installed.",
             color=AMBER, fontsize=20, va="center")

    fig.text(0.058, 0.545,
             "BM25 · dense · ANN · fusion · reranking · evaluation",
             color=TEXT, fontsize=15.5, va="center")
    fig.text(0.058, 0.482,
             "No vector database. No framework. No API key.",
             color=MUTED, fontsize=15.5, va="center")

    # rule
    fig.add_artist(plt.Line2D([0.058, 0.44], [0.40, 0.40],
                              color=RULE, linewidth=1.4))

    facts = [
        ("10", "notebooks"),
        ("22", "exercises"),
        ("47", "discussions"),
        ("15", "CI gates"),
    ]
    for i, (n, label) in enumerate(facts):
        x = 0.058 + i * 0.098
        fig.text(x, 0.305, n, color=TEAL, fontsize=27, fontweight="bold", va="center")
        fig.text(x, 0.222, label, color=MUTED, fontsize=12.5, va="center")

    fig.text(0.058, 0.105,
             "It runs in memory, in about ten seconds.",
             color=MUTED, fontsize=14, va="center", style="italic")

    # ── right: a real measurement ─────────────────────────────────────────
    # The panel lives on its own invisible axes rather than in fig.patches:
    # figure-level patches are drawn after the axes, so a fig.patches panel
    # paints over the plot no matter what zorder it is given.
    bg = fig.add_axes([0.0, 0.0, 1.0, 1.0], zorder=0)
    bg.set_axis_off()
    bg.patch.set_alpha(0)
    bg.add_patch(FancyBboxPatch(
        (0.548, 0.135), 0.390, 0.73,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=PANEL, edgecolor=RULE, linewidth=1.4))
    bg.set_xlim(0, 1); bg.set_ylim(0, 1)

    ax = fig.add_axes([0.628, 0.300, 0.264, 0.385], zorder=2)
    ax.set_facecolor(PANEL)
    ax.plot(EF, WITH_LONG, color=TEAL, linewidth=2.8, marker="o",
            markersize=5, label="+ long-range links")
    ax.plot(EF, KNN_ONLY, color=RUST, linewidth=2.8, marker="o",
            markersize=5, label="pure k-NN graph")
    ax.set_xscale("log", base=2)
    ax.set_xticks(EF)
    ax.set_xticklabels([str(e) for e in EF], fontsize=9.5)
    ax.set_ylim(-0.07, 1.16)
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_yticklabels(["0", "0.5", "1.0"], fontsize=9.5)
    ax.set_xlabel("ef  ·  search visit budget", color=MUTED, fontsize=10.5, labelpad=6)
    ax.set_ylabel("recall@20", color=MUTED, fontsize=10.5, labelpad=6)
    ax.tick_params(colors=MUTED, length=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color(RULE)
    ax.grid(axis="y", color=RULE, linewidth=0.9)
    ax.set_axisbelow(True)
    # The rust series occupies the lower right and the teal the upper right, so
    # the legend goes mid-left, which is the only region both curves leave clear.
    leg = ax.legend(loc="center left", bbox_to_anchor=(0.015, 0.46),
                    frameon=False, fontsize=10, labelcolor=TEXT, handlelength=1.5)
    for t in leg.get_texts():
        t.set_color(TEXT)

    fig.text(0.5875, 0.805, "A finding you can watch happen",
             color=TEXT, fontsize=14.5, fontweight="bold", va="center")
    fig.text(0.5875, 0.752,
             "ANN recall collapses when the graph is not navigable · issue #2",
             color=MUTED, fontsize=10, va="center")
    fig.text(0.5875, 0.185,
             "Every number in this repository has a cell that reproduces it.",
             color=MUTED, fontsize=10.5, va="center", style="italic")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor=INK_BG, dpi=100)
    size_kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.relative_to(OUT.parent.parent)}  ({size_kb:.0f} KB, 1280x640)")


if __name__ == "__main__":
    main()
