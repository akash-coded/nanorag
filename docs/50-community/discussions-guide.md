# Discussions guide

Discussions are the internal-Stack-Overflow half of this playground. Issues are *tracked work
with an owner*; Discussions are *everything else* — and the difference matters, because a
question filed as an issue either sits open forever or gets closed without being searchable.

## Prefixes: the categories GitHub will not let us create

This repository has **nine** discussion categories. GitHub provides no API to add more — there
is no category mutation in the GraphQL schema, and creating one is a manual action in repository
settings. Rather than leave the structure unbuilt, some kinds of thread carry a **title prefix**
and a **label**. Together they do what a tenth category would have done: make a set of threads
findable, filterable, and visually distinct in a list.

| Prefix | Category | Label | What it is |
|---|---|---|---|
| `[clinic · EX-NN]` | Q&A | [`clinic`](https://github.com/akash-coded/nanorag/labels/clinic) | One long-running thread per exercise. Ask here rather than opening a duplicate |
| `[maths]` | Q&A | [`maths`](https://github.com/akash-coded/nanorag/labels/maths) | A derivation, argued out. Pairs with a page in `01-mathematical-foundations/` |
| `[errata]` | Q&A | [`errata`](https://github.com/akash-coded/nanorag/labels/errata) | The material is wrong, or more confident than it should be. Confirmed errata become issues |
| `[solution · EX-NN]` | Show and Tell | [`solution`](https://github.com/akash-coded/nanorag/labels/solution) | A submission, **with numbers**. Reviewers reply with a measurement, not an opinion |
| `[negative result]` | Show and Tell | [`negative-result`](https://github.com/akash-coded/nanorag/labels/negative-result) | Measured and rejected. Full credit — this is the most useful category here |
| `[round · <shape>]` | Interview Prep | [`interview-round`](https://github.com/akash-coded/nanorag/labels/interview-round) | A full simulated loop with a scoring rubric, not a single question |
| `[office hours · <date>]` | Announcements | [`office-hours`](https://github.com/akash-coded/nanorag/labels/office-hours) | One dated session. Agenda before, notes after, thread stays open |
| `[poll]` | Polls | — | Vote **before** the reveal. The gap between the vote and the measurement is the content |

**Filtering.** The label is the reliable filter, because a title can be edited and a label cannot
be edited by accident. To see every exercise clinic thread:

```text
https://github.com/akash-coded/nanorag/discussions?discussions_q=label%3Aclinic
```

**Why not just use the categories loosely?** Because Q&A would become a single undifferentiated
list of eighty threads, and the whole reason a category exists is so a person scanning it can
tell what kind of thing they are looking at. The prefix restores that in one glance.

### Where to post what

- **Stuck on an exercise** → the `[clinic · EX-NN]` thread for that exercise. Not a new thread —
  the answers accumulate where the next person will look for them.
- **Finished an exercise** → Show and Tell with `[solution · EX-NN]`, including your numbers, your
  interval, and what you tried that did not work.
- **A measurement that contradicts the material** → Show and Tell with `[negative result]`, or
  Q&A with `[errata]` if you think the material is simply wrong.
- **A derivation you cannot follow** → Q&A with `[maths]`.
- **Anything else** → the category that fits, no prefix.

## The categories

| Category | Format | Use it for | Do not use it for |
|---|---|---|---|
| 📣 **Announcements** | Announcement | Cohort schedules, releases, breaking changes | Questions |
| 🙋 **Q&A** | Question / answer | "Why does X?", "How do I Y?", errors, confusion | Bug reports with a reproduction (→ issue) |
| 🏗 **Design Reviews** | Open-ended | An architecture you want challenged **before** you build it | Finished work (→ Show & Tell) |
| 🎤 **Show & Tell** | Open-ended | Capstones, decision records, surprising results | Work in progress |
| 📚 **Reading Club** | Open-ended | Discussion of an assigned paper | The assignment itself (→ issue) |
| 💡 **Ideas** | Open-ended | Half-formed extension ideas | Ideas with a hypothesis (→ extension issue) |
| 🗳 **Polls** | Poll | Session scheduling, topic prioritisation | Technical decisions — those need a design review |
| 🎯 **Interview Prep** | Q&A | Practising an answer and getting it critiqued | Real interview questions under NDA |

## Asking a question people can answer

The [Q&A template](../../.github/DISCUSSION_TEMPLATE/q-a.yml) has four fields, and the second one
is the important one.

1. **The question in one line.** If you cannot, you have two questions.
2. **What you have already tried.** This is the field that separates a question from a request.
   It also, more often than not, contains the answer — writing it out is why.
3. **The numbers or the traceback.** Evidence beats adjectives. "Recall seems low" is not
   answerable; "Evidence Recall@8 is 0.61 on the temporal slice, 0.79 elsewhere" is.
4. **Where.** Notebook and section.

**A good title is a sentence someone would search for.**
`Why does Recall@N go up but full-chain recall stay flat?`
not `help with retrieval`

## Answering well

- **Answer the question that was asked**, then say what you would have asked instead.
- **Link the notebook cell.** "Notebook 01 §1.3 measures this" is a better answer than a
  paragraph, because the asker can then vary it.
- **Mark the answer.** An unanswered-looking thread gets asked again next cohort.
- **If you are guessing, say so.** "I think it is X, but I have not measured it" is a useful
  answer. Confident wrong answers are how a forum dies.

## Converting between surfaces

```mermaid
flowchart LR
    Q["💬 Q&amp;A question"] -->|"turns out to be a real defect"| I["🐛 Bug issue<br/><i>with a reproduction</i>"]
    Q -->|"answered, generally useful"| D["📄 Docs PR<br/><i>so nobody asks again</i>"]
    DR["🏗 Design review"] -->|"design agreed"| E["🚀 Extension issue<br/><i>with a hypothesis</i>"]
    E --> PR["🔀 Pull request"]
    PR --> ST["🎤 Show &amp; Tell"]
    ID["💡 Idea"] -->|"acquires a hypothesis"| E
    ID -.->|"stays vague"| ID
    classDef d fill:#EFEDFB,stroke:#6C5CE0,color:#101318
    classDef i fill:#FBF1E2,stroke:#E9A83C,color:#101318
    class Q,DR,ID,ST d
    class I,E,PR,D i
```

**The rule:** a discussion becomes an issue when it acquires an *owner and acceptance
criteria*. Until then it is a conversation, and conversations belong here.

The most valuable conversion is the second one: **a Q&A thread that has been answered three
times is a documentation gap.** Open a docs PR and link the thread in it.

## For faculty

- **Seeded threads are labelled as such.** Several worked examples in Q&A and Design Reviews
  were written by faculty to model the shape of a good question and a good answer. They are
  marked `[worked example]` in the title so nobody mistakes them for a real student's
  question.
- **Answer in public, always.** A DM answer helps one student; the same answer in Q&A helps
  every future cohort. If someone asks in a DM, ask them to post it and answer there.
- **Do not close a thread as "read the docs".** If the docs answered it, they were not
  findable, and that is a docs issue.
- **Use polls for scheduling only.** A technical decision made by poll is a decision with no
  owner.

## Etiquette

- Search before posting. Three of the top ten most-viewed threads in a healthy cohort are
  duplicates that got merged.
- Post code as text in a fenced block, not as a screenshot. Screenshots are not searchable and
  cannot be copied into a reply.
- Redact anything from a real client. This repository is public; the corpus in it is
  synthetic for exactly this reason.
- Negative results are welcome in Show & Tell and are **not** failures. "I tried HyDE and it
  did not clear the noise band, here is why I think that is" is one of the more useful things
  you can post.
