#!/usr/bin/env python3
"""Install agent skills into a non-Claude client's skills directory.

Claude Code users get the skills through the ``kapitan-core`` / ``kapitan-generators``
plugins. Everyone else (Cursor, Codex, Kiro, ...) loads Agent Skills from a directory; this
copies the chosen ``skills/<name>/`` packages there. Copy, not symlink, so it works on
Windows and survives the source checkout moving. Stdlib only; run from a repo checkout.

    scripts/install_skills.py --list
    scripts/install_skills.py ~/.config/agent/skills                # all skills
    scripts/install_skills.py ~/.config/agent/skills --category core
    scripts/install_skills.py ./.skills kapitan-inventory-model kapitan-secrets-refs
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_CATEGORY = re.compile(r"^category:\s*(\S+)\s*$", re.MULTILINE)


def _category(skill_dir: Path) -> str:
    match = _FRONTMATTER.match((skill_dir / "SKILL.md").read_text())
    if match:
        cat = _CATEGORY.search(match.group(1))
        if cat:
            return cat.group(1)
    return "uncategorized"


def _available() -> dict[str, str]:
    return {d.name: _category(d) for d in sorted(SKILLS.iterdir()) if (d / "SKILL.md").exists()}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dest", nargs="?", help="directory the client loads skills from")
    parser.add_argument("names", nargs="*", help="skills to install (default: all)")
    parser.add_argument("--category", help="only install skills in this category")
    parser.add_argument("--list", action="store_true", help="list skills and exit")
    args = parser.parse_args(argv[1:])

    available = _available()

    if args.list:
        for name, cat in available.items():
            print(f"{name}  [{cat}]")
        return 0

    if not args.dest:
        parser.error("dest directory is required (or pass --list)")

    selected = args.names or list(available)
    unknown = [n for n in selected if n not in available]
    if unknown:
        print(f"unknown skills: {', '.join(unknown)}", file=sys.stderr)
        return 1
    if args.category:
        selected = [n for n in selected if available[n] == args.category]
        if not selected:
            print(f"no skills in category '{args.category}'", file=sys.stderr)
            return 1

    dest = Path(args.dest).expanduser()
    dest.mkdir(parents=True, exist_ok=True)
    for name in selected:
        target = dest / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(SKILLS / name, target)
        print(f"installed {name} -> {target}")

    print(
        "\nNext: drop a rules file into your repo so the agent follows the Kapitan "
        "guardrails:\n  rules/AGENTS.md (generic), rules/CLAUDE.md (Claude Code), "
        "or rules/cursor/kapitan.mdc (Cursor)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
