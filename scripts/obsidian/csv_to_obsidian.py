#!/usr/bin/env python3
"""Convert awesome-claude-code CSV to Obsidian markdown notes.

Usage:
    python scripts/obsidian/csv_to_obsidian.py --vault-path "/path/to/Hearst/Claude Code"

If --vault-path is not provided, notes are written to ./obsidian_export/
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CSV_PATH = REPO_ROOT / "THE_RESOURCES_TABLE.csv"

CATEGORY_FOLDERS: dict[str, str] = {
    "Agent Skills": "Agent Skills",
    "Workflows & Knowledge Guides": "Workflows",
    "Tooling": "Tooling",
    "Status Lines": "Status Lines",
    "Hooks": "Hooks",
    "Slash-Commands": "Slash-Commands",
    "CLAUDE.md Files": "CLAUDE.md Files",
    "Alternative Clients": "Alternative Clients",
    "Official Documentation": "Official Documentation",
}


def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "", name).strip()


def build_note(row: dict[str, str]) -> str:
    lines: list[str] = [
        "---",
        f"id: {row['ID']}",
        f"category: \"{row['Category']}\"",
        f"subcategory: \"{row.get('Sub-Category', 'General')}\"",
        f"author: \"{row['Author Name']}\"",
        f"license: \"{row.get('License', 'Unknown')}\"",
        f"date_added: \"{row.get('Date Added', '')}\"",
        f"active: {row.get('Active', 'TRUE')}",
        "tags:",
        "  - claude-code",
        f"  - {row['Category'].lower().replace(' ', '-').replace('&', 'and')}",
    ]
    sub = row.get("Sub-Category", "")
    if sub and sub != "General":
        lines.append(f"  - {sub.lower().replace(' ', '-').replace('&', 'and')}")
    lines.extend(["---", ""])

    lines.extend([
        f"# {row['Display Name']}",
        "",
        f"> {row['Description']}",
        "",
        f"- **Primary Link**: [{row['Primary Link']}]({row['Primary Link']})",
    ])
    if row.get("Secondary Link"):
        lines.append(
            f"- **Secondary Link**: [{row['Secondary Link']}]({row['Secondary Link']})"
        )
    lines.extend([
        f"- **Author**: [{row['Author Name']}]({row.get('Author Link', '')})",
        f"- **License**: {row.get('License', 'Unknown')}",
        f"- **Added**: {row.get('Date Added', 'N/A')}",
    ])
    if row.get("Latest Release"):
        ver = row.get("Release Version", "N/A")
        lines.append(f"- **Latest Release**: {ver} ({row['Latest Release']})")

    lines.extend([
        "",
        "## Notes",
        "",
        "_Add your personal notes, use cases, and integration ideas here._",
        "",
        "## Status",
        "",
        "- [ ] Reviewed",
        "- [ ] Installed / Downloaded",
        "- [ ] Integrated into workflow",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vault-path",
        type=Path,
        default=REPO_ROOT / "obsidian_export",
        help="Root folder inside your Obsidian vault for Claude Code notes",
    )
    args = parser.parse_args()
    vault: Path = args.vault_path

    created = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row.get("Category", "Uncategorized")
            folder = CATEGORY_FOLDERS.get(category, category)
            sub = row.get("Sub-Category", "General")

            dest = vault / folder
            if sub and sub != "General":
                dest = dest / sanitize_filename(sub)
            dest.mkdir(parents=True, exist_ok=True)

            filename = sanitize_filename(row["Display Name"]) + ".md"
            (dest / filename).write_text(build_note(row), encoding="utf-8")
            created += 1

    index = build_index(vault)
    (vault / "_Index.md").write_text(index, encoding="utf-8")

    print(f"Created {created} resource notes + _Index.md in {vault}")


def build_index(vault: Path) -> str:
    return """\
# Claude Code Resources Index

> Auto-generated from [awesome-claude-code](https://github.com/mccartmc21-del/awesome-claude-code).

## All Resources by Category

```dataview
TABLE author, license, active
FROM "Claude Code"
WHERE id
GROUP BY category
SORT category ASC
```

## Recently Added

```dataview
TABLE category, author
FROM "Claude Code"
WHERE id
SORT date_added DESC
LIMIT 20
```

## Reviewed Resources

```dataview
LIST
FROM "Claude Code"
WHERE contains(file.tasks.text, "Reviewed") AND file.tasks.completed
SORT category ASC
```
"""


if __name__ == "__main__":
    main()
