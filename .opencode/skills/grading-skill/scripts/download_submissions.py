#!/usr/bin/env python3
"""
Download all submissions for a CPVBDD2 assignment via downloadall endpoint.
Always produces a ZIP with structure: StudentName_XXXX_assignsubmission_file/files

Usage:
    python3 download_submissions.py <cmid> [--output-dir <dir>]

Output:
    <output-dir>/
        all_submissions_<cmid>.zip     # Original download
        extracted/                      # Extracted files
        metadata.json                   # Student list with MD5 hashes
"""
import os, sys, re, json, zipfile, requests, unicodedata, tempfile, hashlib
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moodle_session import BASE, get_session

def normalize(s):
    """Normalize: lowercase, no accents, no underscores, no dots."""
    return ''.join(c for c in unicodedata.normalize('NFD', s) 
                  if unicodedata.category(c) != 'Mn').lower().replace('_', ' ').replace('.', ' ')

def download(cmid, output_dir=None):
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix=f"subs_{cmid}_")
    
    zip_path = os.path.join(output_dir, f"all_submissions_{cmid}.zip")
    
    print(f"Baixando cmid={cmid}...")
    s = get_session()
    r = s.get(f"{BASE}/mod/assign/view.php?id={cmid}&action=downloadall", stream=True)
    r.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    
    size = os.path.getsize(zip_path)
    print(f"ZIP: {size:,} bytes -> {zip_path}")
    
    # Extract and build metadata
    extract_dir = os.path.join(output_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_dir)
    
    # Build metadata
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
                
                # MD5 of file content
                md5 = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
                
                if norm not in students:
                    students[norm] = {'original_name': original_name, 'files': [], 'md5_set': set()}
                students[norm]['files'].append({'name': fname, 'path': full_path, 'size': os.path.getsize(full_path), 'md5': md5})
                students[norm]['md5_set'].add(md5)
    
    # Save metadata
    meta_path = os.path.join(output_dir, "metadata.json")
    meta = {}
    for norm, data in students.items():
        core_md5 = sorted(data['md5_set'])[0] if data['md5_set'] else ''
        meta[norm] = {
            'original_name': data['original_name'],
            'file_count': len(data['files']),
            'total_size': sum(f['size'] for f in data['files']),
            'md5': core_md5,
            'files': [{'name': f['name'], 'size': f['size'], 'md5': f['md5']} for f in data['files']]
        }
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    print(f"Extraídos: {len(students)} students, {sum(len(v['files']) for v in students.values())} arquivos")
    print(f"Metadata: {meta_path}")
    
    return {'zip_path': zip_path, 'extract_dir': extract_dir, 'metadata_path': meta_path, 'student_count': len(students)}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('cmid', type=int)
    parser.add_argument('--output-dir', default=None)
    args = parser.parse_args()
    
    result = download(args.cmid, args.output_dir)
    print(f"\nPronto: {result['student_count']} alunos")
    print(f"ZIP: {result['zip_path']}")
    print(f"Metadata: {result['metadata_path']}")