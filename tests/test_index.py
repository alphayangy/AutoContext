#!/usr/bin/env python3
"""
Tests for AutoContext tooling.

Run with: python3 -m pytest tests/ -v
Or: python3 tests/test_index.py
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDELINES = ROOT / "guidelines"


def test_index_json_exists():
    assert (GUIDELINES / "index.json").exists(), "guidelines/index.json is missing"


def test_index_yaml_exists():
    assert (GUIDELINES / "index.yaml").exists(), "guidelines/index.yaml is missing"


def test_index_matches_atoms():
    """Every atom file must be represented in the index, and vice versa."""
    index = json.loads((GUIDELINES / "index.json").read_text(encoding="utf-8"))
    indexed_names = {atom["name"] for atom in index["atoms"]}

    atom_files = set()
    for path in GUIDELINES.rglob("*.md"):
        if path.name in ("index.md",):
            continue
        name = path.stem
        if name.endswith(".zh"):
            name = name[:-3]
        atom_files.add(name)

    missing_in_index = atom_files - indexed_names
    extra_in_index = indexed_names - atom_files

    assert not missing_in_index, f"Atom files missing from index: {missing_in_index}"
    assert not extra_in_index, f"Index entries without atom files: {extra_in_index}"


def test_index_required_fields():
    """Every index entry must have required metadata."""
    index = json.loads((GUIDELINES / "index.json").read_text(encoding="utf-8"))
    for atom in index["atoms"]:
        assert atom.get("name"), "Atom missing name"
        assert atom.get("profiles"), f"Atom {atom['name']} missing profiles"
        assert atom.get("priority"), f"Atom {atom['name']} missing priority"
        assert atom.get("path"), f"Atom {atom['name']} missing path"
        assert (GUIDELINES / atom["path"]).exists(), f"Atom {atom['name']} path does not exist"


def test_render_atoms_en():
    """English rendering should work using the index."""
    result = subprocess.run(
        [
            sys.executable,
            "tools/render-atoms.py",
            "--working-standard", "read-before-editing",
            "--output", "/tmp/test-render-en.md",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"render-atoms.py failed: {result.stderr}"
    output = Path("/tmp/test-render-en.md").read_text(encoding="utf-8")
    assert "[read-before-editing]" in output


def test_render_atoms_zh():
    """Chinese rendering should work using the index."""
    result = subprocess.run(
        [
            sys.executable,
            "tools/render-atoms.py",
            "--working-standard", "read-before-editing",
            "--lang", "zh",
            "--output", "/tmp/test-render-zh.md",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"render-atoms.py --lang zh failed: {result.stderr}"
    output = Path("/tmp/test-render-zh.md").read_text(encoding="utf-8")
    assert "[read-before-editing]" in output
    assert "This is working if" not in output


if __name__ == "__main__":
    test_index_json_exists()
    test_index_yaml_exists()
    test_index_matches_atoms()
    test_index_required_fields()
    test_render_atoms_en()
    test_render_atoms_zh()
    print("All tests passed.")
