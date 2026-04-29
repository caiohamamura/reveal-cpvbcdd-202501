#!/usr/bin/env python3
"""
Weekly Consolidation Script
Consolidates 7 daily summaries into one weekly summary and ingests it into the wiki vault.
Usage: python3 weekly_consolidate.py [YYYY-WNN]
       python3 weekly_consolidate.py --latest   (detects current week)
       python3 weekly_consolidate.py --prev     (previous week)
"""

import re
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
SUMMARIES_DIR = WORKSPACE / "memory" / "summaries"
WEEKLY_DIR = SUMMARIES_DIR / "weekly"
WEEKLY_DIR.mkdir(parents=True, exist_ok=True)


def get_week_bounds(week_str: str) -> tuple[str, str]:
    """Parse YYYY-WNN into (start_date, end_date) Mon-Sun."""
    match = re.match(r"(\d{4})-W(\d{2})", week_str)
    if not match:
        raise ValueError(f"Invalid week format: {week_str} (expected YYYY-WNN)")
    
    year, week = int(match.group(1)), int(match.group(2))
    
    # Find Jan 4 of that year (always in week 1)
    jan4 = datetime(year, 1, 4)
    # Find Monday of that week
    monday = jan4 + timedelta(weeks=week - 1, days=-jan4.weekday())
    sunday = monday + timedelta(days=6)
    
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def get_week_from_date(date: datetime) -> str:
    """Get YYYY-WNN from a datetime."""
    return date.strftime("%G-W%V")


def find_target_week(week_arg: Optional[str] = None, prev: bool = False) -> str:
    """Determine target week from argument or detect current."""
    if week_arg and re.match(r"\d{4}-W\d{2}", week_arg):
        return week_arg
    
    today = datetime.utcnow()
    if prev:
        # Go back one week
        target = today - timedelta(weeks=1)
    else:
        target = today
    
    return get_week_from_date(target)


def list_daily_summaries(start_date: str, end_date: str) -> list[Path]:
    """List all daily summary files within the date range."""
    daily_dir = SUMMARIES_DIR / "daily"
    if not daily_dir.exists():
        return []
    
    summaries = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        summary_file = daily_dir / f"{date_str}.md"
        if summary_file.exists():
            summaries.append(summary_file)
        current += timedelta(days=1)
    
    return summaries


def read_summaries(summaries: list[Path]) -> list[tuple[str, str]]:
    """Read all summary files, return list of (date, content)."""
    result = []
    for f in sorted(summaries):
        date = f.stem
        content = f.read_text(encoding="utf-8", errors="replace")
        result.append((date, content))
    return result


def extract_key_themes(summaries: list) -> dict:
    """Extract key themes, decisions, lessons from summaries."""
    themes = {
        "decisions": [],
        "technical_facts": [],
        "lessons": [],
        "pending": [],
        "completed": [],
        "projects": [],
    }
    
    for date, content in summaries:
        for line in content.split("\n"):
            line_lower = line.lower()
            
            if any(kw in line_lower for kw in ["decisão", "decision", "trocou", "alterou", "mudou"]):
                if line.strip().startswith("-"):
                    themes["decisions"].append(f"[{date}] {line.strip()}")
            
            elif any(kw in line_lower for kw in ["lição", "lesson", "erro", "bug", "problema", "warning"]):
                if line.strip().startswith("-"):
                    themes["lessons"].append(f"[{date}] {line.strip()}")
            
            elif any(kw in line_lower for kw in ["tecnico", "api", "config", "script", "ferramenta"]):
                if line.strip().startswith("-"):
                    themes["technical_facts"].append(f"[{date}] {line.strip()}")
            
            elif any(kw in line_lower for kw in ["pendente", "to-do", "action", "follow-up"]):
                if line.strip().startswith("-"):
                    themes["pending"].append(f"[{date}] {line.strip()}")
            
            elif any(kw in line_lower for kw in ["conclu", "completed", "done", "finished"]):
                if line.strip().startswith("-"):
                    themes["completed"].append(f"[{date}] {line.strip()}")
            
            elif any(kw in line_lower for kw in ["projeto", "project", "iot", "aula", "planejamento"]):
                if line.strip().startswith("-"):
                    themes["projects"].append(f"[{date}] {line.strip()}")
    
    # Deduplicate
    for k in themes:
        themes[k] = themes[k][:20]  # Limit
    
    return themes


