# CLAUDE.md

@AGENTS.md

## Claude Code specifics

- The project skills in `.claude/skills/` are a symlink to `.agents/skills/`. Codex reads the
  same folder, so add or edit skills there and never replace the symlink with a copy.
- Invoke a project skill with the Skill tool when a task matches its row in the Skills table
  above, before starting the work. Where a project skill has the same name as a user-level or
  plugin skill (for example `humanizer`), the project copy is the one to use in this repo.
- When a user-level skill and a project skill both cover a task (for example
  `artifact-design` and `frontend-anti-slop` for an HTML artifact), load both. Apply the
  precedence order above: the host's page contract and the user's words come first, then
  `frontend-anti-slop` for what they leave open.
