"""Check the pinned paper-search-mcp revision without installing or running it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


LOCK_PATH = Path("references/mcp-compatibility.json")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def load_lock(root: Path) -> dict:
    path = root / LOCK_PATH
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
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
    if data["connector"] != "paper-search-mcp":
        raise ValueError("lock file connector must be paper-search-mcp")
    if not SHA_RE.fullmatch(data["tracked_commit"]):
        raise ValueError("tracked_commit must be a 40-character lowercase commit SHA")
    if not isinstance(data["expected_capabilities"], list) or not data["expected_capabilities"]:
        raise ValueError("expected_capabilities must be a non-empty list")
    if not isinstance(data["safety_constraints"], list) or not data["safety_constraints"]:
        raise ValueError("safety_constraints must be a non-empty list")
    return data


def upstream_sha(repository: str, tracked_ref: str) -> str:
    match = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?", repository)
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
