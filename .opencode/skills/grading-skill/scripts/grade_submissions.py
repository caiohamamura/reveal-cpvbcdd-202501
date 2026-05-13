#!/usr/bin/env python3
"""
Grade all submissions based on identified groups.
Reads groups.json from identify_groups.py and generates a markdown table.

Usage:
    python3 grade_submissions.py <submissions_dir> [assignment_id]

assignment_id: ID da tarefa (ex: 46257). Usado para salvar na pasta assignments_<id>
no workspace (/home/openclaw/.openclaw/workspace/moodle/assignments_<id>/).
Se não informado, infere do nome do diretório (ex: /tmp/subs_46257 -> 46257).
"""
import sys
import os
import json
import re


# ============================================================================
# CRITÉRIOS DE AVALIAÇÃO — customize por tarefa se necessário
# ============================================================================
CRITERIA = [
    ("CREATE TABLE (estrutura)", 3),
    ("INSERT INTO (dados)", 2),
    ("CREATE VIEW (≥1)", 3),
    ("VIEW com lógica (WHERE/JOIN/ORDER BY)", 2),
]
TOTAL_POINTS = 10


# ============================================================================
# LÓGICA DE ANÁLISE — customize por tarefa
# ============================================================================
def analyze_sql(filepath_list):
    """
    Analisa um ou mais arquivos SQL e retorna (score_breakdown, feedback_html).
    filepath_list: list of (filepath, filename) tuples
    Returns:
        (scores_dict, feedback_html, error_list)
    """
    scores = {name: 0 for name, _ in CRITERIA}
    errors = []
    feedback_parts = []

    # Combine all SQL content
    combined_content = ''
    for fpath, fname in filepath_list:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                combined_content += f.read() + '\n'
        except:
            try:
                with open(fpath, 'r', encoding='latin-1') as f:
                    combined_content += f.read() + '\n'
            except Exception as e:
                errors.append(f"Não consegui ler {fname}: {e}")

    if not combined_content.strip():
        errors.append("Nenhum conteúdo SQL encontrado")
        return scores, "<p>❌ Nenhum conteúdo SQL</p>", errors

    content_upper = combined_content.upper()

    # Count totals across ALL files
    table_count = content_upper.count('CREATE TABLE')
    insert_count = content_upper.count('INSERT INTO')
    view_count = content_upper.count('CREATE VIEW') + content_upper.count('CREATE OR REPLACE VIEW')

    # 1. CREATE TABLE
    if table_count >= 3:
        scores["CREATE TABLE (estrutura)"] = 3
        feedback_parts.append(f"✅ {table_count} tabelas criadas")
    elif table_count >= 1:
        scores["CREATE TABLE (estrutura)"] = 2
        feedback_parts.append(f"⚠️ {table_count} tabela(s) criada(s)")
    else:
        feedback_parts.append("❌ Nenhuma tabela criada")

    # 2. INSERT INTO
    if insert_count >= 5:
        scores["INSERT INTO (dados)"] = 2
        feedback_parts.append(f"✅ {insert_count} INSERTs (dados)")
    elif insert_count >= 1:
        scores["INSERT INTO (dados)"] = 1
        feedback_parts.append(f"⚠️ {insert_count} INSERT(s)")
    else:
        feedback_parts.append("❌ Nenhum INSERT")

    # 3. CREATE VIEW
    if view_count >= 3:
        scores["CREATE VIEW (≥1)"] = 3
        feedback_parts.append(f"✅ {view_count} views criadas")
    elif view_count >= 1:
        scores["CREATE VIEW (≥1)"] = 2
        feedback_parts.append(f"⚠️ {view_count} view(s)")
    else:
        feedback_parts.append("❌ Nenhuma view")

    # 4. VIEW com lógica (WHERE/JOIN/ORDER BY em views)
    has_where = 'WHERE' in content_upper and 'CREATE' in content_upper
    has_join = 'JOIN' in content_upper
    has_order = 'ORDER BY' in content_upper
    logic_count = sum([has_where, has_join, has_order])

    if logic_count >= 3:
        scores["VIEW com lógica (WHERE/JOIN/ORDER BY)"] = 2
        feedback_parts.append("✅ Views com WHERE/JOIN/ORDER BY")
    elif logic_count >= 1:
        scores["VIEW com lógica (WHERE/JOIN/ORDER BY)"] = 1
        feedback_parts.append(f"⚠️ {logic_count} view(s) com lógica")
    else:
        if view_count > 0:
            feedback_parts.append("⚠️ Views sem WHERE/JOIN/ORDER BY")

    total = sum(scores.values())
    feedback_html = "<p>" + "<br>".join(feedback_parts) + f"</p><p><strong>Total: {total}/{TOTAL_POINTS}</strong></p>"

    return scores, feedback_html, errors


