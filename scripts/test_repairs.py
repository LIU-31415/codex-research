"""Local regression checks. Run with python -B scripts/test_repairs.py; no model calls."""

import argparse
from contextlib import ExitStack, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
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
    (repo / ".gitignore").write_text("runs/\n.runtime/\n", encoding="utf-8")
    tracked = ["runs/events.jsonl", "runs/answer.md", ".runtime/stderr.log"]
    for relative in [*tracked, "runs/private-untracked.md"]:
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("sk-" + "x" * 24, encoding="utf-8")
    subprocess.run(["git", "add", "-f", "--", *tracked], cwd=repo, check=True, capture_output=True)
    files = {p.relative_to(repo).as_posix() for p in privacy.iter_files(repo)}
    assert set(tracked) <= files, "tracked ignored outputs must still be scanned"
    assert "runs/private-untracked.md" not in files, "ignored local data must remain excluded"
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


def main():
    with tempfile.TemporaryDirectory(prefix="codex-research-regression-") as temporary:
        root = Path(temporary).resolve()
        check_tracked_outputs(root)
        disabled_skills = check_user_skills(root)
        check_evaluation_outputs(root, disabled_skills)
    print("REPAIR_CHECKS_OK: tracked privacy, user-skill overrides, state artifacts, execution failures")


if __name__ == "__main__":
    main()
