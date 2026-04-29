# Padrões de Parsing Moodle

## Seletores Comuns

### Tarefas (assignment)
```python
# Lista de tarefas na página do curso
tasks = soup.select('li.activity.assignment')

# Cada tarefa: título, prazo, status
for task in tasks:
    title = task.select_one('.instancename').get_text(strip=True)
    deadline = task.select_one('.description time[unixtime]')  # às vezes presente
    # ou procure em .content afterlink
```

### Seções do curso
```python
# Seções/topics
sections = soup.select('li.section')
for sec in sections:
    title = sec.select_one('.sectionname')
    activities = sec.select('.activity')
```

### Forum posts
```python
posts = soup.select('div.forumpost')
for post in posts:
    author = post.select_one('.author .d-inline-block')
    content = post.select_one('.posting .fullpost')
    time = post.select_one('.timestamp')
```

### Mensagensflash (sucesso/erro)
```python
# Feedback após ação
msgs = soup.select('.alert-success, .alert-danger, .toast-wrapper')
```

## Padrões de Data

Moodle frequentemente usa:
- `data-timestamp="1234567890"` (Unix epoch)
- `<span class="text-ubisoft">` com JS para renderizar datas
- Relativas: "em 3 dias", "atrás de 2 horas"

## Offline/Online

```python
# Verificar se ainda está logado
if "login" in r.url.lower():
    raise Exception("Sessão expirou - preciso de novo cookie MoodleSession")
```

## Content-Type

Sempre verificar `r.headers.get('content-type', '')` — às vezes Moodle retorna redirect em vez de HTML.


## Duplicar Seção

O Moodle redireciona após duplicação para `?section=N+1`. O novo `id` da seção (para `editsection.php`) deve ser procurado no HTML da página resultante como `editsection.php?id=NOVO_ID` — diferente do `sectionid` original.

```python
# Após duplicate_section via GET:
r = session.get(f"{BASE}/course/view.php?id={course}&sesskey={sesskey}&sectionid={src_sid}&duplicatesection=1")
# new_section_num está na URL como ?section=N
# new_section_db_id está no HTML (procurar editsection.php?id=NOVO_ID)
```
