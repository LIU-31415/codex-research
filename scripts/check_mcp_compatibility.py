"""Check the pinned paper-search-mcp revision without installing or running it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


LOCK_PATH = Path("evals/mcp-compatibility.json")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"https://github\.com/([^/\s?#]+)/([^/\s?#]+?)(?:\.git)?/?")


def load_lock(root: Path) -> dict:
    path = root / LOCK_PATH
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("lock file must contain a JSON object")
    required = {
        "connector",
        "repository",
        "tracked_ref",
        "tracked_commit",
        "checked_at",
        "review_policy",
        "expected_capabilities",
        "safety_constraints",
    }
    missing = required - data.keys()
    if missing:
        raise ValueError(f"lock file missing fields: {', '.join(sorted(missing))}")
    for field in sorted(required - {"expected_capabilities", "safety_constraints"}):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    if data["connector"] != "paper-search-mcp":
        raise ValueError("lock file connector must be paper-search-mcp")
    if not REPOSITORY_RE.fullmatch(data["repository"]):
        raise ValueError("repository must be an HTTPS GitHub repository URL")
    if not SHA_RE.fullmatch(data["tracked_commit"]):
        raise ValueError("tracked_commit must be a 40-character lowercase commit SHA")
    for field in ("expected_capabilities", "safety_constraints"):
        if not isinstance(data[field], list) or not data[field] or any(
            not isinstance(value, str) or not value.strip() for value in data[field]
        ):
            raise ValueError(f"{field} must be a non-empty list of non-empty strings")
    return data


def upstream_sha(repository: str, tracked_ref: str) -> str:
    match = REPOSITORY_RE.fullmatch(repository)
    if not match:
        raise ValueError("repository must be an HTTPS GitHub repository URL")
    owner, name = match.groups()
    endpoint = f"https://api.github.com/repos/{owner}/{name}/commits/{tracked_ref}"
    request = Request(endpoint, headers={"Accept": "application/vnd.github+json", "User-Agent": "codex-research-compatibility-check"})
    with urlopen(request, timeout=20) as response:
        payload = json.load(response)
    sha = payload.get("sha")
    if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
        raise ValueError("GitHub API response did not contain a commit SHA")
    return sha


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--online", action="store_true", help="query GitHub for the tracked ref")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        lock = load_lock(root)
        if not args.online:
            print(f"MCP_COMPATIBILITY_LOCK_OK {lock['tracked_ref']} {lock['tracked_commit']}")
            return 0
        current = upstream_sha(lock["repository"], lock["tracked_ref"])
    except (OSError, json.JSONDecodeError, ValueError, HTTPError, URLError, TimeoutError) as exc:
        print(f"MCP_COMPATIBILITY_CHECK_FAILED: {exc}")
        return 3

    if current != lock["tracked_commit"]:
        print(
            "UPSTREAM_CHANGED: "
            f"{lock['repository']}#{lock['tracked_ref']} is now {current}; "
            "review capabilities and safety before updating the lock."
        )
        return 2
    print(f"MCP_COMPATIBILITY_OK {lock['tracked_ref']} {current}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
