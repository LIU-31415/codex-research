"""Local regression checks. Run with python -B scripts/test_repairs.py; no model calls."""

import argparse
from contextlib import ExitStack, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


privacy = load_module("privacy_check", "scripts/check_public_repo.py")
runner = load_module("evaluation_runner", "evals/run_eval.py")


def check_tracked_outputs(root):
    repo = root / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True, capture_output=True)
    (repo / ".gitignore").write_text("runs/\n.runtime/\n.env*\n", encoding="utf-8")
    tracked = ["runs/events.jsonl", "runs/answer.md", ".runtime/stderr.log", "nested/check_public_repo.py", ".env", ".env.local", "production.env"]
    for relative in [*tracked, "runs/private-untracked.md", ".env.private"]:
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("sk-" + "x" * 24, encoding="utf-8")
    subprocess.run(["git", "add", "-f", "--", *tracked], cwd=repo, check=True, capture_output=True)
    files = {p.relative_to(repo).as_posix() for p in privacy.iter_files(repo)}
    assert set(tracked) <= files, "tracked ignored outputs must still be scanned"
    assert "runs/private-untracked.md" not in files, "ignored local data must remain excluded"
    assert ".env.private" not in files, "ignored local environment files must remain excluded"
    errors = []
    privacy.check_privacy(repo, errors)
    assert len(errors) == len(tracked), errors
    assert all("possible OpenAI-style token" in error for error in errors)


def check_user_skills(root):
    user = root / "user"
    codex_home = root / "eval-config"
    expected = set()
    for directory in (user / ".agents" / "skills", user / ".codex" / "skills", codex_home / "skills"):
        skill = directory / "example" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("unchanged", encoding="utf-8")
        expected.add(str(skill.resolve()))
    with patch.object(Path, "home", return_value=user):
        actual = runner.user_skill_paths({"CODEX_HOME": str(codex_home)})
    assert set(actual) == expected, "both home scopes and the selected Codex home must be covered"
    assert all(Path(p).read_text(encoding="utf-8") == "unchanged" for p in actual)
    config = runner.skill_override(actual)
    assert config.count("enabled=false") == len(expected)
    assert all(json.dumps(p, ensure_ascii=False) in config for p in actual)
    return actual


def check_repository_diagnostics(root):
    repo = root / "diagnostics"
    repo.mkdir()
    (repo / "with space.md").write_text("Synthetic", encoding="utf-8")
    document = repo / "README.md"
    document.write_text(
        '[space](<with space.md>) [encoded](with%20space.md#section) '
        '[title](with%20space.md "Title") [empty]( ) [self]()', encoding="utf-8",
    )
    errors = []
    privacy.check_markdown_links(repo, errors)
    assert not errors, errors
    document.write_text('[escape](%2e%2e/outside.md) [missing](missing.md)', encoding="utf-8")
    privacy.check_markdown_links(repo, errors)
    assert len(errors) == 2 and "escapes repository" in errors[0] and "missing link target" in errors[1], errors
    document.write_bytes(b"\xff")
    output = io.StringIO()
    with patch.object(privacy.sys, "argv", ["check_public_repo.py", "--root", str(repo)]), redirect_stdout(output):
        assert privacy.main() == 1
    assert "PUBLIC_REPO_CHECK_FAILED" in output.getvalue() and "not valid UTF-8" in output.getvalue()
    assert "evals/rubric.md is missing" in output.getvalue()


