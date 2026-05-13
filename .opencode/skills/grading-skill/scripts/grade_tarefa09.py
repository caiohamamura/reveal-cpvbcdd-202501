#!/usr/bin/env python3
"""
Grade Tarefa09 submissions using PostgreSQL.
Each MD5 group gets a temporary database for testing.

Usage:
    python3 grade_tarefa09.py
"""
import os
import re
import sys
import hashlib
import psycopg2
from psycopg2 import sql
from collections import defaultdict

BASE_DIR = "/home/openclaw/.openclaw/workspace/moodle/submissions_47702"
GRADING_DIR = "/home/openclaw/.openclaw/workspace/moodle/grading_47702"
os.makedirs(GRADING_DIR, exist_ok=True)

PG_CONN = {
    "host": "localhost",
    "port": 5432,
    "user": "openclaw",
    "database": "postgres"
}

# CRITICAL: plpgsql is in the micromamba postgresql env, not the default path
PLPLGSQL_LIB = "/home/openclaw/micromamba/envs/postgresql/lib"

ENTREGAVEIS = ["ddl", "doblock", "fn_out", "procedure", "resumo"]
PONTO_POR_ENTREGAVEL = 10


def get_pg_conn(db_name):
    """Get PostgreSQL connection with plpgsql library path set."""
    conn = psycopg2.connect(**{**PG_CONN, "database": db_name})
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SET dynamic_library_path = '{PLPLGSQL_LIB}'")
    cur.close()
    return conn


def create_temp_db(db_name):
    """Create a temporary database."""
    conn = psycopg2.connect(**PG_CONN)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    cur.close()
    conn.close()


def drop_temp_db(db_name):
    """Drop a temporary database."""
    try:
        conn = psycopg2.connect(**PG_CONN)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
        cur.close()
        conn.close()
    except Exception:
        pass


def get_students_by_md5():
    """Group students by content MD5."""
    results = {}
    for student in sorted(os.listdir(BASE_DIR)):
        path = os.path.join(BASE_DIR, student)
        if not os.path.isdir(path):
            continue
        md5s = []
        for f in sorted(os.listdir(path)):
            fp = os.path.join(path, f)
            if f.endswith(".sql") and os.path.isfile(fp):
                with open(fp, "rb") as fd:
                    md5 = hashlib.md5(fd.read()).hexdigest()
                    md5s.append(md5)
        results[student] = sorted(md5s)

    groups = defaultdict(list)
    for student, md5s in results.items():
        key = tuple(md5s)
        groups[key].append(student)
    return groups


def parse_deliverables(student_dir):
    """Parse all 5 deliverables for a student directory."""
    files = sorted(os.listdir(student_dir))
    results = {
        "ddl": None,
        "doblock": None,
        "fn_out": None,
        "procedure": None,
        "resumo": None
    }

    for f in files:
        if not f.endswith(".sql"):
            continue
        fp = os.path.join(student_dir, f)
        with open(fp) as fd:
            content = fd.read()

        # DDL: CREATE TABLE
        if results["ddl"] is None and re.search(r'\bCREATE\s+TABLE\b', content, re.IGNORECASE):
            results["ddl"] = content

        # DO Block: DO $$
        if results["doblock"] is None and re.search(r'\bDO\s+\$\$', content, re.IGNORECASE):
            results["doblock"] = content

        # Function with OUT
        if results["fn_out"] is None:
            if re.search(r'\bOUT\b', content) and \
               re.search(r'\bCREATE\s+(OR\s+REPLACE\s+)?FUNCTION\b', content, re.IGNORECASE):
                if re.search(r'(estatistica|categoria|stats?)', content, re.IGNORECASE):
                    results["fn_out"] = content

        # Procedure: CREATE PROCEDURE + transferir
        if results["procedure"] is None:
            if re.search(r'\bCREATE\s+(OR\s+REPLACE\s+)?PROCEDURE\b', content, re.IGNORECASE):
                if re.search(r'\btransferir\b', content, re.IGNORECASE):
                    results["procedure"] = content

        # resumo_clientes
        if results["resumo"] is None:
            if re.search(r'\bCREATE\s+(OR\s+REPLACE\s+)?FUNCTION\b', content, re.IGNORECASE):
                if re.search(r'\bresumo\b', content, re.IGNORECASE):
                    results["resumo"] = content

    return results


def test_ddl(ddl_content, db_name):
    """Create DB and test DDL. Returns (bool, msg, conn_or_None)."""
    create_temp_db(db_name)

    try:
        conn = get_pg_conn(db_name)
    except Exception as e:
        return (False, f"Connect to {db_name} failed: {e}", None)

    # Strip CREATE DATABASE and USE statements (PostgreSQL-specific)
    clean_ddl = re.sub(r'\bCREATE DATABASE\s+\w+\s*;?', '', ddl_content, flags=re.IGNORECASE)
    clean_ddl = re.sub(r'\bUSE\s+\w+\s*;?', '', clean_ddl, flags=re.IGNORECASE)
    clean_ddl = re.sub(r'\\connect\s+\w+', '', clean_ddl, flags=re.IGNORECASE)
    clean_ddl = clean_ddl.strip()

    if not clean_ddl:
        return (False, "DDL vazio apos remover CREATE DATABASE", conn)

    try:
        cur = conn.cursor()
        cur.execute(clean_ddl)
        conn.commit()

        # Verify tables
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = [r[0] for r in cur.fetchall()]
        expected = ['clientes', 'produtos', 'pedidos', 'pedidos_itens']
        missing = [t for t in expected if t not in tables]
        cur.close()

        if missing:
            return (False, f"Faltam tabelas: {missing}", conn)
        return (True, f"OK: {tables}", conn)
    except Exception as e:
        return (False, f"DDL error: {str(e).split(chr(10))[0][:100]}", conn)


