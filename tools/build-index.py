#!/usr/bin/env python3
"""
Build guidelines/index.yaml from the atom library.

Scans guidelines/**/*.md, parses YAML frontmatter, and generates a single
index file for fast atom lookup and composition. Also performs consistency
checks and exits non-zero if the atom library is malformed.

Usage:
    python3 tools/build-index.py [--output guidelines/index.yaml]
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_yaml_value(val: str):
    """Parse a simple YAML value: string, number, boolean, or inline list."""
    val = val.strip()
    if not val:
        return ""

    # Inline list: [a, b, c]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in inner.split(","):
            item = item.strip().strip('"').strip("'")
            if item:
                items.append(item)
        return items

    # Booleans
    lower = val.lower()
    if lower in ("true", "yes"):
        return True
    if lower in ("false", "no"):
        return False

    # Null
    if lower in ("null", "~"):
        return None

    # Numbers
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        pass

    # String
    return val.strip('"').strip("'")


def parse_frontmatter(text: str) -> dict:
    """Parse simple YAML frontmatter from markdown text."""
    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    fm_text = text[3:end].strip()
    frontmatter = {}
    current_key = None
    current_obj = None

    for line in fm_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Nested list item under current key (e.g. triggers.files)
        if stripped.startswith("-") and current_key and isinstance(current_obj, dict):
            item = stripped[1:].strip().strip('"').strip("'")
            # Determine which nested list this belongs to by indentation/context
            # Heuristic: if line starts with two spaces less than key, it's a value of the last nested key
            # We keep it simple: only support one level of nesting for lists.
            pass

        # Key: value or key: object start
        if ":" in stripped and not stripped.startswith("-"):
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()

            if val == "":
                # Could be an object or list starting on next lines
                frontmatter[key] = {}
                current_key = key
                current_obj = {}
            else:
                frontmatter[key] = parse_yaml_value(val)
                current_key = None
                current_obj = None
            continue

        # Nested list item (e.g. under triggers.files)
        if stripped.startswith("-") and current_key and isinstance(frontmatter.get(current_key), dict):
            item = stripped[1:].strip().strip('"').strip("'")
            # Find which sub-key we are under by indentation - simplistic: assume current last sub-key
            pass

    return frontmatter


def parse_frontmatter_v2(text: str) -> dict:
    """
    More robust frontmatter parser supporting one level of nested lists.
    Example:
        triggers:
          files:
            - "*.sql"
            - "*.ipynb"
          user_intents:
            - data-analysis
    """
    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    fm_text = text[3:end].strip()
    result = {}
    current_top_key = None
    current_sub_key = None
    base_indent = None
    sub_indent = None

    lines = fm_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Top-level key (no leading indentation)
        if not line.startswith((" ", "\t")) and not stripped.startswith("-") and ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()

            current_top_key = key
            current_sub_key = None
            base_indent = len(line) - len(line.lstrip())

            if val == "":
                result[key] = {}
            else:
                result[key] = parse_yaml_value(val)
                current_top_key = None
            i += 1
            continue

        # Nested key under current_top_key
        if current_top_key and isinstance(result.get(current_top_key), dict) and not stripped.startswith("-") and ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()
            current_sub_key = key
            sub_indent = len(line) - len(line.lstrip())

            if val == "":
                result[current_top_key][key] = []
            else:
                result[current_top_key][key] = parse_yaml_value(val)
                current_sub_key = None
            i += 1
            continue

        # List item under current_sub_key
        if stripped.startswith("-") and current_top_key and current_sub_key:
            item = stripped[1:].strip().strip('"').strip("'")
            if isinstance(result[current_top_key].get(current_sub_key), list):
                result[current_top_key][current_sub_key].append(item)
            i += 1
            continue

        i += 1

    return result


def find_guidelines_root() -> Path:
    """Find the guidelines directory relative to this script or cwd."""
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


def build_index(guidelines_root: Path) -> dict:
    """Scan atoms and build an index dictionary."""
    atoms_by_name: dict[str, dict] = {}
    errors: list[str] = []
    warnings: list[str] = []

    for path in sorted(guidelines_root.rglob("*.md")):
        rel_path = path.relative_to(guidelines_root).as_posix()

        # Skip non-atom markdown files if any
        if path.name in ("index.md",):
            continue

        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter_v2(text)

        name = frontmatter.get("name")
        if not name:
            # Fall back to filename stem if no name in frontmatter
            name = path.stem
            # For .zh.md files, use the English base name
            if name.endswith(".zh"):
                name = name[:-3]
            warnings.append(f"{rel_path}: missing 'name' in frontmatter, using '{name}'")

        is_zh = path.name.endswith(".zh.md")
        section = path.parent.name

        if name not in atoms_by_name:
            atoms_by_name[name] = {
                "name": name,
                "description": frontmatter.get("description", ""),
                "profiles": frontmatter.get("profiles", []),
                "scopes": frontmatter.get("scopes", []),
                "priority": frontmatter.get("priority", "medium"),
                "triggers": frontmatter.get("triggers", {}),
                "conflicts": frontmatter.get("conflicts", []),
                "section": section,
                "path": None,
                "path_zh": None,
            }

        atom = atoms_by_name[name]

        # Validate section consistency
        if atom.get("section") != section:
            warnings.append(f"{rel_path}: atom '{name}' found in multiple sections")

        # Set path
        if is_zh:
            if atom["path_zh"] is not None:
                errors.append(f"{rel_path}: duplicate Chinese atom for '{name}'")
            atom["path_zh"] = rel_path
        else:
            if atom["path"] is not None:
                errors.append(f"{rel_path}: duplicate English atom for '{name}'")
            atom["path"] = rel_path

        # Merge/validate frontmatter fields from the English version as canonical
        if not is_zh:
            atom["description"] = frontmatter.get("description", atom.get("description", ""))
            atom["profiles"] = frontmatter.get("profiles", atom.get("profiles", []))
            atom["scopes"] = frontmatter.get("scopes", atom.get("scopes", []))
            atom["priority"] = frontmatter.get("priority", atom.get("priority", "medium"))
            atom["triggers"] = frontmatter.get("triggers", atom.get("triggers", {}))
            atom["conflicts"] = frontmatter.get("conflicts", atom.get("conflicts", []))

    # Post-validation
    for name, atom in atoms_by_name.items():
        if atom["path"] is None:
            errors.append(f"Atom '{name}' has no English version")
        if atom["path_zh"] is None:
            warnings.append(f"Atom '{name}' has no Chinese version")
        if not atom.get("description"):
            warnings.append(f"Atom '{name}' missing description")
        if not atom.get("profiles"):
            errors.append(f"Atom '{name}' missing profiles")
        if not atom.get("priority"):
            errors.append(f"Atom '{name}' missing priority")
        if not atom.get("scopes"):
            warnings.append(f"Atom '{name}' missing scopes")

    if warnings:
        print("Warnings:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)

    if errors:
        print("Errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        raise SystemExit(1)

    return {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(atoms_by_name),
        "atoms": list(atoms_by_name.values()),
    }


def write_yaml(index: dict, output_path: Path) -> None:
    """Write the index as a simple YAML file without external dependencies."""
    lines = []
    lines.append(f"version: {index['version']}")
    lines.append(f"generated_at: \"{index['generated_at']}\"")
    lines.append(f"count: {index['count']}")
    lines.append("atoms:")

    for atom in index["atoms"]:
        lines.append("  - name: " + _yaml_str(atom["name"]))
        lines.append("    description: " + _yaml_str(atom.get("description", "")))
        lines.append("    profiles: " + _yaml_list(atom.get("profiles", [])))
        lines.append("    scopes: " + _yaml_list(atom.get("scopes", [])))
        lines.append("    priority: " + _yaml_str(atom.get("priority", "medium")))
        lines.append("    triggers: " + _yaml_dict(atom.get("triggers", {})))
        lines.append("    conflicts: " + _yaml_list(atom.get("conflicts", [])))
        lines.append("    section: " + _yaml_str(atom.get("section", "")))
        lines.append("    path: " + _yaml_str(atom.get("path", "")))
        lines.append("    path_zh: " + _yaml_str(atom.get("path_zh", "")))

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _yaml_str(val: str) -> str:
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    # Quote strings that contain special YAML characters
    if re.search(r'[:\[\]{}#&*!|>\'"%@`,]', val) or val.startswith(("-", " ")) or val == "":
        escaped = val.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return val


def _yaml_list(items: list) -> str:
    if not items:
        return "[]"
    return "[" + ", ".join(_yaml_str(str(x)) for x in items) + "]"


def _yaml_dict(d: dict) -> str:
    if not d:
        return "{}"
    # Support one level of nested lists
    parts = []
    for k, v in d.items():
        if isinstance(v, list):
            parts.append(f"{k}: {_yaml_list(v)}")
        elif isinstance(v, dict):
            parts.append(f"{k}: {_yaml_dict(v)}")
        else:
            parts.append(f"{k}: {_yaml_str(str(v))}")
    return "{ " + ", ".join(parts) + " }"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build guidelines/index.yaml and index.json from atom library")
    parser.add_argument(
        "--output",
        "-o",
        default="guidelines/index.yaml",
        help="Output YAML index file path (default: guidelines/index.yaml)",
    )
    args = parser.parse_args()

    guidelines_root = find_guidelines_root()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = guidelines_root.parent / output_path

    print(f"Scanning atoms in: {guidelines_root}")
    index = build_index(guidelines_root)
    print(f"Found {index['count']} atoms")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(index, output_path)
    print(f"Wrote YAML index to: {output_path}")

    # Also write a JSON version for stdlib-only consumers (e.g. render-atoms.py)
    json_path = output_path.with_suffix(".json")
    import json
    json_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote JSON index to: {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