def check_evaluation_outputs(root, disabled_skills):
    evals = root / "evals"
    fixture = evals / "fixtures" / "research_state.md"
    fixture.parent.mkdir(parents=True)
    fixture.write_text("original state", encoding="utf-8")
    case = {
        "id": "state",
        "prompt": "Continue the synthetic review and save its state.",
        "checks": ["STATE_RECOVERY"],
        "files": ["fixtures/research_state.md"],
        "output_files": ["fixtures/research_state.md"],
    }
    cases_path = evals / "evals.json"
    (evals / "rubric.md").write_text("### `STATE_RECOVERY`\n", encoding="utf-8")
    cases_path.write_text(json.dumps([case]), encoding="utf-8")
    with patch.object(runner, "EVALS_DIR", evals), patch.object(runner, "CASES_PATH", cases_path):
        assert runner.load_cases() == [case]
        cases_path.write_text(json.dumps([case, {**case, "id": "STATE"}]), encoding="utf-8")
        try:
            runner.load_cases()
        except ValueError:
            pass
        else:
            raise AssertionError("case ids must not collide on case-insensitive filesystems")
        for field, value in (
            ("id", "../escape"), ("files", [str(fixture)]),
            ("files", ["../evals/fixtures/research_state.md"]), ("output_files", ["C:escape"]),
            ("prompt", None), ("prompt", " "), ("baseline_allowed", "false"),
            ("baseline_allowed", 0), ("files", None), ("files", "fixtures/research_state.md"),
            ("output_files", {}), ("checks", "STATE_RECOVERY"), ("checks", [None]),
            ("checks", ["UNDEFINED"]),
        ):
            cases_path.write_text(json.dumps([{**case, field: value}]), encoding="utf-8")
            try:
                runner.load_cases()
            except ValueError:
                pass
            else:
                raise AssertionError((field, value))
        cases_path.write_text(json.dumps([case]), encoding="utf-8")
    original_mkdtemp = tempfile.mkdtemp
    for scenario in ("success", "nonzero", "timeout", "launch_error", "missing_final", "missing_output"):
        commands = []
        workspaces = []
        args = argparse.Namespace(
            case=[], mode="both", model="synthetic-model", config=[], sandbox="workspace-write",
            codex="synthetic-codex", codex_home=None, timeout=1, run_id=scenario,
            dry_run=False, tool_profile="simulated",
        )

        class Process:
            pid = 12345
            returncode = 7 if scenario == "nonzero" else 0

            def __init__(self, command, **kwargs):
                if scenario == "launch_error":
                    raise OSError("synthetic launch failure")
                self.command = command
                self.workspace = Path(kwargs["cwd"])
                self.calls = 0
                commands.append(command)
                workspaces.append(self.workspace)

            def communicate(self, input=None, timeout=None):
                self.calls += 1
                if input is not None:
                    prompt = input.decode("utf-8")
                    final = Path(self.command[self.command.index("-o") + 1])
                    assert (final.parent / "prompt.txt").read_text(encoding="utf-8") == prompt
                    assert str(self.workspace) not in prompt
                    assert "fixtures/research_state.md" in prompt
                if scenario == "timeout" and self.calls == 1:
                    raise subprocess.TimeoutExpired(self.command, timeout)
                if scenario == "timeout":
                    return
                state = self.workspace / "fixtures" / "research_state.md"
                if scenario == "missing_output":
                    state.unlink()
                else:
                    state.write_text("updated state", encoding="utf-8")
                if scenario != "missing_final":
                    final = Path(self.command[self.command.index("-o") + 1])
                    final.write_text("Synthetic final response", encoding="utf-8")

            def kill(self):
                pass

        with ExitStack() as stack:
            for name, value in (
                ("parse_args", lambda: args), ("codex_version", lambda _: "synthetic-version"),
                ("git_commit", lambda: "synthetic-commit"), ("git_worktree_dirty", lambda: False),
                ("user_skill_paths", lambda _: disabled_skills),
            ):
                stack.enter_context(patch.object(runner, name, value))
            stack.enter_context(patch.object(runner, "EVALS_DIR", evals))
            stack.enter_context(patch.object(runner, "CASES_PATH", cases_path))
            stack.enter_context(patch.object(runner, "RUNS_DIR", root / "runs"))
            stack.enter_context(patch.object(runner.subprocess, "Popen", Process))
            # The timeout case exercises bookkeeping without stopping a real process.
            stack.enter_context(patch.object(runner.subprocess, "run"))
            stack.enter_context(patch.object(
                runner.tempfile, "mkdtemp",
                lambda prefix: original_mkdtemp(prefix=prefix, dir=root),
            ))
            stack.enter_context(redirect_stdout(io.StringIO()))
            exit_code = runner.main()
            if scenario == "success":
                with patch.object(Path, "mkdir", side_effect=FileExistsError), redirect_stdout(io.StringIO()):
                    assert runner.main() == 2, "a creation race must return a setup error"
        assert (exit_code == 0) == (scenario == "success"), scenario
        run_dir = root / "runs" / scenario
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["execution_ok"] == (scenario == "success"), scenario
        assert manifest["disabled_user_skills"] == disabled_skills
        assert all(runner.skill_override(disabled_skills) in command for command in commands)
        assert all(not workspace.exists() for workspace in workspaces), "temporary workspaces must be cleaned"
        if scenario == "success":
            for label in ("baseline", "skill"):
                saved = run_dir / "state" / label / "artifacts" / "fixtures" / "research_state.md"
                assert saved.read_text(encoding="utf-8") == "updated state", "save actual output before cleanup"


