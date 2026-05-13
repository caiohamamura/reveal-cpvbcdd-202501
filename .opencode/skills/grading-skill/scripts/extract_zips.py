#!/usr/bin/env python3
"""
Extract all ZIP files from submissions directory.

Usage:
    python3 extract_zips.py <submissions_dir> [output_dir]

Output structure:
    output_dir/
        StudentName/
            file1.sql
            file2.sql
            ...
"""
import sys
import os
import zipfile
import shutil

def extract_zips(base_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    extracted = []
    for student in os.listdir(base_dir):
        sp = os.path.join(base_dir, student)
        if not os.path.isdir(sp):
            continue
        
        student_out = os.path.join(output_dir, student)
        os.makedirs(student_out, exist_ok=True)
        
        for fname in os.listdir(sp):
            if not fname.endswith('.zip'):
                continue
            
            fpath = os.path.join(sp, fname)
            zf = zipfile.ZipFile(fpath)
            
            print(f"Extraindo {student}/{fname}...")
            zf.printdir()
            
            # Extract all files preserving structure
            for zname in zf.namelist():
                # Skip directories
                if zname.endswith('/'):
                    continue
                
                # Create directories as needed
                zparts = zname.split('/')
                if len(zparts) > 1:
                    # Has subdirectory structure
                    out_subdir = os.path.join(student_out, os.path.dirname(zname))
                    os.makedirs(out_subdir, exist_ok=True)
                
                target = os.path.join(student_out, zname)
                try:
                    with zf.open(zname) as src:
                        with open(target, 'wb') as dst:
                            shutil.copyfileobj(src, dst)
                    extracted.append((student, fname, zname, target))
                except Exception as e:
                    print(f"  Erro ao extrair {zname}: {e}")
            
            zf.close()
    
    print(f"\nTotal: {len(extracted)} arquivos extraídos")
    return extracted


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 extract_zips.py <submissions_dir> [output_dir]")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else base_dir + '_zips'
    
    extract_zips(base_dir, output_dir)