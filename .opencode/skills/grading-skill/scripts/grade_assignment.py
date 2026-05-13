#!/usr/bin/env python3
"""
Download and grade all submissions for a CPVBDD2 assignment.
Uses Moodle's downloadall action for reliable bulk download.

Usage:
    python3 grade_assignment.py <cmid> [options]

Options:
    --output-dir <dir>     Working directory (default: temp)
    --csv <file>          Save CSV output
    --dry-run             Don't submit to Moodle (default)
    --no-dry-run          Submit grades to Moodle

Examples:
    python3 grade_assignment.py 47135 --csv notas.csv
    python3 grade_assignment.py 47702 --dry-run
"""
import os
import sys
import re
import json
import zipfile
import requests
import unicodedata
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moodle_session import BASE, get_session

def normalize(s):
    """Normalize string for comparison: lowercase, no accents, no underscores."""
    return ''.join(c for c in unicodedata.normalize('NFD', s) 
                  if unicodedata.category(c) != 'Mn').lower().replace('_', ' ').replace('.', ' ')

def fuzzy_match_name(zip_norm, grading_norm):
    """Return True if names likely refer to same person.
    
    Uses word overlap after removing common words.
    Also handles prefix/suffix differences (e.g., 'Bruna' vs 'BIBruna').
    """
    STOPWORDS = {'de', 'da', 'do', 'dos', 'das', 'e', 'l', 'la', 'le', 'lo', 'a', 'o'}
    
    z_words = set(zip_norm.split()) - STOPWORDS
    g_words = set(grading_norm.split()) - STOPWORDS
    
    if not z_words or not g_words:
        return False
    
    # Check overlap
    overlap = z_words & g_words
    if len(overlap) >= 2:
        return True
    
    # Check if one name is contained in the other (for prefix/suffix cases)
    if zip_norm in grading_norm or grading_norm in zip_norm:
        return True
    
    # Check first names (handles 'Bruna' vs 'BIBruna' case)
    z_first = list(z_words)[0] if z_words else ''
    g_first = list(g_words)[0] if g_words else ''
    if z_first and g_first:
        # Allow one to contain the other as prefix
        if z_first.startswith(g_first) or g_first.startswith(z_first):
            return True
    
    return False

def get_assignment_title(cmid):
    """Get the assignment title from the course module page."""
    s = get_session()
    r = s.get(f"{BASE}/mod/assign/view.php?id={cmid}")
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    
    title = soup.select_one('h1') or soup.select_one('h2')
    return title.get_text(strip=True) if title else f"Tarefa {cmid}"

# ============================================================================
# DOWNLOAD
# ============================================================================
def download_all_submissions(cmid, output_dir=None):
    """Download all submissions via Moodle's downloadall action."""
    s = get_session()
    url = f"{BASE}/mod/assign/view.php?id={cmid}&action=downloadall"
    
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix=f"subs_{cmid}_")
    
    zip_path = os.path.join(output_dir, f"all_submissions_{cmid}.zip")
    
    print(f"Baixando submissions de {cmid}...")
    r = s.get(url, stream=True)
    r.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"ZIP: {os.path.getsize(zip_path):,} bytes -> {zip_path}")
    return zip_path, output_dir

# ============================================================================
# EXTRACT
# ============================================================================
def extract_and_load(zip_path, output_dir):
    """Extract downloadall ZIP and return (extract_dir, student_data, grading_uids)."""
    extract_dir = os.path.join(output_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_dir)
    
    # Parse ZIP structure: "Nome Aluno_XXXXX_assignsubmission_file/filename"
    students = {}
    
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, extract_dir)
            
            parts = rel_path.split('/')
            if len(parts) >= 2 and '_assignsubmission_file' in parts[0]:
                folder = parts[0]
                original_name = folder.rsplit('_assignsubmission_file', 1)[0]
                # Remove trailing _XXXXX numbers
                student_key = re.sub(r'_\d+$', '', original_name)
                
                norm = normalize(student_key)
                if norm not in students:
                    students[norm] = {'files': [], 'original_name': student_key}
                
                students[norm]['files'].append({
                    'filename': file,
                    'full_path': full_path,
                    'size': os.path.getsize(full_path)
                })
    
    print(f"Extraídos: {len(students)} students, {sum(len(v['files']) for v in students.values())} arquivos")
    
    # Get all UIDs from grading page
    cmid = int(os.path.basename(zip_path).replace('all_submissions_', '').replace('.zip', ''))
    grading_uids = get_grading_uids(cmid)
    
    return extract_dir, students, grading_uids