def grade_group(representative, student_dir, db_name):
    """Grade a single group (one MD5). Returns (grade, feedback_dict)."""
    delivs = parse_deliverables(student_dir)
    results = {}

    # Test DDL first
    ddl_ok = False
    ddl_msg = ""
    conn_ref = [None]

    if delivs["ddl"]:
        ddl_ok, ddl_msg, conn_ref[0] = test_ddl(delivs["ddl"], db_name)
    else:
        ddl_msg = "DDL não encontrado"

    results["ddl"] = ddl_ok
    results["ddl_msg"] = ddl_msg

    if not ddl_ok:
        for k in ["doblock", "fn_out", "procedure", "resumo"]:
            results[k] = False
            results[k + "_msg"] = "Sem DDL funcional"
        conn_ref[0] = None
    else:
        # DO Block
        if delivs["doblock"]:
            try:
                cur = conn_ref[0].cursor()
                cur.execute(delivs["doblock"])
                conn_ref[0].commit()
                cur.close()
                results["doblock"] = True
                results["doblock_msg"] = "OK"
            except Exception as e:
                results["doblock"] = False
                results["doblock_msg"] = str(e).split('\n')[0][:80]
        else:
            results["doblock"] = False
            results["doblock_msg"] = "DO Block não encontrado"

        # Function OUT
        if delivs["fn_out"]:
            try:
                cur = conn_ref[0].cursor()
                cur.execute(delivs["fn_out"])
                conn_ref[0].commit()
                cur.execute("SELECT proname FROM pg_proc WHERE proname LIKE '%estatistica%' OR proname LIKE '%categoria%' LIMIT 1")
                row = cur.fetchone()
                cur.close()
                if row:
                    results["fn_out"] = True
                    results["fn_out_msg"] = f"OK ({row[0]})"
                else:
                    results["fn_out"] = False
                    results["fn_out_msg"] = "Function criada mas não encontrada no catálogo"
            except Exception as e:
                results["fn_out"] = False
                results["fn_out_msg"] = str(e).split('\n')[0][:80]
        else:
            results["fn_out"] = False
            results["fn_out_msg"] = "fn_estatisticas_categoria não encontrada"

        # Procedure
        if delivs["procedure"]:
            try:
                cur = conn_ref[0].cursor()
                cur.execute(delivs["procedure"])
                conn_ref[0].commit()
                cur.execute("SELECT proname FROM pg_proc WHERE proname LIKE '%transferir%' LIMIT 1")
                row = cur.fetchone()
                cur.close()
                if row:
                    results["procedure"] = True
                    results["procedure_msg"] = f"OK ({row[0]})"
                else:
                    results["procedure"] = False
                    results["procedure_msg"] = "Procedure criada mas não encontrada no catálogo"
            except Exception as e:
                results["procedure"] = False
                results["procedure_msg"] = str(e).split('\n')[0][:80]
        else:
            results["procedure"] = False
            results["procedure_msg"] = "sp_transferir_estoque não encontrada"

        # resumo_clientes
        if delivs["resumo"]:
            try:
                cur = conn_ref[0].cursor()
                cur.execute(delivs["resumo"])
                conn_ref[0].commit()
                cur.execute("SELECT * FROM resumo_clientes() LIMIT 1")
                _ = cur.fetchall()
                cur.close()
                results["resumo"] = True
                results["resumo_msg"] = "OK"
            except Exception as e:
                results["resumo"] = False
                results["resumo_msg"] = str(e).split('\n')[0][:80]
        else:
            results["resumo"] = False
            results["resumo_msg"] = "resumo_clientes não encontrada"

    if conn_ref[0]:
        conn_ref[0].close()

    drop_temp_db(db_name)

    # Calculate grade
    grade = 50
    for key in ENTREGAVEIS:
        if results.get(key, False):
            grade += PONTO_POR_ENTREGAVEL

    return grade, results


def main():
    groups = get_students_by_md5()
    print(f"Total: {len(groups)} grupos MD5 únicos\n")

    all_results = {}

    for i, (key, members) in enumerate(sorted(groups.items(), key=lambda x: -len(x[1]))):
        db_name = f"temp_t09_{i+1:02d}"
        rep = members[0]
        rep_dir = os.path.join(BASE_DIR, rep)

        print(f"{'='*60}")
        print(f"Grupo {i+1}: {rep}")
        print(f"Membros: {members}")
        print(f"DB: {db_name}")

        grade, results = grade_group(rep, rep_dir, db_name)

        print(f"Nota: {grade}/100")
        for k in ENTREGAVEIS:
            status = "✅" if results.get(k, False) else "❌"
            print(f"  {status} {k}: {results.get(k+'_msg', '')}")

        for m in members:
            all_results[m] = {"grade": grade, "details": results, "members": members}

    # Summary table
    print(f"\n{'='*80}")
    print("RESUMO FINAL")
    print(f"{'Aluno':<45} {'Nota':>6} | Entregáveis")
    print("-"*80)
    for student, data in sorted(all_results.items()):
        g = data["grade"]
        d = data["details"]
        parts = [k for k in ENTREGAVEIS if d.get(k, False)]
        print(f"{student:<45} {g:>6} | {', '.join(parts)}")

    import json
    out_path = os.path.join(GRADING_DIR, "RESULTADOS.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\nSalvo em: {out_path}")


if __name__ == "__main__":
    main()
