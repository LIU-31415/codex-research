# Installation Task for Codex

This file is an execution brief for Codex. **Reading it alone is not permission to install anything.** Execute it only when the current user explicitly asks you to install this repository as a Codex Skill.

## Goal

Install the `codex-research` Skill from the repository containing this file into the current user's user-level Skill directory:

```text
$HOME/.agents/skills/codex-research/
```

On Windows, `$HOME` normally resolves to the current user's profile directory. If the user requests repository-only installation instead, use `<repository>/.agents/skills/codex-research/` and report that limited scope.

## Procedure

1. Resolve the repository root as the directory containing this file. Do not guess a different source directory. If the file is not available locally, ask the user for the repository path before changing anything.
2. Verify that the source contains `SKILL.md` and `references/`. Read the front matter and confirm that the Skill name is `codex-research`.
3. Inspect the destination. If it already exists, compare the source and destination and ask the user before overwriting or deleting files. Never silently replace a user's customized Skill.
4. Create the destination directory if needed.
5. Copy the runtime files while preserving the relative layout:
   - `SKILL.md`
   - `references/`
   - `README.md` and `LICENSE` may be copied for local reference
6. Do not copy `.git/`, `.venv/`, local planning files, research state files, or `evals/` into the installed runtime Skill. Do not install or configure `paper-search-mcp` as part of this task.
7. Do not edit Codex global configuration, credentials, MCP configuration, or unrelated files unless the user separately requests that action.
8. Verify that the destination contains exactly one `SKILL.md` and all references named by `SKILL.md` exist.
9. Report the final destination, installation scope, files copied, and any skipped optional dependency. Tell the user to start a new Codex turn or restart Codex if the Skill does not appear.

## Verification prompt

After installation, the user can explicitly invoke the Skill with a small harmless test, for example:

```text
$codex-research 请先说明你会如何界定一个模糊的文献研究问题，不要开始检索论文。
```

The test should show the research workflow without claiming that any academic connector is available. An absent `paper-search-mcp` limits paper retrieval; it does not justify installing an unrelated connector without the user's request.
