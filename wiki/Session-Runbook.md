# Session runbook — for whoever is running the cohort

The minimum you need to run a hands-on session with this repository, end to end. Nothing here needs a pull request; it is all scripts and boards.

## Before the session (10 minutes)

**1. Pick the items.** Two challenges and one lab is a good 45-minute block. `python scripts/lab.py list` shows every item with its time and format. Prefer a `predict` challenge first — it needs no setup and gets people reasoning before typing.

**2. Assign them.**

```bash
python scripts/assign.py --session 2026-09-08 --items C03,C02,L03 \
    --to alice,bob,carol --due 2026-09-10 --announce
```

That creates one Tracker row per person per item (`Outcome = Assigned`), and `--announce` posts a session thread in Announcements that @mentions everyone with the list, the Codespaces button, and where progress is tracked. Drop `--announce` if you would rather tell them yourself.

**3. Have the Codespaces link ready.** [codespaces.new/akash-coded/nanorag?quickstart=1](https://codespaces.new/akash-coded/nanorag?quickstart=1). With prebuilds configured it opens ready in ~10 seconds; without, ~2 minutes on first open. Say so up front.

## During the session

- **Do the `predict` one together first, out loud.** Ask for a vote before anyone runs anything. The room's distribution is the teaching content; the reveal is one command.
- **Send everyone to the arena thread for the item**, not to you. `[arena · C03]` in Show and Tell. The sandbox replies in about a minute with what passed, what did not, and the next item — and the thread accumulates the common mistakes where the next cohort will find them.
- **Watch the Tracker, not the room.** [Board #11](https://github.com/users/akash-coded/projects/11), grouped by Outcome. *Retrying* with Attempts ≥ 3 is someone to go and sit with. *Assigned* twenty minutes in is someone who has not started and may be stuck on setup.

## After the session

**4. Note it.** Add an entry to [Office Hours Log](Office-Hours-Log) — date, what came up, where it landed. Two minutes; the same three questions come up every cohort and a log turns the fourth asking into a link.

**5. Read the board the next morning.**

| What you see | What it means |
|---|---|
| Still *Assigned* past the due date | Never tried. Ask why — usually setup, sometimes fear of the thread being public |
| *Retrying*, Attempts 4+ | Stuck on a hidden check. Read their thread reply; the check message says which |
| *Passed after retry* on most people | The lab is well-pitched |
| *Passed* first time on everyone | Too easy for this cohort; move it to a warm-up |
| Nobody passed | Either the brief is wrong or the check message is. Open a lab feedback issue — that is a bug, not a cohort problem |

**6. Check the Pulse.** [Board #12](https://github.com/users/akash-coded/projects/12) refreshes every six hours — unanswered Q&A older than 48h is the row to act on. A question a learner asked during the session and nobody answered is the fastest way to lose them.

## If the sandbox misbehaves

The [Lab submissions workflow](https://github.com/akash-coded/nanorag/actions/workflows/discussion-lab.yml) has three jobs. `execute` failing with a timeout is the learner's code looping; `post` failing is almost always `PROJECT_TOKEN` missing the `project` scope — the reply still posts, only the Tracker update is skipped, and the log says so.
