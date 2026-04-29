#!/usr/bin/env python3
"""
Memory Consolidation Script
Extracts key entries from daily memory files and generates consolidation summary.
Can be run standalone or imported as module.
"""

import re
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"


def find_daily_files(days_back: int = 7) -> list[Path]:
    """Find all daily memory files from last N days."""
    files = []
    for f in MEMORY_DIR.glob("????-??-??.md"):
        if f.name not in ("TEMPLATE.md", "heartbeat-state.json"):
            files.append(f)
    return sorted(files, key=lambda p: p.name, reverse=True)


def find_last_consolidation(mem_md: Path) -> Optional[str]:
    """Find date of last consolidation entry in MEMORY.md."""
    if not mem_md.exists():
        return None
    content = mem_md.read_text()
    matches = re.findall(r"## Consolida[cç][aã]o (\d{4}-\d{2}-\d{2})", content)
    return matches[-1] if matches else None


def extract_key_entries(content: str) -> dict:
    """Extract key information types from daily file content."""
    entries = {
        "decisoes": [],
        "licoes": [],
        "fatos_tecnicos": [],
        "acoes_pendentes": [],
        "configuracoes": [],
        "projetos": [],
    }

    lines = content.split("\n")
    for i, line in enumerate(lines):
        # Decisions
        if re.search(r"(decis[ã]o|decidiu|alterou|mudou para|trocou por)", line.lower()):
            entries["decisoes"].append(line.strip())

        # Lessons (LIÇÃO)
        if re.search(r"li[cç][ã]o|lesson|error|mistake|bug|encontrou|problema| quebrado", line.lower()):
            entries["licoes"].append(line.strip())

        # Technical facts (API configs, tool setups, errors)
        if re.search(r"(api|config|script|install|deploy|timeout|error|bug|fix|rate limit)", line.lower()):
            entries["fatos_tecnicos"].append(line.strip())

        # Pending actions
        if re.search(r"(pendente|to[ -]do|action item|follow[ -]up|lembrete)", line.lower()):
            entries["acoes_pendentes"].append(line.strip())

        # Configurations
        if re.search(r"(configur|setup|instal|deploy|criou|created|novo)", line.lower()):
            entries["configuracoes"].append(line.strip())

        # Projects
        if re.search(r"(projeto|project|aula|planejamento|curso)", line.lower()):
            entries["projetos"].append(line.strip())

    return entries


def extract_date_from_filename(filename: str) -> str:
    """Extract YYYY-MM-DD from filename like '2026-04-20.md'."""
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return match.group(1) if match else "unknown"


def generate_consolidation_md(files: list[Path], last_consol: Optional[str]) -> str:
    """Generate consolidation section for MEMORY.md."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    sections = []
    sections.append(f"\n## Consolidação {today}\n")

    all_entries = {"decisoes": [], "licoes": [], "fatos_tecnicos": [], 
                   "acoes_pendentes": [], "configuracoes": [], "projetos": []}

    for f in files:
        date = extract_date_from_filename(f.name)
        content = f.read_text()
        entries = extract_key_entries(content)
        for k, v in entries.items():
            if v:
                for item in v:
                    if item not in all_entries[k]:
                        all_entries[k].append(f"[{date}] {item}")

    if all_entries["decisoes"]:
        sections.append("### Decisões importantes")
        for item in all_entries["decisoes"]:
            sections.append(f"- {item}")
        sections.append("")

    if all_entries["licoes"]:
        sections.append("### Lições aprendidas")
        for item in all_entries["licoes"]:
            sections.append(f"- {item}")
        sections.append("")

    if all_entries["fatos_tecnicos"]:
        sections.append("### Fatos técnicos")
        for item in all_entries["fatos_tecnicos"]:
            sections.append(f"- {item}")
        sections.append("")

    if all_entries["acoes_pendentes"]:
        sections.append("### Ações pendentes")
        for item in all_entries["acoes_pendentes"]:
            sections.append(f"- {item}")
        sections.append("")

    if all_entries["configuracoes"]:
        sections.append("### Configurações")
        for item in all_entries["configuracoes"]:
            sections.append(f"- {item}")
        sections.append("")

    if all_entries["projetos"]:
        sections.append("### Contextos de projeto")
        for item in all_entries["projetos"]:
            sections.append(f"- {item}")
        sections.append("")

    return "\n".join(sections)


def update_memory_md(consolidation_text: str) -> None:
    """Append consolidation section to MEMORY.md."""
    with open(MEMORY_FILE, "a") as f:
        f.write(consolidation_text)


def run_consolidation(days_back: int = 7, verbose: bool = False) -> dict:
    """Run full consolidation process. Returns summary dict."""
    files = find_daily_files(days_back)
    last_consol = find_last_consolidation(MEMORY_FILE)
    
    if verbose:
        print(f"Found {len(files)} daily files")
        print(f"Last consolidation: {last_consol or 'never'}")
    
    if not files:
        return {"status": "no_files", "files_processed": 0}

    consolidation_text = generate_consolidation_md(files, last_consol)
    update_memory_md(consolidation_text)

    # Count entries
    lines = consolidation_text.split("\n")
    summary = {
        "status": "success",
        "files_processed": len(files),
        "last_consolidation": last_consol,
        "today": datetime.now().strftime("%Y-%m-%d"),
        "entries_added": len([l for l in lines if l.startswith("- ")]),
    }
    
    if verbose:
        print(f"Consolidation complete: {summary}")
    
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Consolidate daily memory files into MEMORY.md")
    parser.add_argument("--days", "-d", type=int, default=7, help="Days to look back (default: 7)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    result = run_consolidation(days_back=args.days, verbose=args.verbose)
    print(f"Consolidation result: {result['status']}")
    if result["status"] == "success":
        print(f"  Files processed: {result['files_processed']}")
        print(f"  Entries added: {result['entries_added']}")
    sys.exit(0 if result["status"] == "success" else 1)