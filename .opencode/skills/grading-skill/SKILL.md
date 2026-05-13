---
name: grading-skill
description: "Testa scripts SQL de Banco de Dados do CPVBDD2 via SQLite (fallback) ou PostgreSQL. Use quando Caio pedir para: (1) testar SQL de uma submission, (2) executar scripts SQL no SQLite, (3) extrair ZIPs de submissions. Suporta: extração de ZIPs, identificação de grupos via MD5."
---

# CPVBDD2 Grading Skill — Teste de SQL

Testa scripts SQL do CPVBDD2 usando scraping HTTP e SQLite (fallback PostgreSQL).

## Configuração

```bash
# Token em .env (MOODLE_TOKEN)
# Atualizar quando expirar
```

## ⚠️ REGRA DE OURO

**NUNCA envie notas ao Moodle sem autorização explícita do Caio.**
O workflow é: baixar submissions → testar SQL → gerar tabela no chat → **aguardar autorização** → submeter.

## ⚠️ REGRA DE PASTA

**TODO arquivo específico de uma tarefa deve ser criado dentro de `assignments/<id>/`.**
- Submissões: `assignments/<id>/<aluno>/`
- Grupos: `assignments/<id>/groups.json`
- Resultados: `assignments/<id>/RESULTADOS.md`
- NUNCA criar arquivos soltos na raiz do workspace.

## PostgreSQL

```bash
micromamba run -n postgresql psql -h localhost -p 5432 -U openclaw -d postgres

# Criar banco temporário por grupo:
micromamba run -n postgresql psql -h localhost -p 5432 -U openclaw -d postgres -c "CREATE DATABASE temp_<hash8>;"
```

PostgreSQL 18.3 está disponível para testes de SQL. Para testes rápidos em memória, use `test_sql.py` com SQLite (fallback).

## Scripts Disponíveis

### test_sql.py — Testar SQL no SQLite

```bash
python3 .opencode/skills/grading-skill/scripts/test_sql.py \
  /path/to/script.sql
```

**O que faz:**
1. Lê o script SQL
2. Normaliza PostgreSQL-specifics para SQLite (SERIAL → INTEGER, etc.)
3. Executa no SQLite in-memory
4. Retorna output, erros e resultado

**Normalizações aplicadas:**
- `SERIAL` → `INTEGER`
- `PRIMARY KEY AUTOINCREMENT` → `PRIMARY KEY`
- `VARCHAR(n)` → `TEXT`
- Remove `DROP DATABASE`
- `CREATE OR REPLACE` preservado

### identify_groups.py — Identificar Grupos via MD5

```bash
python3 .opencode/skills/grading-skill/scripts/identify_groups.py \
  /tmp/subs_41405/
```

**O que faz:**
- Computa MD5 de todos os arquivos SQL/TXT de cada aluno
- Agrupa por MD5 — mesmo MD5 = mesmo grupo de entrega
- Detecta fraude (mesmo arquivo em grupos diferentes)

### extract_zips.py — Extrair ZIPs

```bash
python3 .opencode/skills/grading-skill/scripts/extract_zips.py \
  /tmp/subs_41405/ \
  /tmp/zip_extract/
```

**O que faz:**
- Extrai todos os ZIPs das submissions para pastas individuais
- Preserva estrutura de diretórios

### download_submissions.py — Baixar Submissions

```bash
python3 .opencode/skills/grading-skill/scripts/download_submissions.py \
  41405 \
  --output /tmp/subs_41405/
```

---

## Uso Direto (Python)

### Testar SQL em SQLite

```python
import sqlite3, re

def test_sql_sqlite(sql_content):
    """Testa SQL em SQLite. Substitui PostgreSQL-specifics."""
    sql = re.sub(r'SERIAL', 'INTEGER', sql_content)
    sql = re.sub(r'PRIMARY KEY AUTOINCREMENT', 'PRIMARY KEY', sql)
    sql = re.sub(r'DROP DATABASE[^;]+;', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'VARCHAR\(\d+\)', 'TEXT', sql)

    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')
    errors = []
    for statement in sql.split(';'):
        stmt = statement.strip()
        if not stmt:
            continue
        if stmt.startswith(('CREATE', 'INSERT', 'CREATE OR REPLACE')):
            try:
                conn.executescript(stmt + ';')
            except Exception as e:
                errors.append(str(e))
    return errors
```

### Testar SQL em PostgreSQL (se disponível)

```bash
# Setup
rm -rf /tmp/pgtest && mkdir -p /tmp/pgtest
pg_ctl initdb -D /tmp/pgtest 2>/dev/null || pg_ctl initdb -D /tmp/pgtest
pg_ctl -D /tmp/pgtest -l /tmp/pgtest.log start
createdb test

# Testar arquivo
psql test -f /tmp/arquivo.sql 2>&1

# Limpar
pg_ctl -D /tmp/pgtest stop
```

---

## Ver também

- `moodle-grading/` — skill geral de correção do Moodle
- `moodle/` — configuração base e autenticação
