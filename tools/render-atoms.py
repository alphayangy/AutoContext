#!/usr/bin/env python3
"""
Deterministic atom renderer for auto-context.

Reads guideline atoms from guidelines/{section}/{name}.md and renders them
into Working Rules / Verification / Safety sections without rewriting,
compressing, or dropping expansion bullets.

Usage:
    python3 tools/render-atoms.py \
        --working-standard goal-driven-execution,read-before-editing \
        --verification ensure-runs-before-claiming-done \
        --safety no-secrets \
        --output /tmp/rules.md

The output is deterministic: the core sentence and every expansion bullet
come straight from the atom file. Only formatting whitespace is added.
"""

import argparse
import os
import re
import sys
from pathlib import Path


def find_guidelines_root() -> Path:
    """Find the guidelines directory relative to this script or cwd."""
    # 1. Same directory as this script: ../guidelines
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir.parent / "guidelines",
        Path.cwd() / "guidelines",
        Path.cwd() / ".claude" / "skills" / "auto-context" / "guidelines",
        Path.home() / ".claude" / "skills" / "auto-context" / "guidelines",
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    raise FileNotFoundError("Could not find guidelines/ directory")


def load_index(guidelines_root: Path) -> dict[str, dict]:
    """Load guidelines/index.json if present. Returns a name → atom-info map."""
    import json
    index_path = guidelines_root / "index.json"
    if not index_path.exists():
        return {}

    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
        return {atom["name"]: atom for atom in data.get("atoms", [])}
    except Exception:
        return {}


def parse_atom(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    # Split frontmatter and body
    frontmatter = {}
    body = text
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            fm_text = text[3:end].strip()
            body = text[end + 3 :].strip()
            # Parse simple key: value lines
            for line in fm_text.splitlines():
                if ":" in line and not line.strip().startswith("-"):
                    key, val = line.split(":", 1)
                    frontmatter[key.strip()] = val.strip()

    lines = body.splitlines()

    core_idx = None
    accept_idx = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # Core sentence: first bold line
        if stripped.startswith("**") and stripped.endswith("**") and core_idx is None:
            core_idx = i
            continue
        # Acceptance sentence (English or Chinese)
        if stripped.startswith(("**This is working if:**", "**准则生效的标志:**")):
            accept_idx = i
            break

    core_sentence = (
        lines[core_idx].strip().strip("*").strip() if core_idx is not None else ""
    )
    acceptance = (
        lines[accept_idx].strip().strip("*").strip() if accept_idx is not None else ""
    )

    # Expansion = everything between core and acceptance, preserving structure
    end = accept_idx if accept_idx is not None else len(lines)
    expansion_lines = []
    for line in lines[core_idx + 1 : end]:
        if line.strip():
            expansion_lines.append(line)

    return {
        "name": frontmatter.get("name", path.stem),
        "path": str(path),
        "core": core_sentence,
        "expansion": expansion_lines,
        "acceptance": acceptance,
    }


def find_atom(guidelines_root: Path, name: str, index: dict[str, dict], lang: str = "en") -> Path:
    """Find atom file by name. Prefer index.yaml if available, fallback to os.walk."""
    # Use index for fast lookup
    if name in index:
        key = "path_zh" if lang == "zh" else "path"
        rel_path = index[name].get(key)
        if rel_path:
            path = guidelines_root / rel_path
            if path.exists():
                return path
        # Fallback to English if requested language is missing
        fallback = index[name].get("path")
        if fallback:
            path = guidelines_root / fallback
            if path.exists():
                return path

    # Fallback: walk the directory
    target = f"{name}.zh.md" if lang == "zh" else f"{name}.md"
    for root, _dirs, files in os.walk(guidelines_root):
        if target in files:
            return Path(root) / target
    raise FileNotFoundError(f"Atom not found: {name} (lang={lang})")


def render_atom(atom: dict) -> str:
    lines = [f"- **{atom['core']}** `[{atom['name']}]`"]
    # Preserve original indentation/structure, but indent two spaces under the core bullet.
    for raw in atom["expansion"]:
        # Normalize tabs to spaces and strip trailing whitespace
        text = raw.rstrip().expandtabs(4)
        # If the line is already a markdown bullet, keep its relative nesting;
        # otherwise indent it as a sub-bullet.
        stripped = text.lstrip()
        if stripped.startswith(("- ", "* ")):
            # Already a bullet; indent two spaces so it nests under the core bullet.
            lines.append(f"  {text}")
        elif re.match(r"^\d+\.\s", stripped):
            # Numbered list item; indent two spaces.
            lines.append(f"  {text}")
        else:
            # Plain text (e.g. "Before modifying a file:") — treat as a sub-bullet
            # so it stays visually grouped under this rule.
            lines.append(f"  - {stripped}")
    return "\n".join(lines)


def render_section(title: str, atom_names: list[str], guidelines_root: Path, index: dict[str, dict], lang: str) -> str:
    if not atom_names:
        return ""
    out = [f"## {title}"]
    for name in atom_names:
        path = find_atom(guidelines_root, name, index, lang)
        atom = parse_atom(path)
        if not atom["core"]:
            raise ValueError(f"Atom {name} has no core sentence in {path}")
        out.append(render_atom(atom))
    return "\n\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render guideline atoms deterministically")
    parser.add_argument("--working-standard", default="", help="Comma-separated atom names")
    parser.add_argument("--verification", default="", help="Comma-separated atom names")
    parser.add_argument("--safety", default="", help="Comma-separated atom names")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--guidelines-root", help="Path to guidelines/ directory")
    parser.add_argument("--lang", default="en", choices=["en", "zh"], help="Atom language (default: en)")
    args = parser.parse_args()

    guidelines_root = Path(args.guidelines_root) if args.guidelines_root else find_guidelines_root()
    index = load_index(guidelines_root)

    def split_names(s: str) -> list[str]:
        return [x.strip() for x in s.split(",") if x.strip()]

    sections = [
        ("Working Rules", split_names(args.working_standard)),
        ("Verification", split_names(args.verification)),
        ("Safety", split_names(args.safety)),
    ]

    rendered = []
    for title, names in sections:
        section_text = render_section(title, names, guidelines_root, index, args.lang)
        if section_text:
            rendered.append(section_text)

    output = "\n\n".join(rendered)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        sys.stdout.write(output + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
