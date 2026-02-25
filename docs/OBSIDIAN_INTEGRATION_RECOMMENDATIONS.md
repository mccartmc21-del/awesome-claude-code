# Obsidian Integration Recommendations

## What This Repo Is

**awesome-claude-code** is a community-curated directory of 200+ resources for enhancing Claude Code workflows. It catalogs:

| Category | Count (approx.) | What It Covers |
|---|---|---|
| Agent Skills | ~18 | Model-controlled configs that give Claude specialized capabilities (DevOps, security auditing, full-stack dev, project management) |
| Workflows & Knowledge Guides | ~40 | End-to-end development methodologies, documentation mirrors, spec-driven workflows |
| Tooling | ~40 | Apps built on Claude Code — IDE integrations, usage monitors, orchestrators, config managers |
| Status Lines | ~10 | Terminal status bar customizations |
| Hooks | ~15 | Lifecycle event handlers (pre-commit, post-tool, notification systems) |
| Slash-Commands | ~50 | Custom prompts for Git, code analysis, testing, CI/CD, documentation, task management |
| CLAUDE.md Files | ~20 | Project-specific instruction files (language-specific, domain-specific, scaffolding) |
| Alternative Clients | ~10 | Mobile/desktop UIs for Claude Code |
| Official Documentation | ~10 | Anthropic's own Claude Code docs and GitHub Actions |

The repo also includes a full automation pipeline: Python scripts for README generation, link validation, GitHub issue-based submission workflows, repo health monitoring, and ticker/stats tracking.

---

## Recommended Approach: Obsidian Vault Integration

### Vault Structure

Inside your Obsidian vault `Hearst` (Google Drive, `michael.mccarthy@hearst.com`), create the following folder structure:

```
Hearst/
├── Claude Code/
│   ├── _Index.md                    ← Master index (generated from this repo)
│   ├── _Quick Reference.md          ← Your personal cheat sheet
│   ├── Agent Skills/
│   │   ├── AgentSys.md
│   │   ├── cc-devops-skills.md
│   │   ├── Context Engineering Kit.md
│   │   ├── Everything Claude Code.md
│   │   ├── Fullstack Dev Skills.md
│   │   ├── Superpowers.md
│   │   ├── Trail of Bits Security.md
│   │   └── ...
│   ├── Workflows/
│   │   ├── AB Method.md
│   │   ├── Agentic Workflow Patterns.md
│   │   ├── Claude Code Ultimate Guide.md
│   │   ├── Claude CodePro.md
│   │   └── ...
│   ├── Tooling/
│   │   ├── IDE Integrations/
│   │   ├── Usage Monitors/
│   │   ├── Orchestrators/
│   │   └── General/
│   ├── Slash-Commands/
│   │   ├── Git & Version Control/
│   │   ├── Code Analysis & Testing/
│   │   ├── Documentation/
│   │   ├── CI & Deployment/
│   │   └── General/
│   ├── Hooks/
│   ├── CLAUDE.md Files/
│   │   ├── Language-Specific/
│   │   ├── Domain-Specific/
│   │   └── Scaffolding/
│   ├── Templates/
│   │   ├── slash-command-template.md
│   │   ├── hook-template.md
│   │   └── CLAUDE.md-template.md
│   └── My Customizations/
│       ├── hearst-CLAUDE.md          ← Your org-specific CLAUDE.md
│       ├── hearst-slash-commands/
│       └── notes/
```

### Step-by-Step Integration

#### 1. Set Up Obsidian-Git Sync (Recommended)

Since your vault lives in Google Drive, you have two sync options:

**Option A — Google Drive native sync (simplest)**
- Your Obsidian vault on Google Drive already syncs across devices
- Manually or script the export from this repo into the vault folder
- Downside: no version control on the vault itself

