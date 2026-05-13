#!/usr/bin/env python3
"""
Identify groups by computing MD5 of all SQL/text files.
Groups = files with the same MD5 (shared submission).

Usage:
    python3 identify_groups.py <submissions_dir>
"""
import sys
import os
import json
import hashlib
from collections import defaultdict

def get_all_sql_files(base_dir):
    """Find all SQL/TXT files, including extracted from ZIPs."""
    files = {}
    for student in os.listdir(base_dir):
        sp = os.path.join(base_dir, student)
        if not os.path.isdir(sp):
            continue
        student_files = []
        for root, dirs, filenames in os.walk(sp):
            for f in filenames:
                if f.endswith(('.sql', '.txt')):
                    fp = os.path.join(root, f)
                    student_files.append(fp)
        if student_files:
            files[student] = student_files
    return files


def compute_md5(filepath):
    """Compute MD5 of a file, handling encoding issues."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def identify_groups(base_dir):
    """Return (groups_dict, unique_submissions_dict)."""
    all_files = get_all_sql_files(base_dir)
    
    # md5 -> list of (student, filepath)
    md5_map = defaultdict(list)
    # student -> md5_set (for unique identification)
    student_hashes = {}
    
    for student, filepaths in all_files.items():
        hashes = set()
        for fp in filepaths:
            md5 = compute_md5(fp)
            if md5:
                hashes.add(md5)
                md5_map[md5].append((student, os.path.basename(fp)))
        student_hashes[student] = hashes
    
    # Groups: same MD5 = same submission
    groups = {}  # md5 -> [students]
    for md5, entries in md5_map.items():
        students = list(dict.fromkeys(e[0] for e in entries))  # preserve order, unique
        groups[md5] = students
    
    # Unique submissions: one representative per group
    unique = {}  # md5 -> {student, files}
    for md5, entries in md5_map.items():
        rep_student = entries[0][0]
        rep_file = entries[0][1]
        unique[md5] = {'student': rep_student, 'file': rep_file, 'members': [e[0] for e in entries]}
    
    return groups, unique


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 identify_groups.py <submissions_dir>")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    groups, unique = identify_groups(base_dir)
    
    print("=== GRUPOS IDENTIFICADOS (mesmo MD5 = mesmo arquivo) ===\n")
    
    # Check for potential fraud (same file across different groups)
    fraud_alerts = []
    for md5, info in unique.items():
        n = len(info['members'])
        if n > 3:
            fraud_alerts.append((md5, info['members']))
            print(f"⚠️ ALERTA: {n} alunos com mesmo MD5 (possível fraude):")
            for m in info['members']:
                print(f"  - {m}")
            print()
    
    # Normal groups
    normal_groups = [(md5, info) for md5, info in unique.items() if len(info['members']) <= 3]
    
    print(f"=== GRUPOS NORMAIS ({len(normal_groups)} grupos, até 3 alunos) ===\n")
    for i, (md5, info) in enumerate(sorted(normal_groups, key=lambda x: x[1]['student']), 1):
        print(f"Grupo {i}: {info['student']} (representante)")
        for m in info['members']:
            print(f"  - {m}")
        print(f"  Arquivo: {info['file']}")
        print()
    
    # Students with no files
    all_students_with_files = set()
    for info in unique.values():
        for m in info['members']:
            all_students_with_files.add(m)
    
    metadata_path = os.path.join(base_dir, 'metadata.json')
    if os.path.exists(metadata_path):
        with open(metadata_path) as f:
            metadata = json.load(f)
        no_submission = [s['name'] for s in metadata if s['name'] not in all_students_with_files and len(s['files']) == 0]
        if no_submission:
            print(f"=== SEM SUBMISSÃO ({len(no_submission)} alunos) ===")
            for s in sorted(no_submission):
                print(f"  - {s}")
    
    # Save groups to JSON for grading script
    output_path = os.path.join(base_dir, 'groups.json')
    groups_data = {
        'normal': [{'md5': md5, **info} for md5, info in sorted(unique.items(), key=lambda x: x[1]['student'])],
        'fraud': [{'md5': md5, 'members': members} for md5, members in fraud_alerts],
        'no_submission': no_submission if os.path.exists(metadata_path) else []
    }
    with open(output_path, 'w') as f:
        json.dump(groups_data, f, indent=2, ensure_ascii=False)
    print(f"\nGrupos salvos em: {output_path}")


if __name__ == '__main__':
    main()