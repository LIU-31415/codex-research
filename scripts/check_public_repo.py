"""Deterministic checks for the public codex-research repository.

This intentionally does not run a model, contact an MCP, or inspect user-level
Codex configuration. It checks only repository content and local metadata.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


TEXT_SUFFIXES = {
    ".env",
    ".md",
    ".json",
    ".jsonl",
    ".log",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SKIP_DIRS = {".git", ".venv", "__pycache__", ".runtime", "runs"}

# High-signal patterns only: ordinary words such as "token" or "credential"
# are allowed in documentation. The checker itself is excluded from scanning.
SENSITIVE_PATTERNS = [
    ("Windows user path", re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|Documents|Desktop|AppData)[\\/]")),
    ("Unix user path", re.compile(r"/(?:Users|home)/[^\s/]+")),
    ("email address", re.compile(r"(?i)(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}\b")),
    ("OpenAI-style token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("private key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
]
LINK_RE = re.compile(r"\[[^\]]+\]\((<[^>]*>|[^\s)]*)(?:\s+[^)]*)?\)")


def iter_files(root: Path):
    """Honor Git ignores for scratch files, but scan tracked output directories."""
    git_listing = True
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
            check=True,
            capture_output=True,
            text=False,
        )
        paths = [root / item for item in result.stdout.decode("utf-8").split("\0") if item]
    except (OSError, subprocess.SubprocessError):
        git_listing = False
        paths = list(root.rglob("*"))
    for path in paths:
        if not path.is_file() or not (
            path.suffix.lower() in TEXT_SUFFIXES
            or path.name == ".env" or path.name.startswith(".env.")
        ):
            continue
        if not git_listing and any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path == root / "scripts" / "check_public_repo.py":
            continue
        yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_privacy(root: Path, errors: list[str]) -> None:
    for path in iter_files(root):
        try:
            content = read_text(path)
        except UnicodeDecodeError as exc:
            errors.append(f"{path.relative_to(root)}: not valid UTF-8 ({exc})")
            continue
        for label, pattern in SENSITIVE_PATTERNS:
            match = pattern.search(content)
            if match:
                line = content.count("\n", 0, match.start()) + 1
                errors.append(f"{path.relative_to(root)}:{line}: possible {label}")


def check_markdown_links(root: Path, errors: list[str]) -> None:
    for path in iter_files(root):
        if path.suffix.lower() != ".md":
            continue
        content = read_text(path)
        for raw_target in LINK_RE.findall(content):
            target = raw_target.strip("<>")
            if (
                not target
                or target.startswith(("http://", "https://", "mailto:", "#", "data:"))
            ):
                continue
            target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes repository: {raw_target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: missing link target: {raw_target}")


def check_metadata(root: Path, errors: list[str]) -> None:
    skill = root / "SKILL.md"
    if not skill.exists():
        errors.append("SKILL.md is missing")
    else:
        lines = read_text(skill).splitlines()
        if not lines or lines[0].strip() != "---":
            errors.append("SKILL.md must start with YAML frontmatter")
        elif "---" not in lines[1:]:
            errors.append("SKILL.md frontmatter needs a closing ---")
        else:
            # Project format: one field per line; metadata uses a JSON object.
            # This is a YAML subset, not a general YAML parser.
            fields = {}
            allowed = {"name", "description", "license", "allowed-tools", "metadata"}
            for line in lines[1 : lines[1:].index("---") + 1]:
                if not line.strip() or line.startswith("#"):
                    continue
                match = re.fullmatch(r"([a-z-]+):[ \t]*(.*)", line)
                if not match:
                    errors.append("SKILL.md: use one top-level field per line")
                    continue
                key, value = match.groups()
                if key not in allowed or key in fields:
                    errors.append(f"SKILL.md: unsupported or duplicate field: {key}")
                fields[key] = None
                value = value.strip()
                try:
                    if key == "metadata" or value.startswith('"'):
                        value = json.loads(value)
                    elif value.startswith("'"):
                        if not re.fullmatch(r"'(?:[^']|'')*'", value):
                            raise ValueError("invalid single-quoted string")
                        value = value[1:-1].replace("''", "'")
                    elif (
                        not value or not re.match(r"[A-Za-z]", value)
                        or re.search(r":\s|\s#", value)
                        or value.lower() in {"null", "true", "false", "yes", "no", "on", "off"}
                    ):
                        raise ValueError("use a single-line plain or quoted string")
                    if key == "metadata":
                        if not isinstance(value, dict) or any(not isinstance(v, str) for v in value.values()):
                            raise ValueError("metadata must be a JSON object of strings")
                    elif not isinstance(value, str) or not value.strip():
                        raise ValueError("value must be a non-empty string")
                    fields[key] = value
                except ValueError as exc:
                    errors.append(f"SKILL.md: invalid {key}: {exc}")
            if "name" not in fields or (fields["name"] is not None and fields["name"] != "codex-research"):
                errors.append("SKILL.md frontmatter must declare name: codex-research")
            description = fields.get("description")
            if "description" not in fields:
                errors.append("SKILL.md frontmatter needs a description")
            elif isinstance(description, str) and not 1 <= len(description.strip()) <= 1024:
                errors.append(f"SKILL.md description must contain 1-1024 characters (got {len(description.strip())})")

    for relative in ("evals/evals.json", "evals/trigger-evals.json"):
        path = root / relative
        try:
            data = json.loads(read_text(path))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"{relative}: invalid JSON ({exc})")
            continue
        if not isinstance(data, list):
            errors.append(f"{relative}: top-level value must be an array")
        elif any(not isinstance(item, dict) for item in data):
            errors.append(f"{relative}: each record must be an object")
        elif relative == "evals/trigger-evals.json":
            for index, item in enumerate(data, 1):
                if not isinstance(item.get("query"), str) or not item["query"].strip():
                    errors.append(f"{relative}: record {index} needs a non-empty string query")
                if not isinstance(item.get("should_trigger"), bool):
                    errors.append(f"{relative}: record {index} needs a boolean should_trigger")

    rubric = root / "evals/rubric.md"
    if not rubric.is_file():
        errors.append("evals/rubric.md is missing")
    else:
        rubric_text = read_text(rubric)
        for relative in ("evals/evals.json",):
            try:
                cases = json.loads(read_text(root / relative))
            except (OSError, json.JSONDecodeError):
                continue
            for case in cases if isinstance(cases, list) else []:
                if not isinstance(case, dict):
                    continue
                for check in case.get("checks", []):
                    if f"### `{check}`" not in rubric_text:
                        errors.append(f"evals/rubric.md: missing definition for check {check}")
                for fixture in case.get("files", []):
                    if not isinstance(fixture, str):
                        errors.append("evals/evals.json: fixture path must be a string")
                        continue
                    target = (root / "evals" / fixture).resolve()
                    if not target.is_relative_to((root / "evals").resolve()) or not target.is_file():
                        errors.append(f"evals/evals.json: missing or unsafe fixture: {fixture}")

    try:
        version = read_text(root / "VERSION").strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            errors.append("VERSION must contain a semantic release version")
        if f"**Current version: `v{version}`**" not in read_text(root / "README.md"):
            errors.append("README.md version disagrees with VERSION")
        if not re.search(rf"(?m)^## v{re.escape(version)} — \d{{4}}-\d{{2}}-\d{{2}}$", read_text(root / "CHANGELOG.md")):
            errors.append("CHANGELOG.md is missing the dated current release")
    except OSError as exc:
        errors.append(f"release metadata missing: {exc.filename}")


def check_consent_contract(root: Path, errors: list[str]) -> None:
    """Catch drift between the three user-facing MCP consent descriptions."""
    required = {
        "SKILL.md": (
            "Ask whether the user wants Codex to install or configure",
            "Wait for the user's answer",
            "If the user declines, stop this MCP-dependent research path",
            "temporary files created by the attempted installation",
            "verify it with a real harmless tool call",
        ),
        "README.md": (
            "Ask the user whether they want Codex to install or configure",
            "Wait for the user's answer",
            "If the user declines, stop the MCP-dependent path",
            "temporary files created by the attempted setup",
            "verify it with a real harmless tool call",
        ),
        "references/search-strategy.md": (
            "Ask whether the user wants Codex to install or configure",
            "wait for the answer",
            "If the user declines, stop this MCP-dependent path",
            "temporary files created by the attempted setup",
            "verify with one harmless real tool call",
        ),
    }
    for relative, phrases in required.items():
        path = root / relative
        if not path.exists():
            errors.append(f"{relative}: missing consent contract document")
            continue
        content = read_text(path)
        for phrase in phrases:
            if phrase not in content:
                errors.append(f"{relative}: consent contract missing: {phrase}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    for check in (check_privacy, check_markdown_links, check_metadata, check_consent_contract):
        try:
            check(root, errors)
        except (OSError, UnicodeError) as exc:
            errors.append(f"{check.__name__}: unable to read repository content ({exc})")
    if errors:
        print("PUBLIC_REPO_CHECK_FAILED")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print("PUBLIC_REPO_CHECK_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