**Option B — Obsidian Git plugin + this repo (recommended)**
- Install the [Obsidian Git](https://github.com/Vinzent03/obsidian-git) community plugin
- Clone this repo into a subfolder of your vault, or symlink it
- The plugin auto-commits and pushes changes on a schedule
- You get both Google Drive sync AND git history

#### 2. Convert the Resource CSV to Obsidian Notes

The single source of truth is `THE_RESOURCES_TABLE.csv`. Each row can become an Obsidian note. Here is a Python script you can run to generate them:

```python
#!/usr/bin/env python3
"""Convert awesome-claude-code CSV to Obsidian markdown notes."""

import csv
import os
import re
from pathlib import Path

VAULT_BASE = Path.home() / "Google Drive" / "Hearst" / "Claude Code"
CSV_PATH = Path("THE_RESOURCES_TABLE.csv")

CATEGORY_FOLDERS = {
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
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def make_note(row: dict) -> str:
    frontmatter = [
        "---",
        f"id: {row['ID']}",
        f"category: {row['Category']}",
        f"subcategory: {row['Sub-Category']}",
        f"author: {row['Author Name']}",
        f"license: {row['License']}",
        f"date_added: {row['Date Added']}",
        f"active: {row['Active']}",
        f"tags:",
        f"  - claude-code",
        f"  - {row['Category'].lower().replace(' ', '-')}",
    ]
    if row.get('Sub-Category'):
        frontmatter.append(f"  - {row['Sub-Category'].lower().replace(' ', '-')}")
    frontmatter.append("---")
    frontmatter.append("")

    body = [
        f"# {row['Display Name']}",
        "",
        f"> {row['Description']}",
        "",
        f"- **Primary Link**: [{row['Primary Link']}]({row['Primary Link']})",
    ]
    if row.get('Secondary Link'):
        body.append(f"- **Secondary Link**: [{row['Secondary Link']}]({row['Secondary Link']})")
    body.extend([
        f"- **Author**: [{row['Author Name']}]({row['Author Link']})",
        f"- **License**: {row['License']}",
        f"- **Added**: {row['Date Added']}",
    ])
    if row.get('Latest Release'):
        body.append(f"- **Latest Release**: {row.get('Release Version', 'N/A')} ({row['Latest Release']})")

    body.extend([
        "",
        "## Notes",
        "",
        "_Add your personal notes, use cases, and integration ideas here._",
        "",
        "## Status",
        "",
        f"- [ ] Reviewed",
        f"- [ ] Installed / Downloaded",
        f"- [ ] Integrated into workflow",
    ])

    return "\n".join(frontmatter + body) + "\n"

def main():
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row.get("Category", "Uncategorized")
            folder = CATEGORY_FOLDERS.get(category, category)
            subcategory = row.get("Sub-Category", "General")

            dest_dir = VAULT_BASE / folder
            if subcategory and subcategory != "General":
                dest_dir = dest_dir / sanitize_filename(subcategory)
            dest_dir.mkdir(parents=True, exist_ok=True)

            filename = sanitize_filename(row["Display Name"]) + ".md"
            note_path = dest_dir / filename
            note_path.write_text(make_note(row))
            print(f"  Created: {note_path}")

if __name__ == "__main__":
    main()
```

#### 3. Create a Master Index Note

Create `_Index.md` in the `Claude Code/` folder with a Dataview query (requires the Dataview plugin):

```markdown
# Claude Code Resources Index

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
TABLE category, author, description
FROM "Claude Code"
WHERE id
SORT date_added DESC
LIMIT 20
```

## My Reviewed Resources

```dataview
TABLE category, author
FROM "Claude Code"
WHERE contains(file.tasks.text, "Reviewed") AND file.tasks.completed
SORT category ASC
```
```

#### 4. Create a Quick Reference Note

`_Quick Reference.md` — your personal cheat sheet:

```markdown
# Claude Code Quick Reference

## High-Priority Resources to Evaluate

Based on the awesome-claude-code curation, these are the most impactful
resources to review first:

### Must-Have Agent Skills
- [[Everything Claude Code]] — Comprehensive coverage of all Claude Code features
- [[Superpowers]] — Core engineering best practices as skills
- [[cc-devops-skills]] — Essential for anyone deploying code
- [[Trail of Bits Security]] — Professional security auditing
- [[Context Engineering Kit]] — Advanced context engineering patterns

### Essential Workflows
- [[Claude Code Ultimate Guide]] — Beginner to power user
- [[Agentic Workflow Patterns]] — Architectural patterns with diagrams
- [[Claude Code System Prompts]] — Understand what's under the hood
- [[Claude Code Documentation Mirror]] — Always-current docs

### Key Tooling
- Review IDE integrations relevant to your stack
- Review orchestrators for multi-agent workflows
- Evaluate usage monitors for cost tracking

## My Active Configuration
- Current CLAUDE.md: `[[hearst-CLAUDE.md]]`
- Active hooks: _list your hooks_
- Active slash-commands: _list your commands_
```

---

## High-Value Resources to Prioritize

Based on the repository's descriptions and activity signals, here are the resources most likely to accelerate your skills:

### Tier 1 — Start Here

| Resource | Why |
|---|---|
| **Everything Claude Code** | Covers "just about everything" — standalone value per skill |
| **Superpowers** | Core engineering competencies, well-written, adaptable |
| **Claude Code Ultimate Guide** | Beginner → power user with templates and quizzes |
| **Context Engineering Kit** | Advanced techniques with minimal token footprint |
| **Claude Code System Prompts** | See exactly how Claude Code works internally |

### Tier 2 — Domain-Specific

| Resource | Why |
|---|---|
| **cc-devops-skills** | IaC code generation for major platforms |
| **Trail of Bits Security Skills** | Professional security auditing with CodeQL/Semgrep |
| **Fullstack Dev Skills** | 65 skills + Jira/Confluence integration |
| **Compound Engineering Plugin** | Turn mistakes into improvement opportunities |
| **Claude Code Documentation Mirror** | Stay current with Claude Code's expanding features |

### Tier 3 — Workflow Optimization

| Resource | Why |
|---|---|
| **Agentic Workflow Patterns** | Architectural patterns with Mermaid diagrams |
| **Claude CodePro** | Spec-driven + TDD + cross-session memory |
| **AB Method** | Spec-driven workflow with sub-agents |
| **Claude Code Tips** | 35+ quick tips covering voice, containers, multi-model |

---

## Practical Integration Steps

### Step 1: Install Obsidian Plugins

Install these community plugins in your vault:

1. **Dataview** — query your notes like a database
2. **Obsidian Git** — version control for your vault (optional but recommended)
3. **Templater** — template system for creating new resource notes
4. **Kanban** — visual board for tracking which resources you're evaluating

### Step 2: Run the CSV-to-Notes Script

Run the Python script above from the root of this repo. It generates one Obsidian note per resource with YAML frontmatter, making them queryable via Dataview.

### Step 3: Review and Tag Resources

Work through the resources, starting with Tier 1. In each note:
- Check the "Reviewed" task when you've read it
- Check "Installed / Downloaded" when you've cloned or installed it
- Check "Integrated into workflow" when it's part of your daily setup
- Add personal notes under the Notes section

### Step 4: Build Your Custom CLAUDE.md

Create `hearst-CLAUDE.md` in `My Customizations/` combining the best patterns you've found:

```markdown
# CLAUDE.md — Hearst

## Project Context
- Organization: Hearst
- Primary contact: michael.mccarthy@hearst.com

## Coding Standards
<!-- Pull from resources you've reviewed -->

## Workflow Rules
<!-- Incorporate patterns from your favorite workflows -->

## Active Skills
<!-- Reference skills you've installed -->
```

### Step 5: Set Up a Sync Workflow

To keep your Obsidian notes in sync as this repo updates:

1. Pull latest changes from this repo periodically
2. Re-run the CSV-to-Notes script (it overwrites existing notes but preserves the structure)
3. Your personal notes in the "Notes" and "Status" sections will need to be in separate files or tracked manually if you re-run the script

**Better approach**: Use the script only for initial import, then maintain notes manually and use the repo's README as a reference for new additions.

---

## Architecture Notes for Future Automation

The repo's Python scripts in `scripts/` offer patterns you could adapt:

- `scripts/resources/parse_issue_form.py` — Pattern for parsing structured submissions
- `scripts/readme/generate_readme.py` — Pattern for generating docs from CSV data
- `scripts/validation/validate_links.py` — Link checking you could run against your vault's external links
- `scripts/ticker/fetch_repo_ticker_data.py` — GitHub API integration for tracking repo stats

These could be adapted into Obsidian plugins or periodic scripts that keep your vault's resource notes fresh.
