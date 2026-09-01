# Q18 · What would block a retrieval-model release in your evaluation pipeline?


Two hard blocks and two warnings.

**Hard block** if any frozen-slice metric drops beyond its tolerance — the frozen slice is the
one thing tuning never saw, so a drop there is real. **Hard block** if a previously-passing
regression case now fails; those cases exist because someone was hurt by that failure once.

**Warn** if cost per query rises more than about 15%, and **warn** if any single tenant or
slice drops while the average holds — that second one is the case where someone experiences a
6% average improvement as a total outage of their use case.

Two things I would add. A delta inside the noise band is not a result: I measure run-to-run and
sampling variance once, write it down, and compare every delta against it. And the override
path matters as much as the gate — a human can ship past a block, and that decision is logged
with their name on it. A gate nobody can override gets disabled; a gate with a silent override
is theatre.

---
