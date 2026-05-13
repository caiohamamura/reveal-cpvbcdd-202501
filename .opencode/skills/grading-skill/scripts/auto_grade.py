#!/usr/bin/env python3
"""
Auto-grade CPVBDD2 assignments by analyzing assignment description.
Detects task type and grading criteria automatically from assignment page.

Usage:
    python3 auto_grade.py <cmid> [--task-type auto|mv|functions|triggers] [--csv <file>]

Workflow:
    1. Fetch assignment page, parse title and description
    2. Detect task type from keywords
    3. Download submissions via downloadall
    4. Analyze each submission for required components
    5. Output grades to CSV (Moodle-ready)
"""
import os, sys, re, json, zipfile, requests, unicodedata, tempfile, hashlib
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moodle_session import BASE, get_session

def normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) 
                  if unicodedata.category(c) != 'Mn').lower().replace('_', ' ').replace('.', ' ')

def fuzzy_match(zip_norm, grading_norm):
    STOPWORDS = {'de', 'da', 'do', 'dos', 'das', 'e', 'l', 'la', 'le', 'lo', 'a', 'o'}
    z_words = set(zip_norm.split()) - STOPWORDS
    g_words = set(grading_norm.split()) - STOPWORDS
    if not z_words or not g_words:
        return False
    overlap = z_words & g_words
    if len(overlap) >= 2:
        return True
    if zip_norm in grading_norm or grading_norm in zip_norm:
        return True
    z_first = list(z_words)[0] if z_words else ''
    g_first = list(g_words)[0] if g_words else ''
    if z_first and g_first and (z_first.startswith(g_first) or g_first.startswith(z_first)):
        return True
    return False

# ─────────────────────────────────────────────────────────────────────────────
# DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────
def download_submissions(cmid, output_dir=None):
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix=f"subs_{cmid}_")
    zip_path = os.path.join(output_dir, f"all_submissions_{cmid}.zip")
    
    print(f"Baixando submissions {cmid}...")
    s = get_session()
    r = s.get(f"{BASE}/mod/assign/view.php?id={cmid}&action=downloadall", stream=True)
    r.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"ZIP: {os.path.getsize(zip_path):,} bytes")
    
    extract_dir = os.path.join(output_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_dir)
    
    return zip_path, extract_dir

def extract_students(extract_dir):
    students = {}
    for root, dirs, files in os.walk(extract_dir):
        for fname in files:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, extract_dir)
            parts = rel_path.split('/')
            if len(parts) >= 2 and '_assignsubmission_file' in parts[0]:
                folder = parts[0]
                original_name = re.sub(r'_\d+$', '', folder.replace('_assignsubmission_file', ''))
                norm = normalize(original_name)
                if norm not in students:
                    students[norm] = {'original_name': original_name, 'files': []}
                students[norm]['files'].append({'name': fname, 'path': full_path, 'size': os.path.getsize(full_path)})
    return students

def get_grading_uids(cmid):
    s = get_session()
    r = s.get(f"{BASE}/mod/assign/view.php?id={cmid}&action=grading")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    uids = {}
    for row in soup.select('tr'):
        cells = row.select('td')
        if len(cells) >= 2:
            name = cells[1].get_text(strip=True)
            for a in row.select('a'):
                href = a.get('href', '')
                m = re.search(r'userid=(\d+)', href)
                if m:
                    uids[normalize(name)] = int(m.group(1))
                    break
    return uids

def get_assignment_info(cmid):
    """Fetch assignment title and description."""
    s = get_session()
    r = s.get(f"{BASE}/mod/assign/view.php?id={cmid}")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.select_one('h1') or soup.select_one('h2')
    title = title.get_text(strip=True) if title else f"Tarefa {cmid}"
    
    # Get description (all text in the assignment description area)
    desc = ''
    for elem in soup.select('.submission-stats, .intro, .box, .generalbox'):
        text = elem.get_text(separator=' ', strip=True)
        if len(text) > len(desc):
            desc = text
    
    return {'title': title, 'description': desc}

# ─────────────────────────────────────────────────────────────────────────────
# CONTENT READING
# ─────────────────────────────────────────────────────────────────────────────
def read_content(file_path):
    if file_path.endswith('.zip'):
        try:
            z = zipfile.ZipFile(file_path)
            parts = []
            for name in z.namelist():
                if name.endswith(('.sql', '.txt')):
                    parts.append(z.read(name).decode('utf-8', errors='replace'))
            return '\n'.join(parts)
        except Exception as e:
            return f"<!-- ZIP ERROR: {e} -->"
    elif file_path.endswith(('.sql', '.txt')):
        for enc in ('utf-8', 'latin-1'):
            try:
                return open(file_path, 'r', encoding=enc).read()
            except:
                pass
    return ""