def find_all_sql_files(student_dir):
    """Find ALL SQL files for a student (direct + from ZIPs)."""
    sql_files = []

    # Direct SQL files (top level only)
    for f in os.listdir(student_dir):
        if f.endswith(('.sql', '.txt')):
            fp = os.path.join(student_dir, f)
            if os.path.isfile(fp):
                sql_files.append((fp, f))

    # Files from extracted ZIPs (recursive, skip top-level already counted)
    for root, dirs, files in os.walk(student_dir):
        for f in files:
            if f.endswith(('.sql', '.txt')):
                fp = os.path.join(root, f)
                if os.path.dirname(fp) == student_dir:
                    continue
                sql_files.append((fp, f))

    return sql_files


def grade_student(student_dir):
    """Grade a single student. Returns (grade, feedback, errors)."""
    sql_files = find_all_sql_files(student_dir)

    if not sql_files:
        return 0, "<p>❌ Nenhum arquivo SQL encontrado</p>", ["No SQL files"]

    scores, feedback, errors = analyze_sql(sql_files)
    total = sum(scores.values())
    return total, feedback, errors


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 grade_submissions.py <submissions_dir> [assignment_id]")
        print("  assignment_id: ID da tarefa (ex: 46257). Salva em assignments_<id>/ no workspace.")
        sys.exit(1)

    base_dir = sys.argv[1]
    assignment_id = sys.argv[2] if len(sys.argv) > 2 else None

    if not assignment_id:
        match = re.search(r'subs_(\d+)$', base_dir)
        assignment_id = match.group(1) if match else os.path.basename(base_dir)

    # Persistent workspace output directory
    workspace = '/home/openclaw/.openclaw/workspace/moodle'
    output_base = os.path.join(workspace, f'assignments_{assignment_id}')
    os.makedirs(output_base, exist_ok=True)

    groups_path = os.path.join(base_dir, 'groups.json')
    if not os.path.exists(groups_path):
        print(f"ERRO: groups.json não encontrado. Execute identify_groups.py primeiro.")
        sys.exit(1)

    with open(groups_path) as f:
        groups_data = json.load(f)

    results = []
    graded_students = set()

    # Grade normal groups
    for group in groups_data['normal']:
        for member in group['members']:
            if member in graded_students:
                continue
            graded_students.add(member)

            student_dir = os.path.join(base_dir, member.replace(' ', '_'))
            grade, feedback, errors = grade_student(student_dir)
            results.append({
                'members': [member],
                'student': member,
                'grade': grade,
                'feedback': feedback,
                'errors': errors
            })

    # Grade fraud groups
    for group in groups_data['fraud']:
        for member in group['members']:
            if member in graded_students:
                continue
            graded_students.add(member)
            results.append({
                'members': [member],
                'student': member,
                'grade': 0,
                'feedback': "<p>❌ FRAUDE: arquivo idêntico entregue por grupos diferentes</p>",
                'is_fraud': True
            })

    # Grade no-submission
    for student in groups_data.get('no_submission', []):
        if student in graded_students:
            continue
        graded_students.add(student)
        results.append({
            'members': [student],
            'student': student,
            'grade': 0,
            'feedback': "<p>❌ Nenhum envio</p>"
        })

    # Print to stdout
    print(f"\n# Correção — Tarefa {assignment_id}")
    print(f"  Base: {base_dir}")
    print()
    print("| Aluno | Nota | Feedback |")
    print("|-------|------|----------|")

    for r in sorted(results, key=lambda x: (-x['grade'], x['student'])):
        for member in r['members']:
            print(f"| {member} | **{r['grade']}** | {r['feedback']} |")

    print()
    print(f"**Total de alunos corrigidos:** {len(results)}")
    print(f"**Grupos com fraude:** {len([r for r in results if r.get('is_fraud')])}")
    print(f"**Sem envio:** {len([r for r in results if 'Nenhum envio' in r.get('feedback', '')])}")

    # Save to persistent workspace
    output_md = os.path.join(output_base, 'correcao.md')
    with open(output_md, 'w') as f:
        f.write(f"# Correção — Tarefa {assignment_id}\n\n")
        f.write(f"**Base:** {base_dir}\n\n")
        f.write("| Aluno | Nota | Feedback |\n")
        f.write("|-------|------|----------|\n")
        for r in sorted(results, key=lambda x: (-x['grade'], x['student'])):
            for member in r['members']:
                fb = r['feedback'].replace('|', '\\|')
                f.write(f"| {member} | **{r['grade']}** | {fb} |\n")
        f.write(f"\n**Total de alunos corrigidos:** {len(results)}\n")
        f.write(f"**Grupos com fraude:** {len([r for r in results if r.get('is_fraud')])}\n")
        f.write(f"**Sem envio:** {len([r for r in results if 'Nenhum envio' in r.get('feedback', '')])}\n")

    print(f"\nRelatório salvo em: {output_md}")

    output_json = os.path.join(output_base, 'correcao.json')
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"JSON salvo em: {output_json}")


if __name__ == '__main__':
    main()