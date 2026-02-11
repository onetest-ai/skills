#!/usr/bin/env python3
"""Validate SKILL.md files — frontmatter, semver, security checks."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


REQUIRED_FIELDS = {"name", "version", "author", "description", "tags"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")

# Dangerous patterns to detect in skill body
DANGEROUS_PATTERNS = [
    (r"\brm\s+-rf\b", "rm -rf command"),
    (r"\bcurl\b.*\|\s*\bbash\b", "curl piped to bash"),
    (r"\bwget\b.*\|\s*\bbash\b", "wget piped to bash"),
    (r"\beval\s*\(", "eval() call"),
    (r"\bexec\s*\(", "exec() call"),
    (r"\b__import__\s*\(", "__import__() call"),
    (r"\bos\.system\s*\(", "os.system() call"),
    (r"\bsubprocess\.call\s*\(.*shell\s*=\s*True", "subprocess with shell=True"),
]


def validate_skill(skill_md: Path) -> list[str]:
    """Validate a single SKILL.md. Returns list of error messages."""
    errors: list[str] = []

    if not skill_md.exists():
        return [f"File not found: {skill_md}"]

    text = skill_md.read_text(encoding="utf-8")

    # --- Frontmatter parsing ---
    if not text.startswith("---"):
        return [f"{skill_md}: Missing YAML frontmatter (must start with ---)"]

    parts = text.split("---", 2)
    if len(parts) < 3:
        return [f"{skill_md}: Malformed frontmatter (missing closing ---)"]

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        return [f"{skill_md}: YAML parse error: {e}"]

    # --- Required fields ---
    missing = REQUIRED_FIELDS - set(meta.keys())
    if missing:
        errors.append(f"Missing required fields: {', '.join(sorted(missing))}")

    # --- Name validation ---
    name = meta.get("name", "")
    if name and not NAME_RE.match(name):
        errors.append(f"Invalid name '{name}': must be lowercase alphanumeric with dashes")

    # Check name matches directory
    dir_name = skill_md.parent.name
    if name and name != dir_name:
        errors.append(f"Name '{name}' doesn't match directory '{dir_name}'")

    # --- Version validation ---
    version = meta.get("version", "")
    if version and not SEMVER_RE.match(str(version)):
        errors.append(f"Invalid version '{version}': must be semver (e.g., 1.0.0)")

    # --- Description length ---
    desc = meta.get("description", "")
    if len(desc) > 120:
        errors.append(f"Description too long ({len(desc)} chars, max 120)")

    # --- Tags ---
    tags = meta.get("tags", [])
    if not isinstance(tags, list) or len(tags) < 1:
        errors.append("Must have at least 1 tag")

    # --- Security checks on body ---
    body = parts[2] if len(parts) > 2 else ""
    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE):
            errors.append(f"Security warning: {description} detected in skill body")

    return errors


def main() -> int:
    """Validate skill files passed as arguments, or all skills in skills/."""
    paths = sys.argv[1:]

    if not paths:
        # Validate all skills
        skills_dir = Path(__file__).resolve().parent.parent / "skills"
        if skills_dir.is_dir():
            paths = [str(d / "SKILL.md") for d in sorted(skills_dir.iterdir()) if (d / "SKILL.md").is_file()]

    if not paths:
        print("No SKILL.md files found to validate.")
        return 0

    total_errors = 0
    for path_str in paths:
        path = Path(path_str)
        errors = validate_skill(path)
        if errors:
            print(f"\n{path}:")
            for e in errors:
                print(f"  ERROR: {e}")
            total_errors += len(errors)
        else:
            print(f"  {path.parent.name}: OK")

    if total_errors:
        print(f"\n{total_errors} error(s) found.")
        return 1

    print(f"\nAll {len(paths)} skills validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