def generate_weekly_summary(week_str: str, start_date: str, end_date: str, 
                            summaries: list, themes: dict) -> str:
    """Generate the weekly summary markdown."""
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    source_files = [f"memory/summaries/daily/{s.stem}.md" for s in summaries]
    
    lines = []
    lines.append("---")
    lines.append("type: weekly-summary")
    lines.append(f"week: {week_str}")
    lines.append(f"year: {start_date[:4]}")
    lines.append(f"dateRange: {start_date} to {end_date}")
    lines.append("sources:")
    for s in source_files:
        lines.append(f"  - {s}")
    lines.append(f"consolidatedAt: {now}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Semana {week_str} ({start_date} a {end_date})")
    lines.append("")
    lines.append("## Visão Geral da Semana")
    lines.append("[Resumo de 2-3 frases sobre o que aconteceu nesta semana]")
    lines.append("")
    lines.append("## Temas Principais")
    
    # Deduplicate themes by subject (simple approach)
    seen_subjects = set()
    for theme_list in [themes["projects"], themes["decisions"], themes["technical_facts"]]:
        for item in theme_list[:5]:
            subject = item[11:50].strip()  # Get part after [date]
            if subject and subject not in seen_subjects:
                seen_subjects.add(subject)
                lines.append(f"- {subject}")
    
    if not seen_subjects:
        lines.append("- [Sem temas principais identificados]")
    lines.append("")
    lines.append("## Marcos e Conclusões")
    
    if themes["completed"]:
        for item in themes["completed"][:5]:
            lines.append(f"- ✅ {item[11:]}")
    else:
        lines.append("- Nenhuma conclusão registrada")
    lines.append("")
    lines.append("## Contrast with Long-Term Memory")
    lines.append("")
    lines.append("### Confirmações (+)")
    lines.append("- [Fato do MEMORY.md confirmado pela semana, se houver]")
    lines.append("")
    lines.append("### Contradições (~)")
    lines.append("- [Fato do MEMORY.md que a semana contradiz, se houver]")
    lines.append("")
    lines.append("### Evolusções →")
    lines.append("- [Conceito do MEMORY.md que evoluiu com a semana, se houver]")
    lines.append("")
    lines.append("### Padrões Novos ★")
    lines.append("- [Padrão observado pela primeira vez esta semana]")
    lines.append("")
    lines.append("## Ações")
    lines.append("### Concluídas")
    
    if themes["completed"]:
        for item in themes["completed"][:5]:
            lines.append(f"- {item[11:]}")
    else:
        lines.append("- Nenhuma ação concluída registrada")
    lines.append("")
    lines.append("### Pendentes")
    
    if themes["pending"]:
        for item in themes["pending"][:5]:
            lines.append(f"- [ ] {item[11:]}")
    else:
        lines.append("- Nenhuma ação pendente registrada")
    lines.append("")
    lines.append("## Notas Adicionais")
    lines.append("[Outras observações significativas]")
    
    return "\n".join(lines)


def ingest_to_wiki(weekly_path: Path, verbose: bool = False) -> dict:
    """Run openclaw wiki ingest on the weekly summary."""
    if verbose:
        print(f"Ingesting to wiki: {weekly_path}")
    
    try:
        result = subprocess.run(
            ["openclaw", "wiki", "ingest", str(weekly_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if verbose:
            print(f"  stdout: {result.stdout.strip()}")
            if result.stderr:
                print(f"  stderr: {result.stderr.strip()}")
        
        return {"status": "success" if result.returncode == 0 else "failed", 
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def run_weekly_consolidation(week_arg: Optional[str] = None, prev: bool = False,
                            ingest: bool = True, verbose: bool = False) -> dict:
    """Run weekly consolidation. Returns summary dict."""
    try:
        week_str = find_target_week(week_arg, prev)
        start_date, end_date = get_week_bounds(week_str)
    except ValueError as e:
        return {"status": "error", "message": str(e)}
    
    if verbose:
        print(f"Week: {week_str} ({start_date} to {end_date})")
    
    summaries = list_daily_summaries(start_date, end_date)
    
    if not summaries:
        return {
            "status": "no_summaries",
            "week": week_str,
            "dateRange": f"{start_date} to {end_date}",
            "message": f"No daily summaries found for {start_date} to {end_date}"
        }
    
    if verbose:
        print(f"Found {len(summaries)} daily summaries")
    
    summaries_content = read_summaries(summaries)
    themes = extract_key_themes(summaries_content)
    summary_text = generate_weekly_summary(week_str, start_date, end_date, summaries, themes)
    
    output_path = WEEKLY_DIR / f"{week_str}.md"
    output_path.write_text(summary_text, encoding="utf-8")
    
    if verbose:
        print(f"Saved to: {output_path}")
    
    result = {"status": "success", "week": week_str, "output": str(output_path),
              "daily_summaries_used": len(summaries)}
    
    if ingest:
        ingest_result = ingest_to_wiki(output_path, verbose)
        result["wiki_ingest"] = ingest_result
    
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Consolidate weekly summaries and ingest to wiki")
    parser.add_argument("week", nargs="?", default=None, help="Target week (YYYY-WNN)")
    parser.add_argument("--latest", action="store_true", help="Use current week")
    parser.add_argument("--prev", action="store_true", help="Use previous week")
    parser.add_argument("--no-ingest", action="store_true", help="Skip wiki ingestion")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    if args.latest:
        week_arg = None
        prev = False
    elif args.prev:
        week_arg = None
        prev = True
    else:
        week_arg = args.week
    
    result = run_weekly_consolidation(week_arg, prev, not args.no_ingest, args.verbose)
    
    print(f"Status: {result['status']}")
    if result["status"] == "success":
        print(f"  Week: {result['week']}")
        print(f"  Output: {result['output']}")
        print(f"  Daily summaries: {result['daily_summaries_used']}")
        if "wiki_ingest" in result:
            print(f"  Wiki ingest: {result['wiki_ingest']['status']}")
    elif result["status"] == "no_summaries":
        print(f"  {result['message']}")
    else:
        print(f"  Error: {result.get('message', 'unknown')}")
        sys.exit(1)