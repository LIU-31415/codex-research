#!/usr/bin/env python3
"""Run paired, fixture-backed Codex evaluations.

The runner deliberately stays dependency-free. It records the Codex event
stream and final message, but does not claim that a small run is a benchmark.
"""

from __future__ import annotations

import argparse
import datetime as datetime_module
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = ROOT / "evals"
CASES_PATH = EVALS_DIR / "evals.json"
RUNS_DIR = EVALS_DIR / "runs"
EVAL_SKILL_NAME = "codex-research-eval"


def utc_now() -> str:
    return (
        datetime_module.datetime.now(datetime_module.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def load_cases() -> List[Dict[str, Any]]:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("evals.json must contain a JSON array")
    cases: List[Dict[str, Any]] = []
    seen = set()
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("each evaluation case needs a string id")
        case_id = item["id"]
        if case_id in seen:
            raise ValueError("duplicate evaluation case: " + case_id)
        seen.add(case_id)
        for relative in item.get("files", []):
            if not isinstance(relative, str):
                raise ValueError("fixture paths must be strings: " + case_id)
            source = (EVALS_DIR / relative).resolve()
            if not is_within(source, EVALS_DIR) or not source.is_file():
                raise ValueError("missing or unsafe fixture for " + case_id + ": " + relative)
        cases.append(item)
    return cases


def git_commit() -> Optional[str]:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def git_worktree_dirty() -> Optional[bool]:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return bool(completed.stdout.strip())


def skill_source_sha256() -> str:
    digest = hashlib.sha256()
    paths = [ROOT / "SKILL.md"] + sorted((ROOT / "references").glob("*.md"))
    for path in paths:
        relative = path.relative_to(ROOT).as_posix().encode("utf-8")
        digest.update(relative + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def resolve_executable(executable: str) -> str:
    resolved = shutil.which(executable)
    if resolved:
        return resolved
    if os.name == "nt" and not Path(executable).suffix:
        resolved = shutil.which(executable + ".cmd")
        if resolved:
            return resolved
    return executable


def codex_version(executable: str) -> Optional[str]:
    try:
        completed = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    value = (completed.stdout or completed.stderr).strip()
    return value or None


def selected_cases(all_cases: Sequence[Dict[str, Any]], requested: Sequence[str]) -> List[Dict[str, Any]]:
    by_id = {case["id"]: case for case in all_cases}
    if not requested:
        return list(all_cases)
    unknown = [case_id for case_id in requested if case_id not in by_id]
    if unknown:
        raise ValueError("unknown case(s): " + ", ".join(unknown))
    return [by_id[case_id] for case_id in requested]


def stage_workspace(
    temporary_root: Path,
    with_skill: bool,
    case: Dict[str, Any],
) -> Path:
    workspace = temporary_root / ("skill" if with_skill else "baseline")
    workspace.mkdir(parents=True, exist_ok=True)

    for relative in case.get("files", []):
        source = (EVALS_DIR / relative).resolve()
        destination = workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    if with_skill:
        # Use a unique name so a user-level codex-research installation cannot
        # silently replace the copy under evaluation.
        skill_dir = workspace / ".agents" / "skills" / EVAL_SKILL_NAME
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        skill_text = skill_text.replace(
            "name: codex-research\n",
            "name: {}\n".format(EVAL_SKILL_NAME),
            1,
        )
        (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
        shutil.copytree(
            ROOT / "references",
            skill_dir / "references",
            dirs_exist_ok=True,
        )

    return workspace


def build_prompt(
    case: Dict[str, Any],
    with_skill: bool,
    workspace: Optional[Path] = None,
) -> str:
    parts = []
    if with_skill:
        parts.append(
            "Use the local evaluation copy of `codex-research` explicitly. "
            "Its temporary skill name is `{}` so a user-level installation cannot be selected.".format(
                EVAL_SKILL_NAME
            )
        )
    else:
        parts.append("Run this evaluation without loading or using any evaluation Skill.")
    parts.append(case["prompt"])
    files = case.get("files", [])
    if files:
        listed = "\n".join(
            "- " + value
            + (" (exact path: " + str(workspace / value) + ")" if workspace else "")
            for value in files
        )
        parts.append(
            "Read each evaluation fixture before answering. The files are available at these paths:\n"
            + listed
        )
    return "\n\n".join(parts)


def command_for(
    executable: str,
    workspace: Path,
    final_path: Path,
    model: Optional[str],
    configs: Sequence[str],
    sandbox: str,
) -> List[str]:
    command = [
        executable,
        "exec",
        "--ephemeral",
        "--sandbox",
        sandbox,
        "--skip-git-repo-check",
        "--color",
        "never",
        "--json",
        "-C",
        str(workspace),
        "-o",
        str(final_path),
    ]
    if model:
        command.extend(["--model", model])
    for config in configs:
        command.extend(["--config", config])
    command.append("-")
    return command


def run_one(
    output_dir: Path,
    executable: str,
    workspace: Path,
    prompt: str,
    model: Optional[str],
    configs: Sequence[str],
    sandbox: str,
    timeout: int,
    environment: Dict[str, str],
) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    final_path = output_dir / "final.md"
    events_path = output_dir / "events.jsonl"
    stderr_path = output_dir / "stderr.log"
    command = command_for(executable, workspace, final_path, model, configs, sandbox)

    started_at = utc_now()
    started = time.monotonic()
    timed_out = False
    error: Optional[str] = None
    with events_path.open("w", encoding="utf-8") as events_file, stderr_path.open(
        "w", encoding="utf-8"
    ) as stderr_file:
        try:
            completed = subprocess.run(
                command,
                cwd=str(workspace),
                env=environment,
                input=prompt,
                stdout=events_file,
                stderr=stderr_file,
                check=False,
                text=True,
                timeout=timeout,
            )
            return_code: Optional[int] = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            return_code = None
            error = "timeout after {} seconds".format(timeout)
        except OSError as exc:
            return_code = None
            error = str(exc)

    result = {
        "started_at_utc": started_at,
        "duration_seconds": round(time.monotonic() - started, 3),
        "exit_code": return_code,
        "timed_out": timed_out,
        "error": error,
        "final_file": str(final_path.name) if final_path.exists() else None,
        "events_file": events_path.name,
        "stderr_file": stderr_path.name,
    }
    json_write(output_dir / "result.json", result)
    return result


def print_dry_run(
    case: Dict[str, Any],
    executable: str,
    mode: str,
    model: Optional[str],
    configs: Sequence[str],
    sandbox: str,
) -> None:
    for with_skill, label in ((False, "baseline"), (True, "skill")):
        if mode not in ("both", label):
            continue
        prompt = build_prompt(case, with_skill)
        print("[{} / {}]".format(case["id"], label))
        print("  codex executable: {}".format(executable))
        print("  model: {}".format(model or "configured default"))
        print("  config overrides: {}".format(", ".join(configs) or "none"))
        print("  sandbox: {}".format(sandbox))
        print("  prompt: {}".format(prompt.replace("\n", " ")))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", default=[], help="case id; repeatable")
    parser.add_argument(
        "--mode",
        choices=("baseline", "skill", "both"),
        default="both",
        help="which side of the pair to run",
    )
    parser.add_argument("--model", help="fixed Codex model identifier")
    parser.add_argument(
        "--sandbox",
        choices=("read-only", "workspace-write"),
        default="read-only",
        help="sandbox policy for each Codex run",
    )
    parser.add_argument(
        "--config",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Codex config override; repeatable",
    )
    parser.add_argument("--codex", default="codex", help="Codex executable")
    parser.add_argument("--codex-home", help="isolated CODEX_HOME directory")
    parser.add_argument(
        "--tool-profile",
        default="record-manually",
        help="label for the configured tool/connectors",
    )
    parser.add_argument("--timeout", type=int, default=900, help="per-run timeout in seconds")
    parser.add_argument("--run-id", help="output run id; defaults to UTC timestamp")
    parser.add_argument("--dry-run", action="store_true", help="print the planned runs only")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.timeout <= 0:
        print("--timeout must be positive", file=sys.stderr)
        return 2

    try:
        cases = selected_cases(load_cases(), args.case)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("Evaluation setup error: {}".format(exc), file=sys.stderr)
        return 2

    executable = resolve_executable(args.codex)
    if args.dry_run:
        for case in cases:
            print_dry_run(
                case,
                executable,
                args.mode,
                args.model,
                args.config,
                args.sandbox,
            )
        return 0

    version = codex_version(executable)
    if version is None:
        print(
            "Cannot run evaluations: Codex executable not found or --version failed. "
            "Use --codex or run --dry-run.",
            file=sys.stderr,
        )
        return 2

    run_id = args.run_id or datetime_module.datetime.now(datetime_module.timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )
    run_dir = RUNS_DIR / run_id
    if run_dir.exists():
        print("Run directory already exists: {}".format(run_dir), file=sys.stderr)
        return 2
    run_dir.mkdir(parents=True)

    environment = os.environ.copy()
    if args.codex_home:
        environment["CODEX_HOME"] = str(Path(args.codex_home).expanduser().resolve())

    manifest: Dict[str, Any] = {
        "run_id": run_id,
        "created_at_utc": utc_now(),
        "repository": "codex-research",
        "skill_commit": git_commit(),
        "skill_worktree_dirty": git_worktree_dirty(),
        "skill_source_sha256": skill_source_sha256(),
        "evaluation_skill_name": EVAL_SKILL_NAME,
        "codex_version": version,
        "codex_executable": executable,
        "model": args.model or "configured default",
        "config_overrides": args.config,
        "timeout_seconds": args.timeout,
        "codex_home_supplied": bool(args.codex_home),
        "tool_profile": args.tool_profile,
        "sandbox": args.sandbox,
        "mode": args.mode,
        "cases": [],
        "limitations": [
            "A small fixture-backed run is not a production router or retrieval benchmark.",
            "External connector capability and model behavior depend on the supplied environment.",
        ],
    }
    json_write(run_dir / "manifest.json", manifest)
    json_write(
        run_dir / "score-template.json",
        {
            "run_id": run_id,
            "scorer": "",
            "scored_at_utc": "",
            "cases": [
                {
                    "case_id": case["id"],
                    "baseline": {
                        check: (
                            None
                            if case.get("baseline_allowed", True)
                            else "N/A"
                        )
                        for check in case.get("checks", [])
                    },
                    "skill": {check: None for check in case.get("checks", [])},
                    "notes": "",
                }
                for case in cases
            ],
        },
    )

    with tempfile.TemporaryDirectory(prefix="codex-research-eval-") as temporary:
        temporary_root = Path(temporary)
        for case in cases:
            case_dir = run_dir / case["id"]
            prompt_path = case_dir / "request.md"
            prompt_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_path.write_text(
                "# Evaluation request\n\n"
                + case["prompt"]
                + "\n\n## Fixture files\n\n"
                + "\n".join("- " + value for value in case.get("files", []))
                + "\n",
                encoding="utf-8",
            )
            case_record: Dict[str, Any] = {
                "case_id": case["id"],
                "declared_checks": case.get("checks", []),
                "baseline_allowed": case.get("baseline_allowed", True),
            }
            for with_skill, label in ((False, "baseline"), (True, "skill")):
                if args.mode not in ("both", label):
                    continue
                if not with_skill and not case.get("baseline_allowed", True):
                    case_record["baseline_skipped_reason"] = (
                        "Skipped because the fixture contains source instructions "
                        "that could prompt unsafe baseline actions."
                    )
                    continue
                workspace = stage_workspace(temporary_root / case["id"], with_skill, case)
                prompt = build_prompt(case, with_skill, workspace)
                result = run_one(
                    case_dir / label,
                    executable,
                    workspace,
                    prompt,
                    args.model,
                    args.config,
                    args.sandbox,
                    args.timeout,
                    environment,
                )
                case_record[label] = result
            manifest["cases"].append(case_record)
            json_write(run_dir / "manifest.json", manifest)

    print("Evaluation run complete: {}".format(run_dir))
    print("Score the saved outputs with evals/rubric.md; do not treat this as a benchmark.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