# ─────────────────────────────────────────────────────────────────────────────
# AUTO-DETECT TASK TYPE
# ─────────────────────────────────────────────────────────────────────────────
def detect_task_type(description, sample_content=None):
    desc_upper = description.upper()
    
    if 'MATERIALIZED VIEW' in desc_upper or 'CREATE MATERIALIZED VIEW' in desc_upper:
        return 'mv'
    if 'FUNCTION' in desc_upper and 'PROCEDURE' in desc_upper:
        return 'functions'
    if 'CREATE FUNCTION' in desc_upper:
        return 'functions'
    if 'CREATE PROCEDURE' in desc_upper:
        return 'functions'
    if 'TRIGGER' in desc_upper:
        return 'triggers'
    if 'VIEW' in desc_upper:
        return 'view'
    
    # Fallback: inspect sample submission content
    if sample_content:
        sample_upper = sample_content.upper()
        has_fn = bool(re.search(r'CREATE\s+(?:OR REPLACE\s+)?FUNCTION', sample_upper))
        has_proc = bool(re.search(r'CREATE\s+(?:OR REPLACE\s+)?PROCEDURE', sample_upper))
        has_do = bool(re.search(r'\bDO\s+\$\$', sample_upper))
        has_mv = 'CREATE MATERIALIZED VIEW' in sample_upper
        if has_mv:
            return 'mv'
        if (has_fn or has_proc or has_do):
            # Heuristic: if we see DO blocks and functions, it's functions/triggers task
            if has_do and (has_fn or has_proc):
                return 'functions'
            if has_fn and not has_proc:
                return 'functions'
            if has_proc and not has_fn:
                return 'functions'
    
    return 'unknown'

# ─────────────────────────────────────────────────────────────────────────────
# GRADING FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def grade_mv(all_text):
    """Grade Materialized View assignment."""
    has_table = bool(re.search(r'CREATE TABLE', all_text, re.IGNORECASE))
    has_insert = bool(re.search(r'INSERT INTO', all_text, re.IGNORECASE))
    has_mv = bool(re.search(r'CREATE MATERIALIZED VIEW', all_text, re.IGNORECASE))
    has_refresh = 'REFRESH' in all_text.upper()
    has_with_data = 'WITH DATA' in all_text.upper() or 'WITH NO DATA' in all_text.upper()
    
    if not has_mv:
        return 0, "Sem CREATE MATERIALIZED VIEW."
    if has_table and has_insert and has_mv and (has_refresh or has_with_data):
        return 100, "Tudo completo."
    if has_table and has_insert and has_mv:
        return 75, "MV sem REFRESH ou WITH DATA."
    missing = []
    if not has_table: missing.append('tabelas')
    if not has_insert: missing.append('dados')
    return 50, f"Faltam: {', '.join(missing)}"

def grade_functions(all_text):
    """Grade Functions/Procedures assignment."""
    has_table = bool(re.search(r'CREATE TABLE', all_text, re.IGNORECASE))
    has_insert = bool(re.search(r'INSERT INTO', all_text, re.IGNORECASE))
    has_do_block = 'DO $$' in all_text.upper() or bool(re.search(r'DO\s+\$\$', all_text, re.IGNORECASE))
    has_function = bool(re.search(r'CREATE (?:OR REPLACE )?FUNCTION', all_text, re.IGNORECASE))
    has_procedure = bool(re.search(r'CREATE (?:OR REPLACE )?PROCEDURE', all_text, re.IGNORECASE))
    has_return = 'RETURN QUERY' in all_text.upper()
    
    if not has_function and not has_procedure:
        return 0, "Sem CREATE FUNCTION ou PROCEDURE."
    
    count = sum([has_table, has_insert, has_do_block, has_function, has_procedure, has_return])
    
    if count >= 5:
        return 100, "Tudo completo."
    elif count >= 3:
        return 75, f"Faltam alguns componentes ({count}/6)."
    else:
        return 50, f"Muito incompleto ({count}/6)."

def grade_triggers(all_text):
    """Grade Triggers assignment."""
    has_table = bool(re.search(r'CREATE TABLE', all_text, re.IGNORECASE))
    has_insert = bool(re.search(r'INSERT INTO', all_text, re.IGNORECASE))
    has_trigger = bool(re.search(r'CREATE (?:OR REPLACE )?TRIGGER', all_text, re.IGNORECASE))
    has_function = bool(re.search(r'CREATE (?:OR REPLACE )?FUNCTION', all_text, re.IGNORECASE))
    has_procedure = bool(re.search(r'CREATE (?:OR REPLACE )?PROCEDURE', all_text, re.IGNORECASE))
    has_before_after = bool(re.search(r'\b(BEFORE|AFTER)\b', all_text, re.IGNORECASE))
    has_for_each_row = bool(re.search(r'FOR EACH ROW', all_text, re.IGNORECASE))
    
    if not has_trigger:
        return 0, "Sem CREATE TRIGGER."
    
    count = sum([has_table, has_insert, has_trigger, has_function, has_before_after, has_for_each_row])
    
    if count >= 5:
        return 100, "Tudo completo."
    elif count >= 3:
        return 75, f"Faltam alguns componentes ({count}/6)."
    else:
        return 50, f"Muito incompleto ({count}/6)."

