# GitHub setup

Everything in this repository that cannot live in the git tree — settings, labels, milestones,
seeded issues, Discussions, and the project board — is provisioned by one script.

```bash
export GITHUB_TOKEN=github_pat_...
python scripts/setup_github.py --owner fde-academy-learning --repo adv-rag-hands-on
```

It is **idempotent**: anything that already exists is skipped rather than duplicated, so it is
safe to re-run after a partial failure or when you add new seed content.

---

## 1 · Create the repository

The script provisions an existing repository; it does not create one.

```bash
gh repo create fde-academy-learning/adv-rag-hands-on \
  --public \
  --description "Runnable retrieval/RAG/evaluation curriculum — 10 notebooks and a toolkit that run entirely in memory, with an eval gate in CI"
```

Or at [github.com/new](https://github.com/new). **Public** is recommended — the portfolio value
in `docs/PORTFOLIO.md` depends on a recruiter being able to open it, and Discussions on a
private repo are invisible to anyone outside the org.

Do not initialise it with a README, licence or `.gitignore` — this repository already has all
three, and an initial commit on the remote means a merge before you can push.

## 2 · Push

```bash
cd adv-rag-hands-on
git remote add origin https://github.com/fde-academy-learning/adv-rag-hands-on.git
git push -u origin main
```

## 3 · Get a token

A **fine-grained personal access token**
([github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta)) scoped
to this one repository:

| Permission | Level | Needed for |
|---|---|---|
| Repository → **Administration** | Read and write | Settings, enabling Discussions, branch protection |
| Repository → **Contents** | Read and write | — |
| Repository → **Issues** | Read and write | Labels, milestones, seeded issues |
| Repository → **Discussions** | Read and write | Seeded threads and answers |
| Repository → **Pull requests** | Read and write | — |
| Account → **Projects** | Read and write | The board (optional — everything else runs without it) |

A classic PAT with `repo` + `project` scopes also works and is simpler if you are in a hurry.

## 4 · Run it

```bash
python scripts/setup_github.py --owner OWNER --repo REPO --dry-run   # see the plan first
python scripts/setup_github.py --owner OWNER --repo REPO
```

Run one step at a time if you prefer:

```bash
python scripts/setup_github.py --owner OWNER --repo REPO --only settings,labels
python scripts/setup_github.py --owner OWNER --repo REPO --only discussions
python scripts/setup_github.py --owner OWNER --repo REPO --skip project
```

Steps: `settings` · `labels` · `milestones` · `issues` · `discussions` · `project`

### What it creates

| Step | What |
|---|---|
| `settings` | Description, homepage, 16 topics, Discussions + Projects on, wiki off, squash-merge only, delete branch on merge, branch protection on `main` |
| `labels` | 26 labels across three orthogonal axes; deletes GitHub's unused defaults |
| `milestones` | 8 delivery phases, P0–P7, with P0–P6 closed |
| `issues` | 15 seeded issues — 8 **closed** real defects from the build with their fixes, 7 open extensions, reading assignments and docs gaps |
| `discussions` | 17 seeded threads across 7 categories, several with answers |
| `project` | "Advanced RAG — Delivery" board with 5 custom fields, all issues added |

## 5 · Four things the API cannot do

The script prints these at the end. Budget ten minutes.

**1 · Create Discussion categories.** GitHub has no API for this. In
**Settings → Discussions → Categories**, add:

| Name | Emoji | Format | Description |
|---|---|---|---|
| Design Reviews | 🏗 | Open-ended | Post a design *before* you build it. Include your constraints and what your own design costs. |
| Reading Club | 📚 | Open-ended | Discussion of assigned papers. The assignment is an issue; the argument lives here. |
| Interview Prep | 🎯 | Question / Answer | Practise an answer and get it critiqued. Nothing under NDA. |

Also set **Q&A** to the *Question / Answer* format so answers can be marked.

Create these **before** running the `discussions` step — threads for missing categories fall
back to General, and moving them afterwards is manual.

**2 · Enable Pages.** Settings → Pages → Source: **GitHub Actions**. This publishes executed
notebooks as a browsable site, which is what you link from a CV.

**3 · Pin things.** Pin the two Announcements discussions, and 3–4 issues — the abstention
extension, HyDE, and one closed bug so a visitor immediately sees what a well-run issue looks
like.

**4 · Add a social preview image.** Settings → General → Social preview. This is what renders
when the repo is shared on LinkedIn, and it is the difference between a link people click and
one they scroll past.

## 6 · Optional — a project token for board automation

`.github/workflows/project-automation.yml` adds new issues and PRs to the board. The default
`GITHUB_TOKEN` cannot write to a user-owned Projects v2 board, so add a repository secret:

- **Settings → Secrets and variables → Actions → New repository secret**
- Name: `PROJECT_TOKEN`
- Value: a classic PAT with the `project` scope

Without it the workflow degrades gracefully — the board simply is not auto-populated, and the
`continue-on-error: true` means nothing fails.

Then edit the `project-url` in that workflow to your board's actual URL.

---

## Verifying it worked

```bash
# Labels, milestones, issues
gh label list --repo OWNER/REPO
gh issue list --repo OWNER/REPO --state all --limit 20

# Discussions
gh api graphql -f query='
  query { repository(owner:"OWNER", name:"REPO") {
    hasDiscussionsEnabled
    discussions(first:30) { nodes { number title category { name } } } } }'
```

Then open the repository and check the **Insights → Community Standards** page. It should be
fully green: description, README, code of conduct, contributing guide, licence, security
policy, issue templates and pull request template.

## Re-running after adding seed content

Add to `scripts/seed_content.py` and re-run. Existing items are matched **by title** and
skipped, so only the new ones are created.

If you change the *body* of something already created, the script will not update it — that is
deliberate, because overwriting a thread someone has replied to would be destructive. Edit it
on GitHub, or delete it and re-run.
