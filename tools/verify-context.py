#!/usr/bin/env python3
"""
Verify the relationship between CLAUDE.md and AGENTS.md.

Rules:
1. If both CLAUDE.md and AGENTS.md exist, CLAUDE.md MUST reference AGENTS.md.
2. AGENTS.md MUST NOT reference CLAUDE.md (AGENTS.md is the single source).
3. No circular references between agent context files.

Usage:
    python3 tools/verify-context.py [project_root]

Exit codes:
    0 - all checks passed
    1 - verification failed
"""

import re
import sys
from pathlib import Path


# Files that are allowed/required to reference others
PRIMARY_SOURCE = "AGENTS.md"
CLAUDE_FILE = "CLAUDE.md"

# Patterns that count as a reference to another context file
REFERENCE_PATTERNS = {
    "AGENTS.md": re.compile(r"@AGENTS\.md|AGENTS\.md", re.IGNORECASE),
    "CLAUDE.md": re.compile(r"@CLAUDE\.md|CLAUDE\.md", re.IGNORECASE),
}


def find_context_files(root: Path) -> dict[str, Path]:
    """Find AGENTS.md and CLAUDE.md in the project root."""
    files = {}
    for name in (PRIMARY_SOURCE, CLAUDE_FILE):
        path = root / name
        if path.exists() and path.is_file():
            files[name] = path
    return files


def check_reference(file_path: Path, target_name: str) -> bool:
    """Check if file_path contains a reference to target_name."""
    text = file_path.read_text(encoding="utf-8")
    pattern = REFERENCE_PATTERNS[target_name]
    return bool(pattern.search(text))


def verify(root: Path) -> list[str]:
    """Run verification checks and return a list of error messages."""
    errors: list[str] = []
    files = find_context_files(root)

    has_agents = PRIMARY_SOURCE in files
    has_claude = CLAUDE_FILE in files

    if has_agents and has_claude:
        # Rule 1: CLAUDE.md must reference AGENTS.md
        if not check_reference(files[CLAUDE_FILE], PRIMARY_SOURCE):
            errors.append(
                f"{CLAUDE_FILE} exists alongside {PRIMARY_SOURCE} but does not reference it. "
                f"Add '@{PRIMARY_SOURCE}' near the top of {CLAUDE_FILE}."
            )

        # Rule 2: AGENTS.md must NOT reference CLAUDE.md
        if check_reference(files[PRIMARY_SOURCE], CLAUDE_FILE):
            errors.append(
                f"{PRIMARY_SOURCE} must be the single source and must NOT reference {CLAUDE_FILE}. "
                f"Remove any '@{CLAUDE_FILE}' or '{CLAUDE_FILE}' references from {PRIMARY_SOURCE}."
            )

    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    root = root.resolve()

    print(f"Verifying agent context files in: {root}")

    errors = verify(root)

    if not errors:
        print("✅ Context file references are valid.")
        return 0

    print("❌ Context file verification failed:")
    for err in errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
