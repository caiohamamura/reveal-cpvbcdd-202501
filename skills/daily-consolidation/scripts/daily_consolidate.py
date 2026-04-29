#!/usr/bin/env python3
"""
Daily Consolidation Script
Consolidates all memory/dreaming fragments for a given date into a single daily summary.
Usage: python3 daily_consolidate.py [YYYY-MM-DD]
       python3 daily_consolidate.py --latest  (uses most recent date with fragments)
"""

import re
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
SUMMARIES_DIR = MEMORY_DIR / "summaries" / "daily"
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)


def find_target_date(date_arg: Optional[str] = None) -> str:
    """Determine target date from argument or find most recent."""
    if date_arg and re.match(r"\d{4}-\d{2}-\d{2}", date_arg):
        return date_arg
    
    # Find most recent daily memory file
    files = list(MEMORY_DIR.glob("????-??-??.md"))
    files = [f for f in files if f.name not in ("TEMPLATE.md", "heartbeat-state.json")]
    if not files:
        raise ValueError("No daily memory files found")
    
    most_recent = sorted(f.name for f in files)[-1]
    return most_recent.replace(".md", "")


def find_fragment_files(date: str) -> dict:
    """Find all fragment files for a given date."""
    fragments = {}
    
    # Daily log
    daily_file = MEMORY_DIR / f"{date}.md"
    fragments["daily"] = daily_file if daily_file.exists() else None
    
    # Dream files
    for phase in ("light", "deep", "rem"):
        dream_file = MEMORY_DIR / "dreaming" / phase / f"{date}.md"
        fragments[f"dream_{phase}"] = dream_file if dream_file.exists() else None
    
    return fragments


def read_fragments(fragments: dict) -> dict:
    """Read all fragment contents."""
    contents = {}
    for key, path in fragments.items():
        if path and path.exists():
            try:
                contents[key] = path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                contents[key] = f"[Error reading {path}: {e}]"
        else:
            contents[key] = None
    return contents


def extract_sessions(content: str) -> list:
    """Extract session markers from content."""
    sessions = []
    for line in content.split("\n"):
        if re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}|UTC|session|chat|message|from:", line.lower()):
            # Try to extract timestamp
            match = re.search(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2})", line)
            if match:
                sessions.append(match.group(1)[:16])
            elif "session" in line.lower() or "chat" in line.lower():
                sessions.append(line.strip()[:80])
    return sessions[:10]  # Limit to 10


def generate_summary(date: str, fragments: dict, contents: dict) -> str:
    """Generate the daily summary markdown."""
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Collect all non-None sources
    sources = []
    for key, path in fragments.items():
        if path and path.exists():
            sources.append(str(path).replace(str(WORKSPACE) + "/", ""))
    
    lines = []
    lines.append("---")
    lines.append(f"type: daily-summary")
    lines.append(f"date: {date}")
    lines.append(f"sources:")
    for s in sources:
        lines.append(f"  - {s}")
    lines.append(f"consolidatedAt: {now}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Resumo Diário — {date}")
    lines.append("")
    lines.append("## Visão Geral")
    lines.append("[Síntese do dia em 1-2 frases]")
    lines.append("")
    lines.append("## Sessões")
    
    # Extract sessions from all contents
    all_sessions = []
    for key, content in contents.items():
        if content:
            sessions = extract_sessions(content)
            all_sessions.extend(sessions)
    
    if all_sessions:
        for s in all_sessions[:5]:
            lines.append(f"- {s}")
    else:
        lines.append("- [sem dados de sessão disponíveis]")
    lines.append("")
    lines.append("## Decisões")
    lines.append("- [Decisão se houver, senão escrever 'Nenhuma decisão registrada']")
    lines.append("")
    lines.append("## Fatos Técnicos")
    lines.append("- [Fato técnico relevante, se houver]")
    lines.append("")
    lines.append("## Lições Aprendidas")
    lines.append("- [Lição, se houver]")
    lines.append("")
    lines.append("## Síntese dos Sonhos")
    
    dream_summaries = []
    for phase in ("light", "deep", "rem"):
        content = contents.get(f"dream_{phase}")
        if content and len(content) > 50:
            dream_summaries.append(f"**{phase}**: [{len(content)} caracteres de conteúdo]")
    
    if dream_summaries:
        for d in dream_summaries:
            lines.append(f"- {d}")
    else:
        lines.append("- Sem sonhos registrados para este dia")
    lines.append("")
    lines.append("## Ações")
    lines.append("### Concluídas")
    lines.append("- [Ação concluída, se houver]")
    lines.append("")
    lines.append("### Pendentes")
    lines.append("- [ ] [Ação pendente, se houver]")
    lines.append("")
    lines.append("## Notas")
    lines.append("[Outras observações significativas]")
    
    return "\n".join(lines)


def run_daily_consolidation(date_arg: Optional[str] = None, verbose: bool = False) -> dict:
    """Run daily consolidation. Returns summary dict."""
    try:
        date = find_target_date(date_arg)
    except ValueError as e:
        return {"status": "error", "message": str(e)}
    
    if verbose:
        print(f"Consolidating date: {date}")
    
    fragments = find_fragment_files(date)
    contents = read_fragments(fragments)
    
    summary = generate_summary(date, fragments, contents)
    
    output_path = SUMMARIES_DIR / f"{date}.md"
    output_path.write_text(summary, encoding="utf-8")
    
    sources_found = sum(1 for c in contents.values() if c)
    
    if verbose:
        print(f"Saved to: {output_path}")
        print(f"Sources consolidated: {sources_found}")
    
    return {
        "status": "success",
        "date": date,
        "output": str(output_path),
        "sources_consolidated": sources_found,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Consolidate daily memory fragments into summary")
    parser.add_argument("date", nargs="?", default=None, help="Target date (YYYY-MM-DD), defaults to most recent")
    parser.add_argument("--latest", action="store_true", help="Use latest available date")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    result = run_daily_consolidation(args.date, args.verbose)
    print(f"Status: {result['status']}")
    if result["status"] == "success":
        print(f"  Date: {result['date']}")
        print(f"  Output: {result['output']}")
        print(f"  Sources: {result['sources_consolidated']}")
    else:
        print(f"  Error: {result.get('message', 'unknown')}")
        sys.exit(1)