GRADE_FUNCTIONS = {
    'mv': grade_mv,
    'functions': grade_functions,
    'triggers': grade_triggers,
}

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def grade_assignment(cmid, task_type='auto', output_dir=None, csv_path=None, dry_run=True):
    # 1. Get assignment info
    print(f"\n{'='*70}")
    print(f"CPVBDD2 Auto-Grading")
    print(f"{'='*70}")
    
    info = get_assignment_info(cmid)
    print(f"Tarefa: {info['title']} (cmid={cmid})")
    
    # 2. Download
    zip_path, extract_dir = download_submissions(cmid, output_dir)
    
    # 3. Extract students and UIDs
    students = extract_students(extract_dir)
    grading_uids = get_grading_uids(cmid)
    
    print(f"Students in ZIP: {len(students)}")
    print(f"Students in grading page: {len(grading_uids)}")
    
    # Get a sample of actual submission content to help detect task type
    sample_content = None
    if students:
        first_student = next(iter(students.values()))
        if first_student['files']:
            sample_content = read_content(first_student['files'][0]['path'])
    
    if task_type == 'auto':
        detected = detect_task_type(info['description'], sample_content)
        print(f"Tipo detectado: {detected} (via descrição + conteúdo)")
        task_type = detected
    else:
        print(f"Tipo informado: {task_type}")
    
    grade_fn = GRADE_FUNCTIONS.get(task_type, grade_mv)
    
    # 4. Grade each
    all_results = []
    for norm_name, data in students.items():
        uid = grading_uids.get(norm_name)
        if uid is None:
            for gnorm, guids in grading_uids.items():
                if fuzzy_match(norm_name, gnorm):
                    uid = guids
                    break
        if uid is None:
            uid = 0
        
        if not data['files'] or all(f['size'] < 100 for f in data['files']):
            grade, feedback = 0, "Arquivo vazio ou inválido."
        else:
            all_content = ' '.join(read_content(f['path']) for f in data['files'])
            grade, feedback = grade_fn(all_content)
        
        all_results.append({
            'uid': uid,
            'name': data['original_name'],
            'grade': grade,
            'feedback': feedback,
            'file_count': len(data['files']),
            'has_submission': True
        })
    
    # 5. Add non-submitters
    submitted_uids = {r['uid'] for r in all_results if r['uid'] != 0}
    s = get_session()
    r = s.get(f"{BASE}/mod/assign/view.php?id={cmid}&action=grading")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    for row in soup.select('tr'):
        cells = row.select('td')
        if len(cells) >= 2:
            name = cells[1].get_text(strip=True)
            for a in row.select('a'):
                href = a.get('href', '')
                m = re.search(r'userid=(\d+)', href)
                if m:
                    uid = int(m.group(1))
                    if uid not in submitted_uids:
                        all_results.append({
                            'uid': uid,
                            'name': name,
                            'grade': 0,
                            'feedback': "Nenhum arquivo enviado.",
                            'file_count': 0,
                            'has_submission': False
                        })
                    break
    
    all_results.sort(key=lambda x: x['uid'])
    
    # 6. Summary
    total = len(all_results)
    with_sub = sum(1 for r in all_results if r['has_submission'])
    print(f"\nTotal: {total} alunos | {with_sub} entregaram | {total - with_sub} não entregaram")
    for gv in [100, 75, 50, 0]:
        cnt = sum(1 for r in all_results if r['grade'] == gv)
        if cnt:
            print(f"  Nota {gv}: {cnt}")
    
    print(f"\n{'UID':<6} {'Aluno':<42} {'Nota'} Feedback")
    print("-" * 110)
    for r in all_results:
        print(f"{r['uid']:<6} {r['name']:<42} {r['grade']:<5} {r['feedback']}")
    
    # 7. CSV
    if csv_path:
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write('user_id,grade,feedback\n')
            for r in all_results:
                fb = r['feedback'].replace('"', '""')
                f.write(f'{r["uid"]},{r["grade"]},"{fb}"\n')
        print(f"\nCSV salvo: {csv_path}")
    
    if dry_run:
        print(f"\n[DRY RUN] Use --no-dry-run para enviar ao Moodle")
    
    return all_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto-grade CPVBDD2 assignment')
    parser.add_argument('cmid', type=int)
    parser.add_argument('--task-type', choices=['auto', 'mv', 'functions', 'triggers'], default='auto')
    parser.add_argument('--output-dir', default=None)
    parser.add_argument('--csv', default=None)
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=True)
    parser.add_argument('--no-dry-run', dest='dry_run', action='store_false')
    args = parser.parse_args()
    
    grade_assignment(args.cmid, args.task_type, args.output_dir, args.csv, args.dry_run)