def check_metadata_and_fingerprint(root):
    repo = root / "metadata"
    repo.mkdir()
    skill = repo / "SKILL.md"
    valid = 'name: codex-research\ndescription: Synthetic description\nlicense: MIT\n'
    for content, accepted in (
        (valid, True),
        (valid.replace("Synthetic description", "x" * 1024), True),
        (valid.replace("Synthetic description", "x" * 1025), False),
        (valid.replace("Synthetic description", '""'), False),
        (valid.replace("Synthetic description", "null"), False),
        (valid.replace("Synthetic description", "|"), False),
        (valid.replace("Synthetic description", '"quoted description"'), True),
        (valid.replace("Synthetic description", "'single ''quoted'' description'"), True),
        (valid + "description: duplicate\n", False),
        (valid + "compatibility: unsupported locally\n", False),
        (valid + 'metadata: {"audience": "researchers"}\n', True),
        (valid + 'metadata: {"audience": 1}\n', False),
        (valid.replace("codex-research", "other-name"), False),
        (valid.replace("codex-research", '"codex-research"'), True),
        (valid + "  nested: invalid\n", False),
    ):
        skill.write_text("---\n" + content + "---\n", encoding="utf-8")
        errors = []
        privacy.check_metadata(repo, errors)
        skill_errors = [error for error in errors if error.startswith("SKILL.md")]
        assert bool(skill_errors) != accepted, (content, skill_errors)
    skill.write_text("---\n" + valid, encoding="utf-8")
    errors = []
    privacy.check_metadata(repo, errors)
    assert any("closing ---" in error for error in errors), errors
    skill.write_text("---\n" + valid + "---\n", encoding="utf-8")
    references = repo / "references"
    references.mkdir()
    with patch.object(runner, "ROOT", repo):
        previous = runner.skill_source_sha256()
        for relative in ("data.json", "nested/details.md"):
            source = references / relative
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text("first", encoding="utf-8")
            added = runner.skill_source_sha256()
            assert added != previous
            source.write_text("second", encoding="utf-8")
            previous = runner.skill_source_sha256()
            assert previous != added
        skill.write_text("---\n" + valid.replace("codex-research", '"codex-research"') + "---\n", encoding="utf-8")
        previous = runner.skill_source_sha256()
        workspace = runner.stage_workspace(root / "staging", True, {})
        staged_skill = workspace / ".agents" / "skills" / runner.EVAL_SKILL_NAME / "SKILL.md"
        assert "name: " + runner.EVAL_SKILL_NAME + "\n" in staged_skill.read_text(encoding="utf-8")
        staged = workspace / ".agents" / "skills" / runner.EVAL_SKILL_NAME / "references"
        assert {p.relative_to(staged) for p in staged.rglob("*") if p.is_file()} == {
            p.relative_to(references) for p in references.rglob("*") if p.is_file()
        }
        assert runner.skill_source_sha256() == previous
    assert not (ROOT / "references/mcp-compatibility.json").exists()
    assert (ROOT / "evals/mcp-compatibility.json").is_file()


def main():
    assert runner.load_cases(), "the repository's actual evaluation cases must be valid"
    cases = [{"id": "first"}, {"id": "second"}]
    assert runner.selected_cases(cases, ["second", "first", "second"]) == [cases[1], cases[0]]
    for returncode, stdout, stderr, expected in (
        (0, "synthetic-version\n", "", "synthetic-version"),
        (0, "", "synthetic-version\n", "synthetic-version"),
        (1, "", "synthetic launch error", None),
    ):
        completed = subprocess.CompletedProcess([], returncode, stdout, stderr)
        with patch.object(runner.subprocess, "run", return_value=completed):
            assert runner.codex_version("synthetic-codex") == expected
    for value in ("../escape", "/absolute", "C:escape", "CON", "", "a/b", "a\\b"):
        try:
            runner.validate_component(value, "run id")
        except ValueError:
            pass
        else:
            raise AssertionError(value)
    runner.validate_component("release-0_2_3", "run id")
    output = io.StringIO()
    with redirect_stdout(output):
        runner.print_dry_run({"id": "safe", "prompt": "Synthetic", "baseline_allowed": False}, "codex", "both", None, [], "read-only")
    assert " / baseline]" not in output.getvalue() and " / skill]" in output.getvalue()
    with ExitStack() as stack:
        try:
            temporary = stack.enter_context(tempfile.TemporaryDirectory(prefix="codex-research-regression-"))
            root = Path(temporary).resolve()
            probe = root / "probe"
            probe.mkdir()
            (probe / "sample").write_text("probe", encoding="utf-8")
            list(probe.iterdir())
            (probe / "sample").read_text(encoding="utf-8")
        except OSError as exc:
            print(f"REPAIR_CHECKS_ENVIRONMENT_ERROR: temporary workspace unavailable; checks incomplete ({type(exc).__name__}). Set TMPDIR, TEMP or TMP to a writable directory.", file=sys.stderr)
            try:
                stack.close()
            except OSError:
                print("Temporary workspace cleanup also failed.", file=sys.stderr)
            return 3
        check_tracked_outputs(root)
        check_repository_diagnostics(root)
        check_metadata_and_fingerprint(root)
        disabled_skills = check_user_skills(root)
        check_evaluation_outputs(root, disabled_skills)
    print("REPAIR_CHECKS_OK: safe paths, unique cases, version failures, skipped baseline, tracked privacy, user-skill overrides, state artifacts, execution failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
