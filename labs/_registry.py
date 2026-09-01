"""Discovers labs and enforces that the pathway is a valid DAG.

A pathway whose prerequisites contain a cycle is not a pathway, and one that
lists a prerequisite that does not exist silently strands a lab where nobody
reaches it. Both are easy to introduce by hand and neither is visible in review,
so they are checked here and in CI.
"""
from __future__ import annotations

import dataclasses
import json
import pathlib

LABS_DIR = pathlib.Path(__file__).resolve().parent

DIFFICULTY = {"easy": "🟢", "medium": "🟡", "hard": "🔴", "boss": "⚫"}

TRACKS = {
    "T1": "Corpus & Chunking",
    "T2": "Indexing & Retrieval",
    "T3": "Ranking & Packing",
    "T4": "Measurement",
    "T5": "Judgement",
    "T6": "Economics",
    "T7": "Agents & Traces",
    "T8": "Shipping",
}

# Each track's capstone produces the artefact that stage of a product cycle
# actually hands to the next stage. The mapping is the point: you do not learn
# the lifecycle by reading about it, you learn it by being made to produce its
# outputs in the order they are needed.
PDLC = {
    "T1": ("Discovery", "a corpus spec: what is in scope, what the retrievable unit is"),
    "T2": ("Design", "an ADR: the retrieval design, and the alternative that lost"),
    "T3": ("Development", "an implementation with a measurement attached"),
    "T4": ("Testing", "an eval set and the noise band that makes it interpretable"),
    "T5": ("Quality", "a quality gate somebody else can run without you"),
    "T6": ("Viability", "a cost model whose inputs are named"),
    "T7": ("Operations", "a trace that makes a failure reproducible after the fact"),
    "T8": ("Release", "a decision record: ship, do not ship, or not yet measurable"),
}


@dataclasses.dataclass
class Lab:
    id: str
    slug: str
    title: str
    track: str
    difficulty: str
    minutes: int
    prereqs: list[str]
    tags: list[str]
    concept: str
    path: pathlib.Path

    @property
    def badge(self) -> str:
        return DIFFICULTY.get(self.difficulty, "🟡")

    @property
    def dirname(self) -> str:
        return self.path.name


def load() -> dict[str, Lab]:
    labs: dict[str, Lab] = {}
    for meta_path in sorted(LABS_DIR.glob("L*/meta.json")):
        raw = json.loads(meta_path.read_text(encoding="utf-8"))
        lab = Lab(
            id=raw["id"], slug=raw["slug"], title=raw["title"], track=raw["track"],
            difficulty=raw["difficulty"], minutes=raw["minutes"],
            prereqs=raw.get("prereqs", []), tags=raw.get("tags", []),
            concept=raw.get("concept", ""), path=meta_path.parent,
        )
        labs[lab.id] = lab
    return labs


def validate(labs: dict[str, Lab]) -> list[str]:
    """Returns a list of problems. Empty means the pathway is sound."""
    problems: list[str] = []
    for lab in labs.values():
        if lab.track not in TRACKS:
            problems.append(f"{lab.id}: unknown track {lab.track!r}")
        if lab.difficulty not in DIFFICULTY:
            problems.append(f"{lab.id}: unknown difficulty {lab.difficulty!r}")
        for prereq in lab.prereqs:
            if prereq not in labs:
                problems.append(f"{lab.id}: prerequisite {prereq} does not exist")

    # Cycle detection over the prerequisite graph.
    WHITE, GREY, BLACK = 0, 1, 2
    colour = dict.fromkeys(labs, WHITE)

    def visit(node: str, stack: list[str]) -> None:
        colour[node] = GREY
        for parent in labs[node].prereqs:
            if parent not in labs:
                continue
            if colour[parent] == GREY:
                cycle = " -> ".join(stack[stack.index(parent):] + [parent])
                problems.append(f"prerequisite cycle: {cycle}")
            elif colour[parent] == WHITE:
                visit(parent, stack + [parent])
        colour[node] = BLACK

    for node in labs:
        if colour[node] == WHITE:
            visit(node, [node])
    return problems


def unlocked(labs: dict[str, Lab], done: set[str]) -> list[Lab]:
    """Labs whose prerequisites are all satisfied and which are not yet done."""
    return [lab for lab in labs.values()
            if lab.id not in done and all(p in done for p in lab.prereqs)]
