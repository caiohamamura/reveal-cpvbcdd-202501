#!/usr/bin/env python3
"""
Moodle Section Duplicator + Editor

Workflow:
1. GET /course/view.php?id=COURSE&section=N  → encontra sectionid da seção a duplicar
2. GET /course/view.php?...&sectionid=SECTIONID&duplicatesection=1  → duplica
3. O Moodle redireciona para a nova seção (section=N+1)
4. Extrair o NOVO id da seção do HTML da página redirecionada
   (procurar editsection.php?id=NOVO_ID onde NOVO_ID != sectionid original)
5. GET /course/editsection.php?id=NOVO_ID&sr=SECTION  → obtiene form
6. POST /course/editsection.php  → salva com novo nome + summary

Uso:
  python3 duplicate_section.py --course 1486 --source-section 9 --new-name "Aula09 - Foo" --summary aula09.html
"""
import requests
from bs4 import BeautifulSoup
import re
import sys
import argparse

BASE = "https://ead.cpv.ifsp.edu.br"
COOKIE = "57p6nf782p1epirj7nv0ahgpip"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.5",
}


def get_sesskey(session, course_id):
    r = session.get(f"{BASE}/course/view.php?id={course_id}&section=0")
    m = re.search(r'"sesskey":"([^"]+)"', r.text)
    return m.group(1) if m else None


def find_sectionid(session, course_id, section_num):
    """Encontra o sectionid da seção N (source)."""
    r = session.get(f"{BASE}/course/view.php?id={course_id}&section={section_num}")
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.select('a[href*="duplicatesection"]'):
        href = a.get("href", "")
        m = re.search(r'sectionid=(\d+)', href)
        if m:
            return int(m.group(1))
    return None


def duplicate_section(session, course_id, source_sectionid, source_section_num, sesskey):
    """
    Duplica via GET no link de menu.
    Retorna (new_section_db_id, new_section_num) após duplicação.
    O Moodle redireciona para section=new_section_num; o new_section_db_id
    está no HTML da página como editsection.php?id=NOVO_ID.
    """
    url = f"{BASE}/course/view.php"
    params = {
        "id": course_id,
        "sesskey": sesskey,
        "sectionid": source_sectionid,
        "duplicatesection": 1,
    }
    r = session.get(url, params=params, headers={"Referer": f"{BASE}/course/view.php?id={course_id}"})

    # A nova seção fica em ?section=N+1
    m = re.search(r'[?&]section=(\d+)', r.url)
    new_section_num = int(m.group(1)) if m else source_section_num + 1

    # Encontrar o novo id no HTML (editsection.php?id=NOVO_ID)
    # Diferente do sectionid original
    soup = BeautifulSoup(r.text, "html.parser")
    new_id = None
    seen_ids = {source_sectionid}
    for a in soup.select('a[href*="editsection.php?id="]'):
        href = a.get("href", "")
        id_matches = re.findall(r'id=(\d+)', href)
        for mid in id_matches:
            mid_int = int(mid)
            if mid_int not in seen_ids:
                new_id = mid_int
                seen_ids.add(mid_int)
                break
        if new_id:
            break

    return new_id, new_section_num


def get_edit_form_fields(session, section_db_id, section_num):
    """
    Faz GET no editsection.php e retorna lista de tuplas (name, value) com
    TODOS os campos do formulário (preserva ordem e campos duplicados).
    """
    r = session.get(
        f"{BASE}/course/editsection.php?id={section_db_id}&sr={section_num}"
    )
    soup = BeautifulSoup(r.text, "html.parser")
    forms = soup.select("form")
    # O form de edição é o segundo (índice 1), não o de "Configurar modo"
    form = forms[1] if len(forms) > 1 else forms[0]

    fields = []
    for inp in form.select("input, textarea, select"):
        name = inp.get("name")
        if not name:
            continue
        t = inp.get("type", "")
        if t in ("submit", "button", "reset"):
            continue
        fields.append((name, inp.get("value", "")))

    return fields


def update_section(session, section_db_id, section_num, course_id, name, summary_html, sesskey):
    """
    Faz POST no editsection.php para atualizar name e summary.
    
    IMPORTANTE: Moodle exige TODOS os campos do formulário, não só os editáveis.
    Inclui: _qf__editsection_form, mform_isexpanded_*, summary_editor[format],
    availabilityconditionsjson, level, firsttabtext, tab*, etc.
    """
    all_fields = get_edit_form_fields(session, section_db_id, section_num)

    # Converte para dict para atualizar, depois converte de volta para lista
    # (preserva ordem e campos duplicados como 'id' múltiplos)
    fields_dict = {}
    for n, v in all_fields:
        if n not in fields_dict:  # primeiro valor vence para campos não-dup
            fields_dict[n] = v

    # Atualiza campos editáveis
    fields_dict["name"] = name
    fields_dict["summary_editor[text]"] = summary_html
    # Moodle Usa format=4 (HTML) para o editor Atto
    fields_dict["summary_editor[format]"] = "4"
    # availabilityconditionsjson deve ter estrutura JSON válida
    if not fields_dict.get("availabilityconditionsjson"):
        fields_dict["availabilityconditionsjson"] = '{"op":"&","c":[],"showc":[]}'
    fields_dict["submitbutton"] = "Salvar+mudan%C3%A7as"

    # Reconverte para lista de tuplas
    final_fields = list(fields_dict.items())

    r = session.post(
        f"{BASE}/course/editsection.php",
        data=final_fields,
        headers={
            "Referer": f"{BASE}/course/editsection.php?id={section_db_id}&sr={section_num}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )
    return r


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Duplicar e editar uma seção do Moodle"
    )
    parser.add_argument("--course", required=True, type=int)
    parser.add_argument("--source-section", required=True, type=int,
                        help="Número da seção a duplicar (0=geral, 1=aula01, etc.)")
    parser.add_argument("--new-name", required=True)
    parser.add_argument("--summary", required=True,
                        help="Arquivo HTML com o conteúdo da seção")
    args = parser.parse_args()

    sess = requests.Session()
    sess.headers.update(HEADERS)
    sess.cookies.set("MoodleSession", COOKIE, domain="ead.cpv.ifsp.edu.br")

    print(f"[1] Buscando sesskey do curso {args.course}...")
    sesskey = get_sesskey(sess, args.course)
    print(f"  sesskey = {sesskey}")

    print(f"[2] Encontrando sectionid da seção {args.source_section}...")
    source_sectionid = find_sectionid(sess, args.course, args.source_section)
    print(f"  sectionid = {source_sectionid}")

    print(f"[3] Duplicando seção {args.source_section} (sectionid={source_sectionid})...")
    new_id, new_sec = duplicate_section(sess, args.course, source_sectionid, args.source_section, sesskey)
    print(f"  new_section_db_id = {new_id}, new_section_num = {new_sec}")

    if not new_id:
        print("❌ FALHA: não consegui encontrar o ID da nova seção após duplicação")
        sys.exit(1)

    print(f"[4] Lendo summary de {args.summary}...")
    with open(args.summary, "r") as f:
        summary_html = f.read()
    print(f"  tamanho = {len(summary_html)} chars")

    print(f"[5] Atualizando seção {new_id} (sr={new_sec}) com nome '{args.new_name}'...")
    r = update_section(sess, new_id, new_sec, args.course, args.new_name, summary_html, sesskey)
    print(f"  Status: {r.status_code}")
    print(f"  URL final: {r.url}")

    if r.status_code == 200:
        print("✅ Feito!")
    else:
        print("❌ Falhou — verificar resposta acima")
        sys.exit(1)
