#!/usr/bin/env python3
"""Search the local Mao Selected Works Markdown corpus."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    frontmatter = text.split("---", 2)[1]
    data: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def iter_files(volume: str | None) -> list[Path]:
    if volume:
        root = CORPUS / f"vol-{volume}"
        return sorted(root.glob("*.md"))
    return sorted(CORPUS.glob("vol-*/*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Search local Mao Selected Works corpus.")
    parser.add_argument("query", help="Search term or phrase.")
    parser.add_argument("--volume", choices=["1", "2", "3", "4"], help="Restrict search to one volume.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of matches to print.")
    parser.add_argument("--context", type=int, default=80, help="Characters of context on each side.")
    parser.add_argument("--compact", action="store_true", help="Ignore whitespace in both query and corpus.")
    args = parser.parse_args()

    query = compact(args.query) if args.compact else args.query
    count = 0

    for path in iter_files(args.volume):
        text = strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
        haystack = compact(text) if args.compact else text
        start = 0
        while count < args.limit:
            idx = haystack.find(query, start)
            if idx == -1:
                break
            meta = metadata(path)
            left = max(0, idx - args.context)
            right = min(len(haystack), idx + len(query) + args.context)
            snippet = haystack[left:right].replace("\n", " ")
            title = meta.get("title", path.stem)
            volume = meta.get("volume", "?")
            year = meta.get("year", "?")
            print(f"{path}")
            print(f"  title: {title}")
            print(f"  volume: {volume}, year: {year}")
            print(f"  snippet: ...{snippet}...")
            print()
            count += 1
            start = idx + len(query)
        if count >= args.limit:
            break

    if count == 0:
        print("No matches found in local corpus.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

