#!/usr/bin/env python3
"""Validate skill packages: frontmatter, description length, and reference links.

Stdlib only. Exits non-zero on the first batch of problems, printing each. Run from the
repo root or pass a skills directory.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_LINK = re.compile(r"\]\((references/[^)]+)\)")
_MAX_DESCRIPTION = 1024


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = _FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    key = None
    for line in match.group(1).splitlines():
        if re.match(r"^\w[\w-]*:", line):
            key, _, value = line.partition(":")
            key = key.strip()
            fields[key] = value.strip()
        elif key and line.strip():
            fields[key] += " " + line.strip()
    return fields


def validate_skill(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    text = skill_md.read_text()
    fields = _parse_frontmatter(text)

    if not fields.get("name"):
        problems.append(f"{skill_dir.name}: frontmatter missing 'name'")
    elif fields["name"] != skill_dir.name:
        problems.append(f"{skill_dir.name}: name '{fields['name']}' does not match directory")

    description = fields.get("description", "").strip("> ").strip()
    if not description:
        problems.append(f"{skill_dir.name}: frontmatter missing 'description'")
    elif len(description) > _MAX_DESCRIPTION:
        problems.append(f"{skill_dir.name}: description {len(description)} > {_MAX_DESCRIPTION} chars")

    for rel in _LINK.findall(text):
        if not (skill_dir / rel).exists():
            problems.append(f"{skill_dir.name}: broken reference link {rel}")

    return problems


def main(argv: list[str]) -> int:
    skills_root = Path(argv[1]) if len(argv) > 1 else Path("skills")
    if not skills_root.is_dir():
        print(f"no skills directory at {skills_root}", file=sys.stderr)
        return 1

    all_problems: list[str] = []
    skills = sorted(d for d in skills_root.iterdir() if (d / "SKILL.md").exists())
    for skill_dir in skills:
        all_problems.extend(validate_skill(skill_dir))

    if all_problems:
        for p in all_problems:
            print(f"FAIL {p}")
        return 1

    print(f"ok: {len(skills)} skills valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
