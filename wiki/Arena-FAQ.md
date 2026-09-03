# Arena FAQ

Short answers to what people ask in the first ten minutes of the L.A.B. simulator. Edit freely.

## "Where do I start?"

`python scripts/lab.py next`. It lists what you can start right now, challenges first. `C01` and `C03` need nothing; everything else unlocks from something.

In a Codespace this runs for you on attach.

## "What is the difference between a challenge and a lab?"

| | Challenge `C` | Lab `L` |
|---|---|---|
| Time | 5–15 min | 15–50 min |
| Asks for | one mechanism | a **decision**, then the code |
| Shapes | `implement`, `fill`, `fix`, `predict` | `implement` |
| Checks | public + hidden | public + hidden |
| Ends with | *what you can now do*, and the lab it unlocks | a debrief, and the next lab with the reason |

Challenges are the on-ramp. They are **not** prerequisites for labs — nobody partway through the labs is walled off by them.

## "I filled the blanks and it says `expected 4 sentences, got 1`. What?"

That is the check working. A `fill` starter imports with its blanks unfilled — the harness binds `____` to placeholder text — so every check gets to say in the mechanism's own words what the blank costs. Read the message, not the traceback; there is no traceback.

If a message is *unhelpful* — you read it and still do not know what to change — that is a bug in the lab. Open a [lab feedback issue](https://github.com/akash-coded/nanorag/issues/new?template=lab_feedback.yml).

## "The public checks pass and `--hidden` fails."

Normal. Expected. **The gap between them is the lesson.** Hidden checks cover what the brief deliberately did not mention — empty input, a duplicate id, a degenerate config. The reply names the exact check and why.

## "What does the sandbox actually see when I post in a thread?"

Your comment, and nothing else. The job that runs your code has **no credentials** (a zero-scope token), runs it in a container with **no network**, a read-only filesystem, no capabilities, as an unprivileged user, with a 30-second kill. The job that posts the reply never sees your code — it reads a JSON report. Your comment never reaches a shell command line either; it is passed by environment variable into a file.

So: a hostile submission finds nothing to reach. That is why it is safe to have a public thread accept code.

## "Does a `predict` challenge need a code block?"

No. Post the word or number — `negative`, `packing`. The workflow wraps it as `ANSWER = ...` for you.

## "I passed. Why does re-posting still count an attempt?"

Because the board answers *how many tries did it take*, and a pass never turns back into *Retrying* just because you were curious. Attempts go up; Outcome stays Passed.

## "Where is my progress?"

- Locally: `python scripts/lab.py status`. Derived from the checks — nothing stored, nothing to drift.
- For the cohort: [the Hands-on Tracker](https://github.com/users/akash-coded/projects/11) — one row per person per item, moved by the workflows when you submit in a thread or open a PR.

## "Can I see the reference solution?"

`reference.py` in every lab directory. Read it **after** you pass. The debrief in the brief is worth more than the reference and is where the actual teaching is.

## "The workflow did not reply."

Check the thread title starts with an `[arena · Cnn]` or `[submit · Lnn]` prefix; the workflow only listens there. If it does and nothing came back in ~2 minutes, the [Actions tab](https://github.com/akash-coded/nanorag/actions/workflows/discussion-lab.yml) shows the run — a timeout means something in your solution never returned.