def get_grading_uids(cmid):
    """Get student name -> user_id mapping from grading page."""
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

# ============================================================================
# READ CONTENT
# ============================================================================
def read_sql_content(file_path):
    """Read all SQL content from file or ZIP."""
    if file_path.endswith('.zip'):
        try:
            z = zipfile.ZipFile(file_path)
            sql_contents = []
            for name in z.namelist():
                if name.endswith('.sql') or name.endswith('.txt'):
                    sql_contents.append(z.read(name).decode('utf-8', errors='replace'))
            return '\n'.join(sql_contents)
        except Exception as e:
            return f"<!-- ZIP ERROR: {e} -->"
    elif file_path.endswith(('.sql', '.txt')):
        for enc in ('utf-8', 'latin-1'):
            try:
                return open(file_path, 'r', encoding=enc).read()
            except:
                pass
    return ""

# ============================================================================
# GRADING LOGIC - Materialized View (Tarefa08)
# ============================================================================
def grade_student_mv(files):
    """Grade a student's MV submission (Tarefa08)."""
    all_content = []
    for f in files:
        content = read_sql_content(f['full_path'])
        if content:
            all_content.append(content)
    
    text = ' '.join(all_content)
    
    has_table = bool(re.search(r'CREATE TABLE', text, re.IGNORECASE))
    has_insert = bool(re.search(r'INSERT INTO', text, re.IGNORECASE))
    has_mv = bool(re.search(r'CREATE MATERIALIZED VIEW', text, re.IGNORECASE))
    has_refresh = 'REFRESH' in text.upper()
    has_with_data = 'WITH DATA' in text.upper() or 'WITH NO DATA' in text.upper()
    
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

# ============================================================================
# GRADING LOGIC - Functions/Procedures (Tarefa09)
# ============================================================================
def grade_student_functions(files):
    """Grade a student's Functions/Procedures submission (Tarefa09)."""
    all_content = []
    for f in files:
        content = read_sql_content(f['full_path'])
        if content:
            all_content.append(content)
    
    text = ' '.join(all_content)
    
    has_table = bool(re.search(r'CREATE TABLE', text, re.IGNORECASE))
    has_insert = bool(re.search(r'INSERT INTO', text, re.IGNORECASE))
    has_do_block = 'DO $$' in text.upper() or 'DO$' in text.upper()
    has_function = bool(re.search(r'CREATE (OR REPLACE )?FUNCTION', text, re.IGNORECASE))
    has_procedure = bool(re.search(r'CREATE (OR REPLACE )?PROCEDURE', text, re.IGNORECASE))
    has_return = 'RETURN' in text.upper() and 'RETURN QUERY' in text.upper()
    
    if not has_function and not has_procedure:
        return 0, "Sem CREATE FUNCTION ou PROCEDURE."
    
    count = 0
    if has_table: count += 1
    if has_insert: count += 1
    if has_do_block: count += 1
    if has_function: count += 1
    if has_procedure: count += 1
    if has_return: count += 1
    
    # 6 deliverables: table, insert, DO block, function, procedure, return query
    if count >= 5:
        return 100, "Tudo completo."
    elif count >= 3:
        return 75, f"Faltam alguns componentes ({count}/6)."
    else:
        return 50, f"Muito incompleto ({count}/6)."

