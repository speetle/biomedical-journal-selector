#!/usr/bin/env python3
"""Validate required content and visible-text hygiene in a DOCX report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
REQUIRED_TERMS = (
    "核心结论",
    "概率总览",
    "JCR",
    "中科院分区",
    "IF",
    "OA",
    "送外审",
    "外审后接收",
    "总体接收",
    "隐私",
)
FORBIDDEN = ("*", "```", "|---")


def _border_is_visible(cell: ET.Element, edge: str) -> bool:
    border = cell.find(f"./{W}tcPr/{W}tcBorders/{W}{edge}")
    if border is None:
        return False
    value = border.get(W + "val", "")
    return value not in {"", "nil", "none"}


def _is_three_line_table(table: ET.Element) -> bool:
    rows = table.findall(f"./{W}tr")
    if len(rows) < 2:
        return False
    header_cells = rows[0].findall(f"./{W}tc")
    final_cells = rows[-1].findall(f"./{W}tc")
    if not header_cells or not final_cells:
        return False
    # 三条横线：表顶线、表头下横线、表底线。允许线条定义在单元格级别，
    # 但不把普通网格表误判为三线表。
    header_ok = all(
        _border_is_visible(cell, "top") and _border_is_visible(cell, "bottom")
        for cell in header_cells
    )
    final_ok = all(_border_is_visible(cell, "bottom") for cell in final_cells)
    no_verticals = all(
        not _border_is_visible(cell, edge)
        for cell in table.iter(W + "tc")
        for edge in ("left", "right", "insideV")
    )
    return header_ok and final_ok and no_verticals


def inspect_document(path: Path) -> tuple[str, int, int]:
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    text = "\n".join((node.text or "") for node in root.iter(W + "t"))
    tables = list(root.iter(W + "tbl"))
    three_line_count = sum(_is_three_line_table(table) for table in tables)
    return text, len(tables), three_line_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    if not args.report.is_file() or args.report.suffix.lower() != ".docx":
        print("FAIL: report must be an existing .docx file")
        return 2

    text, table_count, three_line_count = inspect_document(args.report)
    problems = []
    for term in REQUIRED_TERMS:
        if term not in text:
            problems.append(f"missing required term: {term}")
    for token in FORBIDDEN:
        if token in text:
            problems.append(f"forbidden visible token: {token}")
    if table_count < 1:
        problems.append("no Word table found")
    elif three_line_count < 1:
        problems.append("no valid three-line probability table found")

    if problems:
        print("FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(
        "PASS: required sections found; "
        f"tables={table_count}; three-line tables={three_line_count}; "
        "no forbidden tokens"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
