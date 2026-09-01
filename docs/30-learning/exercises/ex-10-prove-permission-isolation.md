# EX-10 · Prove permission isolation

> **Difficulty:** 🔴 · label [`difficulty: 3`](https://github.com/akash-coded/nanorag/labels/difficulty:%203)
> **Submit:** open a thread in [Solutions & Peer Review](https://github.com/akash-coded/nanorag/discussions) with your numbers, or a PR linking to it.

**Notebook 03** · ~1 h · *Skill: interview Q4's "prove it" bullet*

Extend `assert_persona_isolation` into a property-based test that runs over the whole eval set
and every persona, and wire it into CI.

**Acceptance criteria**

- The test, passing, in `tests/`
- A deliberately broken configuration that the test **catches** (demonstrate the failure)
- The k-collapse measurement for the broken configuration
- A one-paragraph note on what the test does *not* cover (caches, traces, result counts)

---
