# MEMORY.md — Long-Term Memory

## CPVCIDA — Ciencia de Dados (Curso ID 1498)

### Tarefas Corrigidas

| cmid | Atividade | Estado | Notas |
|------|-----------|--------|-------|
| 47801 | Tarefa10 (Random Forest) | CONCLUIDO | 19 alunos, 9 grupos (B-J), Grupo D = 0 (Colab privado) |
| 48221 | Tarefa11 (PCA) | CONCLUIDO | 13 alunos, 6 grupos (B-F,H), Grupo B = 50 (vazio) |
| 42401 | Tarefa03 | PENDENTE | 3 submissions, 3 para corrigir |

### Pendentes CPVCIDA

| cmid | Atividade | Estado |
|------|-----------|--------|
| 42401 | Tarefa03 | 3 envios pendentes |
| 48556 | Tarefa12 | Aberta ate 17 mai, 1 envio |

### Notas sobre correcao CPVCIDA
- Grupos B-J mapeados via pagina de participantes
- Submissions sao notebooks .ipynb (Colab ou arquivo)
- Nota = 0 se notebook privado; 50 se vazio; senao 50 + soma(deliverables * weight)
- Feedback em PT-BR, sem emojis, acionavel (o que falta para 100)

## CPVBDD2 — Banco de Dados 2 (Curso ID 1486)

### �_CURRENT_TASK: 47702 (Tarefa 09 — Blocks, Functions, Procedures)_

### Tarefas em Andamento

| cmid | Atividade | Estado | Notas |
|------|-----------|--------|-------|
| 46257 | Tarefa Views | ⚠️ PARCIAL | 5 de 6 alunos submetidos (Carlos pendente) |
| 47135 | Tarefa 08 | 📋 BAIXADO | Pendente correção |
| 47702 | Tarefa 09 (Blocks, Functions, Procedures) | 📋 RESULTADOS PRÉVIOS | Nota 50 para todos (DDL falhou) — re-testar com PostgreSQL |

---

## 📁 Estrutura de Correção — `assignments/<id>/`

**Regra:** TODO arquivo específico de tarefa vai em `assignments/<id>/`

```
assignments/
  46257/              # Tarefa Views
    correcao.json / correcao.md
    notas_46257.csv
    carlos_printes/    # prints do Carlos
    Carlos_Eduardo_Costa_Menezes/
  46599/              # Tarefa antiga
    metadata.json
  47135/              # Tarefa 08
    groups.json / metadata.json
    notas_47135.csv / notas_47135_v2.csv
    <aluno>/           # 37 pastas
  47702/              # Tarefa 09 (Blocks, Functions, Procedures)
    CRITERIO.md
    GRADING-DEEP.md
    RESULTADOS.json    # correção prévia (todos 50 — DDL falhou)
    instrucao_tarefa09.sql
    checkpoints/
    <aluno>/           # 21 pastas de alunos
```

---

## 📁 Estado Correção — Tarefa 47702 (Tarefa09)

**Pasta:** `assignments/47702/`
**Pasta submissions:** `/tmp/subs_47702_*/extracted/`

**Entregáveis (5 total, cada = 10pts):**
1. DDL + INSERT (criação banco e-commerce)
2. DO Block anônimo (RAISE NOTICE)
3. fn_estatisticas_categoria (OUT parameters)
4. sp_transferir_estoque + produtos_prateleira
5. resumo_clientes (RETURNS TABLE)

**Regra:** Nota = 50 + (entregáveis_funcionando × 50/6 ≈ 8.33)

**6 entregáveis:**
1. DDL (criação banco e-commerce)
2. INSERT (dados iniciais)
3. DO Block anônimo (RAISE NOTICE)
4. fn_estatisticas_categoria (OUT parameters)
5. sp_transferir_estoque + produtos_prateleira
6. resumo_clientes (RETURNS TABLE)

**Desconto:**
- Erro grave no código (não executa, lógica errada) → perde ponto daquele entregável
- Erro pequeno (falta de `;`, espaços, etc.) → não desconta

**Exemplos:**
- Todos 6 OK → 100
- Só DDL (INSERT com erro) → ~58
- DDL+INSERT OK, resto falho → ~67
- Tudo menos DDL → ~92

**⚠️ RESULTADOS PRÉVIOS:** Correção anterior usou SQLite — todos ficaram com 50 porque o DDL falhou ("relation does not exist"). Precisamos re-testar com **PostgreSQL** real.

**Conexão PostgreSQL:** `/home/openclaw/micromamba/envs/postgresql/bin/psql -h localhost -p 5432 -U openclaw`

**Nota:** O servidor PostgreSQL 18.3 está rodando em `/home/openclaw/test_cluster` com `plpgsql.so` configurado via `dynamic_library_path`.

---

## 📁 Estado Correção — Tarefa 46257 (Views)

**Pasta:** `assignments/46257/`
**Correção:** 5 de 6 alunos submetidos. Carlos pendente (prints de tela).

---

## 🔧 PostgreSQL

```bash
# PostgreSQL 18.3 via micromamba
micromamba run -n postgresql psql -h localhost -p 5432 -U openclaw -d postgres

# Banco temporário:
micromamba run -n postgresql psql -h localhost -p 5432 -U openclaw -c "CREATE DATABASE temp_<nome>;"
```

---

## 📝 Critérios de Correção (CPVBDD2)

**Sistema por entregáveis (50 mínimo):**
- Trabalho começa em 100, cada entregável faltando desconta 50/N pontos
- Nota mínima = 50 (para quem entregou algo válido)
- Nota 0 = não enviou nada

**Grupos:**
- Até 3 alunos por grupo
- Mesmo MD5 = mesmo grupo → mesma nota
- Fraude (mesmo MD5 em grupos diferentes) = nota 0 para todos

---

## ⚠️ Pendências

1. **Tarefa 47702:** Re-testar com PostgreSQL (correção anterior falhou com SQLite)
2. **Tarefa 46257 - Carlos:** Verificação manual de prints
3. **Tarefa 47135:** Pendente correção

---

## 🍪 Cookie Moodle (atualizado em 2026-05-02)

```
MoodleSession=h164tvdiut43o0t45340aknb29
```