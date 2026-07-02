#!/usr/bin/env python3
"""Copy skills into plugin bundles, or check that the copies are in sync.

Skills live once under skills/. Plugins bundle a subset. We copy rather than symlink so the
bundles work on Windows. Run without arguments to sync; run with --check to fail on drift
(used in CI). Stdlib only.
"""

from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

# Which skills each plugin bundles.
PLUGIN_SKILLS: dict[str, list[str]] = {
    "kapitan-core": [
        "kapitan-inventory-model",
        "kapitan-secrets-refs",
        "kapitan-debugging-compile",
    ],
    "kapitan-generators": [
        "kapitan-kubernetes-generator",
        "kapitan-terraform-generator",
        "kapitan-writing-kadet",
        "kapitan-project-scaffolding",
    ],
}

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
PLUGINS = ROOT / "plugins"


def _trees_differ(a: Path, b: Path) -> bool:
    if not b.exists():
        return True
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return True
    return any(_trees_differ(a / sub, b / sub) for sub in cmp.common_dirs)


def sync(check: bool) -> int:
    problems: list[str] = []
    for plugin, skills in PLUGIN_SKILLS.items():
        for skill in skills:
            src = SKILLS / skill
            dst = PLUGINS / plugin / "skills" / skill
            if not src.is_dir():
                problems.append(f"missing source skill: {skill}")
                continue
            if check:
                if _trees_differ(src, dst):
                    problems.append(f"drift: plugins/{plugin}/skills/{skill} != skills/{skill}")
            else:
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)

    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1
    print("plugins in sync" if check else "plugins synced")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync(check="--check" in sys.argv))
