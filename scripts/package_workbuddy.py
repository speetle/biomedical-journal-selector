#!/usr/bin/env python3
"""Build a WorkBuddy-compatible ZIP while keeping canonical SKILL.md portable."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import tempfile
import zipfile
from pathlib import Path


WORKBUDDY_FIELDS = """display_name: 生物医学智能择刊
display_name_en: Biomedical Journal Selector
description_zh: 基于论文质量、期刊适配、动态核验和三阶段录用概率，为生物医学稿件制定可解释的投稿梯队。
description_en: Evaluate biomedical manuscripts and build an evidence-checked journal submission ladder with fit, attainability, value, and three-stage acceptance estimates.
category: research
version: 1.0.0
author: Lianbin
"""


def workbuddy_skill(source: str) -> str:
    marker = "name: biomedical-journal-selector\n"
    if marker not in source:
        raise ValueError("Canonical SKILL.md has an unexpected name or frontmatter")
    converted = source.replace(marker, marker + WORKBUDDY_FIELDS, 1)
    converted = converted.replace(
        'license: MIT\nmetadata:\n  version: "1.0.0"\n  author: "Lianbin"\n',
        "",
        1,
    )
    return converted


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    output = (root / args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / "biomedical-journal-selector-workbuddy.zip"
    checksum = output / "SHA256SUMS"

    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        (stage / "SKILL.md").write_text(
            workbuddy_skill((root / "SKILL.md").read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        for directory in ("references", "scripts", "agents"):
            shutil.copytree(root / directory, stage / directory)
        shutil.copy2(root / "LICENSE", stage / "LICENSE")

        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(stage.rglob("*")):
                if path.is_file() and path.name != "package_workbuddy.py":
                    bundle.write(path, path.relative_to(stage))

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(archive)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

