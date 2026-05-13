#!/usr/bin/env python3
"""
Test SQL scripts for errors.
Uses SQLite as fallback for PostgreSQL-specific syntax.

Usage:
    python3 test_sql.py <arquivo.sql>
    python3 test_sql.py --dir <pasta_com_arquivos>
"""
import sys
import os
import re
import sqlite3
from pathlib import Path


def convert_postgres_to_sqlite(sql):
    """Convert PostgreSQL-specific syntax to SQLite-compatible."""
    sql = sql.strip()
    
    # Remove CREATE DATABASE and USE statements
    sql = re.sub(r'CREATE DATABASE\s+\w+;?', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\\connect\s+\w+', '', sql, flags=re.IGNORECASE)
    
    # SERIAL -> INTEGER
    sql = re.sub(r'\bSERIAL\b', 'INTEGER', sql, flags=re.IGNORECASE)
    
    # BYTEA -> BLOB
    sql = re.sub(r'\bBYTEA\b', 'BLOB', sql, flags=re.IGNORECASE)
    
    # VARCHAR(n) -> TEXT (SQLite doesn't care about length)
    sql = re.sub(r'\bVARCHAR\(\d+\)', 'TEXT', sql, flags=re.IGNORECASE)
    
    # VARCHAR without size -> TEXT
    sql = re.sub(r'\bVARCHAR\b', 'TEXT', sql, flags=re.IGNORECASE)
    
    # TIMESTAMP -> TEXT
    sql = re.sub(r'\bTIMESTAMP\b', 'TEXT', sql, flags=re.IGNORECASE)
    
    # DATE -> TEXT
    sql = re.sub(r'\bDATE\b', 'TEXT', sql, flags=re.IGNORECASE)
    
    # BOOLEAN -> INTEGER
    sql = re.sub(r'\bBOOLEAN\b', 'INTEGER', sql, flags=re.IGNORECASE)
    
    # NUMERIC/DECIMAL -> REAL
    sql = re.sub(r'\bNUMERIC\(\d+,\d+\)', 'REAL', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bDECIMAL\(\d+,\d+\)', 'REAL', sql, flags=re.IGNORECASE)
    
    # Remove CHECK constraints (SQLite supports but can be problematic)
    # Keep them for now as SQLite handles them
    
    # SERIAL PRIMARY KEY -> INTEGER PRIMARY KEY (autoincrement)
    sql = re.sub(r'\bINTEGER\s+SERIAL\b', 'INTEGER', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bSERIAL\s+PRIMARY\s+KEY\b', 'INTEGER PRIMARY KEY', sql, flags=re.IGNORECASE)
    
    # Remove CASCADE / ON DELETE constraints that SQLite doesn't like
    sql = re.sub(r'\bON\s+(DELETE|UPDATE)\s+(CASCADE|SET NULL|RESTRICT)', '', sql, flags=re.IGNORECASE)
    
    # IF NOT EXISTS is fine in SQLite
    # IF EXISTS is fine in SQLite
    
    return sql


def test_sql_file(filepath, verbose=True):
    """Test a single SQL file in SQLite."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            sql_content = f.read()
    
    sql = convert_postgres_to_sqlite(sql_content)
    
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')
    
    errors = []
    success_stmts = []
    
    # Split by semicolon, but be careful with semicolons inside strings
    statements = []
    current = ''
    in_string = False
    string_char = None
    
    for char in sql:
        if char in ("'", '"') and (not in_string or string_char == char):
            in_string = not in_string
            if not in_string:
                string_char = None
            elif string_char is None:
                string_char = char
        if char == ';' and not in_string:
            if current.strip():
                statements.append(current.strip())
            current = ''
        else:
            current += char
    
    # Don't forget the last statement
    if current.strip():
        statements.append(current.strip())
    
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt or stmt.startswith('--'):
            continue
        
        # Skip COPY statements (PostgreSQL specific)
        if stmt.upper().startswith('COPY '):
            errors.append(f'COPY ignorado (PostgreSQL-specific): {stmt[:50]}...')
            continue
        
        try:
            conn.executescript(stmt + ';')
            success_stmts.append(stmt[:60])
        except Exception as e:
            errors.append(f'{stmt[:60]}... -> {e}')
    
    conn.close()
    
    if verbose:
        print(f"=== {os.path.basename(filepath)} ===")
        print(f"Statements executados: {len(success_stmts)}")
        print(f"Erros: {len(errors)}")
        if errors:
            print("Erros:")
            for e in errors:
                print(f"  - {e}")
        print()
    
    return {
        'file': filepath,
        'statements': len(success_stmts),
        'errors': errors,
        'success': len(errors) == 0
    }


def test_sql_dir(dirpath, verbose=True):
    """Test all SQL files in a directory."""
    results = []
    for root, dirs, files in os.walk(dirpath):
        for f in sorted(files):
            if f.endswith(('.sql', '.txt')):
                fp = os.path.join(root, f)
                result = test_sql_file(fp, verbose)
                results.append(result)
    return results


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 test_sql.py <arquivo.sql>")
        print("   ou: python3 test_sql.py --dir <pasta>")
        sys.exit(1)
    
    if sys.argv[1] == '--dir':
        if len(sys.argv) < 3:
            print("Uso: python3 test_sql.py --dir <pasta>")
            sys.exit(1)
        results = test_sql_dir(sys.argv[2])
        print(f"\nTotal: {len(results)} arquivos")
        ok = sum(1 for r in results if r['success'])
        print(f"OK: {ok}, Com erro: {len(results) - ok}")
    else:
        result = test_sql_file(sys.argv[1])
        if result['success']:
            print("✅ SQL válido")
        else:
            print("❌ SQL com erros")


if __name__ == '__main__':
    main()