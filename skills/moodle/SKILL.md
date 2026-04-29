---
name: moodle
description: "Navega e extrai informações do Moodle via scraping HTTP (requests/fetch). Use quando perguntarem sobre aulas, tarefas, disciplinas, notas, ou qualquer atividade do Moodle. Acessa https://ead.cpv.ifsp.edu.br com cookie de sessão. Suporta: listar tarefas, ver detalhes de disciplina, baixar arquivos, consultar notas."
---

# Moodle Skill

Navega o Moodle como um usuário real via HTTP requests (não API).

## Configuração

- **Base URL:** `https://ead.cpv.ifsp.edu.br`
- **Course ID (IoT CPVIOTS):** 1639
- **Cookie:** `MoodleSession=57p6nf782p1epirj7nv0ahgpip`

## Workflow Principal

1. **Sempre use `requests`** com `session` Python e cookie `MoodleSession`
2. **CSRF**: Moodle usa `logintoken` nos forms — haga fetch do form de login primeiro se necessário
3. **Parse**: use `BeautifulSoup` para extrair dados do HTML
4. **headers mínimos**:
   ```python
   headers = {"User-Agent": "Mozilla/5.0"}
   ```

## ⚠️ POST para editsection.php — Campos Obrigatórios

O Moodle exige **TODOS** os campos do formulário no POST, não só os editáveis. Se faltar qualquer campo, o servidor ignora silenciosamente as mudanças.

**Campos críticos que são facilmente esquecidos:**
- `_qf__editsection_form`: `"1"`
- `mform_isexpanded_id_generalhdr`: `"1"`
- `mform_isexpanded_id_availabilityconditions`: `"0"`
- `summary_editor[format]`: `"4"` (formato HTML do Atto)
- `availabilityconditionsjson`: `'{"op":"&","c":[],"showc":[]}'`
- `level`: `""`
- `firsttabtext`: `"Índice"`
- `tabsectionbackground`: `""`
- `tabstyles`: `""`

**Abordagem correta:**
1. Fazer GET no `editsection.php?id=ID&sr=S` e extrair **todos** os campos do `<form>` (preservando ordem e campos duplicados como `id`)
2. Atualizar apenas `name` e `summary_editor[text]`
3. Manter todos os outros campos intactos
4. Enviar como `application/x-www-form-urlencoded

## Formato do Curso: Onetopic

Este Moodle usa o formato `onetopic` — cada seção carrega separadamente:

```
GET /course/view.php?id=1639&section=N
```

Geralmente N de 0 a ~11.

## Tarefas Comuns

### Listar todas as atividades do curso (todas as seções)
```python
all_activities = {}
for section_num in range(0, 12):
    r = session.get(f"{BASE}/course/view.php?id=1639&section={section_num}")
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.select('li.activity'):
        mod = [c for c in a.get('class', []) if c not in ('activity', 'activity-wrapper')][0]
        name = a.select_one('.instancename')
        if name:
            print(f'Sec{section_num}: [{mod}] {name.get_text(strip=True)}')
```

### Duplicar e editar seção
```bash
python3 scripts/duplicate_section.py \
  --course 1486 \
  --source-section 8 \
  --new-name "Aula09 - Foo" \
  --summary aula09.html
```

**O que o script faz:**
1. Encontra o `sectionid` da seção de origem (source-section = número da seção no formato onetopic)
2. Duplica via GET `?duplicatesection=1`
3. Extrai o novo `id` da seção duplicada
4. Faz POST em `editsection.php` com o HTML do summary

**Parâmetros obrigatórios:**
- `--course`: ID numérico do curso
- `--source-section`: Número da seção (0=geral, 1=aula01, etc.)
- `--new-name`: Nome da nova seção
- `--summary`: Caminho para arquivo HTML com o conteúdo da seção

**Dica:** O HTML da summary deve usar `urllib.parse.quote()` nos caracteres especiais. Exemplo see `scripts/test_summary.html`.

### Ver tarefa específica (assignment)
```
GET /mod/assign/view.php?id={cmid}
```

## Exemplo de Script

```python
import requests
from bs4 import BeautifulSoup

BASE = "https://ead.cpv.ifsp.edu.br"
COOKIE = "MoodleSession=p0u7nfikb72j9ae5ci23ta2rtp"

def moodle_get(path):
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0"})
    s.cookies.set("MoodleSession", "p0u7nfikb72j9ae5ci23ta2rtp", domain="ead.cpv.ifsp.edu.br")
    r = s.get(f"{BASE}{path}")
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

# Listar tarefas do curso IoT
soup = moodle_get("/course/view.php?id=1639")
# ... parsear HTML
```

## Quando usar

- "Quais tarefas tenho no Moodle?"
- "Quando é o prazo da atividade X?"
- "O que tem na disciplina de IoT?"
- "Baixar o arquivo da aula"
- Qualquer dúvida sobre atividades, notas, ou conteúdo do Moodle

## Referências

- `references/endpoints.md` — endpoints comuns do Moodle
- `references/parsing.md` — seletores CSS e padrões de parsing
