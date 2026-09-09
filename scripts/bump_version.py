#!/usr/bin/env python3
"""
bump_version.py — Semantic version bumper for student-ml-api

Usage:
    python scripts/bump_version.py patch   # 1.0.0 → 1.0.1
    python scripts/bump_version.py minor   # 1.0.0 → 1.1.0
    python scripts/bump_version.py major   # 1.0.0 → 2.0.0
"""

import sys
import re
import subprocess
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

ROOT         = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "VERSION"
APP_FILE     = ROOT / "app.py"
TEST_FILE    = ROOT / "tests" / "test_app.py"

# ── Helpers ───────────────────────────────────────────────────────────────────

def read_version() -> str:
    return VERSION_FILE.read_text().strip()

def bump(version: str, bump_type: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"VERSION file contains invalid semver: '{version}'")
    major, minor, patch = map(int, parts)
    match bump_type:
        case "major": major += 1; minor = 0; patch = 0
        case "minor": minor += 1; patch = 0
        case "patch": patch += 1
        case _:       raise ValueError(f"Unknown bump type: '{bump_type}'")
    return f"{major}.{minor}.{patch}"

def replace_in_file(path: Path, pattern: str, replacement: str) -> bool:
    if not path.exists():
        return False
    original = path.read_text()
    updated  = re.sub(pattern, replacement, original)
    if updated == original:
        return False
    path.write_text(updated)
    return True

def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {' '.join(cmd)}")
        print(result.stderr)
        sys.exit(1)

# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("major", "minor", "patch"):
        print("Usage: python scripts/bump_version.py [major|minor|patch]")
        sys.exit(1)

    bump_type   = sys.argv[1]
    current     = read_version()
    new_version = bump(current, bump_type)

    print(f"📦 Current version : {current}")
    print(f"🚀 New version     : {new_version}")
    print()

    # 1. VERSION file
    VERSION_FILE.write_text(new_version + "\n")
    print(f"✏️  VERSION          → {new_version}")

    # 2. app.py — update the application_version string
    changed = replace_in_file(
        APP_FILE,
        r'"application_version":\s*"[\d.]+"',
        f'"application_version": "{new_version}"',
    )
    print(f"✏️  app.py           → {'updated' if changed else 'no match found (check manually)'}")

    # 3. tests/test_app.py — update the assertion
    changed = replace_in_file(
        TEST_FILE,
        r'assert data\["application_version"\] == "[\d.]+"',
        f'assert data["application_version"] == "{new_version}"',
    )
    print(f"✏️  test_app.py      → {'updated' if changed else 'no match found (check manually)'}")

    # 4. Git commit + tag
    print()
    run(["git", "add", str(VERSION_FILE), str(APP_FILE), str(TEST_FILE)])
    run(["git", "commit", "-m", f"chore: bump version to {new_version}"])
    run(["git", "tag", "-a", f"v{new_version}", "-m", f"Release version {new_version}"])

    print(f"✅ Committed and tagged v{new_version}")
    print()
    print("👉 To publish, run:")
    print(f"   git push origin HEAD && git push origin v{new_version}")

if __name__ == "__main__":
    main()
