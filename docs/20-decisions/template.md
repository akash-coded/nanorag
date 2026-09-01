# ADR-NNNN: <short imperative title>

- **Status:** Proposed | Accepted | Superseded by ADR-NNNN
- **Date:** YYYY-MM-DD
- **Deciders:** <who>

## Context

What forced a decision. Include the constraint that made it non-obvious — if there was no
constraint, this does not need an ADR.

## Options considered

### Option A — <name>

What it is. What it costs.

### Option B — <name>

What it is. What it costs.

## Decision

What we chose, in one sentence.

## Consequences

**Good:** what this buys.

**Bad:** what it costs — state this even when it is uncomfortable, especially then.

**Revisit when:** the condition under which this decision should be reopened.

## What would change this

The observation that would make this decision wrong. Name a measurement, a threshold, or a
constraint that could actually be checked — not "if requirements change".

A decision without a falsifier is a preference. This section is what makes an ADR reviewable
by someone who was not in the room, and it is the first thing an interviewer reads.

> **Example, from ADR-0003 (LSA as the default encoder):** *"If a sentence-transformer model
> can be loaded offline in under 3 seconds on a cold machine with no network, the argument for
> LSA collapses — its only advantage is that it has no download."*
