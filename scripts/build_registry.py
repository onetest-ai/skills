#!/usr/bin/env python3
"""Build registry.json from skills/*/SKILL.md frontmatter + git stats."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry.json"

REQUIRED_FIELDS = {"name", "version", "author", "description", "tags"}


def parse_frontmatter(skill_md: Path) -> dict | None:
    """Parse YAML frontmatter from a SKILL.md file."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None

    parts = text.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        print(f"  YAML error in {skill_md}: {e}", file=sys.stderr)
        return None

    missing = REQUIRED_FIELDS - set(meta.keys())
    if missing:
        print(f"  Missing fields in {skill_md}: {missing}", file=sys.stderr)
        return None

    return meta


def get_git_stats(skill_path: Path) -> dict:
    """Calculate git-based stats for a skill directory."""
    rel_path = str(skill_path.relative_to(Path(__file__).resolve().parent.parent))
    stats = {
        "commits": 0,
        "contributors": 0,
        "created": "",
        "last_updated": "",
    }

    try:
        # Commit count
        result = subprocess.run(
            ["git", "log", "--oneline", "--follow", "--", rel_path],
            capture_output=True, text=True, cwd=SKILLS_DIR.parent,
        )
        commits = [l for l in result.stdout.strip().split("\n") if l]
        stats["commits"] = len(commits)

        # Contributor count
        result = subprocess.run(
            ["git", "log", "--format=%aN", "--follow", "--", rel_path],
            capture_output=True, text=True, cwd=SKILLS_DIR.parent,
        )
        authors = {a for a in result.stdout.strip().split("\n") if a}
        stats["contributors"] = len(authors)

        # Created date (first commit)
        result = subprocess.run(
            ["git", "log", "--format=%aI", "--follow", "--diff-filter=A", "--", rel_path],
            capture_output=True, text=True, cwd=SKILLS_DIR.parent,
        )
        dates = result.stdout.strip().split("\n")
        if dates and dates[-1]:
            stats["created"] = dates[-1][:10]  # YYYY-MM-DD

        # Last updated (most recent commit)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--follow", "--", rel_path],
            capture_output=True, text=True, cwd=SKILLS_DIR.parent,
        )
        if result.stdout.strip():
            stats["last_updated"] = result.stdout.strip()[:10]

    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return stats


def build_registry() -> None:
    """Scan skills/ and build registry.json."""
    registry: list[dict] = []

    if not SKILLS_DIR.is_dir():
        print("No skills/ directory found.", file=sys.stderr)
        sys.exit(1)

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            print(f"  Skipping {skill_dir.name}: no SKILL.md", file=sys.stderr)
            continue

        print(f"  Processing {skill_dir.name}...")
        meta = parse_frontmatter(skill_md)
        if meta is None:
            continue

        stats = get_git_stats(skill_dir)

        # Collect additional files in the skill directory
        files = []
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file():
                files.append(str(f.relative_to(skill_dir)))

        entry = {
            "name": meta["name"],
            "version": meta["version"],
            "author": meta["author"],
            "description": meta["description"],
            "tags": meta.get("tags", []),
            "model_invocation": meta.get("model-invocation", True),
            "dependencies": meta.get("dependencies", {}),
            "requires": meta.get("requires", []),
            "permissions": meta.get("permissions", {}),
            "files": files,
            "stats": stats,
            "download_url": f"https://raw.githubusercontent.com/onetest-ai/skills/main/skills/{meta['name']}/SKILL.md",
        }
        registry.append(entry)

    REGISTRY_PATH.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nBuilt registry with {len(registry)} skills → {REGISTRY_PATH}")


if __name__ == "__main__":
    build_registry()