# ============================================================================
# MAIN
# ============================================================================
def grade_assignment(cmid, output_dir=None, csv_path=None, dry_run=True, task_type='mv'):
    """Main grading flow."""
    
    # 1. Download
    zip_path, work_dir = download_all_submissions(cmid, output_dir)
    
    # 2. Extract and load
    extract_dir, students, grading_uids = extract_and_load(zip_path, work_dir)
    
    # 3. Build results for ALL students
    all_results = []
    
    # Select grading function
    grade_fn = grade_student_mv if task_type == 'mv' else grade_student_functions
    
    # Students WITH submissions
    for norm_name, data in students.items():
        # Find UID via exact or fuzzy match
        uid = grading_uids.get(norm_name)
        
        if uid is None:
            # Try fuzzy matching against all grading names
            for gnorm, guids in grading_uids.items():
                if fuzzy_match_name(norm_name, gnorm):
                    uid = guids
                    break
        
        if uid is None:
            uid = 0  # Could not match
        
        if not data['files'] or all(f['size'] < 100 for f in data['files']):
            grade, feedback = 0, "Arquivo vazio ou inválido."
        else:
            grade, feedback = grade_fn(data['files'])
        
        all_results.append({
            'uid': uid,
            'name': data['original_name'],
            'grade': grade,
            'feedback': feedback,
            'files': [f['filename'] for f in data['files']],
            'has_submission': True
        })
    
    # Students WITHOUT submissions
    students_with_sub = set()
    for r in all_results:
        if r['uid'] != 0:
            students_with_sub.add(r['uid'])
    
    s = get_session()
    r = s.get(f"{BASE}/mod/assign/view.php?id={cmid}&action=grading")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    
    grading_names = {}
    for row in soup.select('tr'):
        cells = row.select('td')
        if len(cells) >= 2:
            name = cells[1].get_text(strip=True)
            for a in row.select('a'):
                href = a.get('href', '')
                m = re.search(r'userid=(\d+)', href)
                if m:
                    grading_names[int(m.group(1))] = name
                    break
    
    for uid, name in grading_names.items():
        if uid not in students_with_sub:
            all_results.append({
                'uid': uid,
                'name': name,
                'grade': 0,
                'feedback': "Nenhum arquivo enviado.",
                'files': [],
                'has_submission': False
            })
    
    all_results.sort(key=lambda x: x['uid'])
    
    # 4. Summary
    title = get_assignment_title(cmid)
    print(f"\n{'='*70}")
    print(f"{title} (cmid={cmid})")
    print(f"{'='*70}")
    
    total = len(all_results)
    with_sub = sum(1 for r in all_results if r['has_submission'])
    print(f"Total: {total} alunos | {with_sub} entregaram | {total - with_sub} não entregaram")
    
    # Stats
    for grade_val in [100, 75, 50, 0]:
        count = sum(1 for r in all_results if r['grade'] == grade_val)
        if count:
            print(f"  Nota {grade_val}: {count}")
    
    print()
    print(f"{'UID':<6} {'Aluno':<42} {'Nota'} Feedback")
    print("-" * 110)
    for r in all_results:
        print(f"{r['uid']:<6} {r['name']:<42} {r['grade']:<5} {r['feedback']}")
    
    # 5. CSV
    if csv_path:
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write('user_id,grade,feedback\n')
            for r in all_results:
                fb = r['feedback'].replace('"', '""')
                f.write(f'{r["uid"]},{r["grade"]},"{fb}"\n')
        print(f"\nCSV salvo: {csv_path}")
    
    if dry_run:
        print(f"\n[DRY RUN] Nenhuma nota foi enviada ao Moodle.")
        print(f"Para enviar notas, use --no-dry-run")
    
    return all_results

# ============================================================================
# CLI
# ============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Grade CPVBDD2 assignment')
    parser.add_argument('cmid', type=int, help='Course Module ID da tarefa')
    parser.add_argument('--output-dir', help='Diretório de trabalho')
    parser.add_argument('--csv', help='Caminho para CSV de saída')
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--no-dry-run', dest='dry_run', action='store_false')
    parser.add_argument('--task-type', choices=['mv', 'functions'], default='mv',
                      help='Tipo de tarefa: mv (Materialized View) ou functions (Functions/Procedures)')
    
    args = parser.parse_args()
    
    grade_assignment(
        cmid=args.cmid,
        output_dir=args.output_dir,
        csv_path=args.csv,
        dry_run=args.dry_run,
        task_type=args.task_type
    )