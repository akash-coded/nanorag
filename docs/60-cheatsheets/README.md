# Cheat sheets

Compressed, printable, opinionated. Each page is one page: a framework you can hold in your
head, a checklist you can run under pressure, or a decision you can defend in a review.

**These are not summaries of the notebooks.** They are the shapes that were left over after the
measurements were done — the things worth carrying to a corpus that is nothing like this one.

## Frameworks — mental models

Named so you can reach for them mid-conversation.

| | Framework | The question it answers |
|---|---|---|
| 🧭 | [The Four Verdicts](frameworks/four-verdicts.md) | *Where did this answer actually fail?* |
| 🔬 | [The Precondition Test](frameworks/precondition-test.md) | *Should I adopt this technique at all?* |
| 📏 | [The Noise Band Ladder](frameworks/noise-band-ladder.md) | *Is this delta real?* |
| 📶 | [The Stage Gradient](frameworks/stage-gradient.md) | *Which stage is the bottleneck now?* |
| 🧊 | [The Cost Iceberg](frameworks/cost-iceberg.md) | *What does this system actually cost?* |
| 🔒 | [The Inference Channel Audit](frameworks/inference-channel-audit.md) | *Can someone learn what they cannot read?* |
| ⚖️ | [The Calibration Triangle](frameworks/calibration-triangle.md) | *Can I trust this judge?* |
| 🪞 | [The Reranker Mirror](frameworks/reranker-mirror.md) | *Will this second stage add anything?* |

## Playbooks — run these under pressure

| | Playbook | When |
|---|---|---|
| 🚨 | [Retrieval incident runbook](playbooks/retrieval-incident-runbook.md) | Quality dropped and nobody knows why |
| 📅 | [First 30 days on a RAG engagement](playbooks/first-30-days.md) | You have just been handed a client and a promise |
| 🧾 | [Design review checklist](playbooks/design-review-checklist.md) | Someone is about to present an architecture |
| 🚦 | [Release gate playbook](playbooks/release-gate-playbook.md) | Deciding whether a change ships |
| 🔄 | [Encoder migration playbook](playbooks/encoder-migration.md) | Swapping the embedding model without an outage |

## Interviews

| | Sheet | Use it |
|---|---|---|
| 🗺️ | [Navigating the loop](interviews/navigating-the-loop.md) | Before the day — what each round is scoring |
| 🔍 | [The question decoder](interviews/question-decoder.md) | What they are *actually* asking |
| 🚩 | [Red flags you emit without noticing](interviews/red-flags.md) | The sentences that cost you the round |
| 📐 | [Numbers worth memorising](interviews/numbers-to-know.md) | The handful you should be able to produce cold |

---

## How to use these

**Learners:** read the framework, then find the exercise that makes you use it. Every framework
page ends with the exercise and the discussion thread where it was argued out.

**Practitioners:** the playbooks are the transferable part. They assume nothing about this
repository and everything about the failure modes it documents.

**A warning about cheat sheets in general.** A compressed framework is a *prompt for thinking*,
not a substitute for it. Every page here names the condition under which it does not apply,
because a mental model you cannot falsify is a superstition with better formatting.
