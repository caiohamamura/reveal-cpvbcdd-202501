# Endpoints Moodle

## Autenticação

- **Login form:** `GET /login/index.php`
- **Login action:** `POST /login/index.php` (params: `username`, `password`, `logintoken`)
- **Logout:** `GET /login/logout.php`

## Cursos

- **Meus cursos:** `GET /my/` ou `GET /`
- **Ver curso:** `GET /course/view.php?id={course_id}`
- **Listar seções:** dentro do course view, seções em `<ul id="section">` ou `.topics`

## Seções de Curso (Onetopic)

- **Ver seção:** `GET /course/view.php?id={course_id}&section={N}`
- **Editar seção (form):** `GET /course/editsection.php?id={db_id}&sr={section_num}`
  - `db_id` = ID numérico da seção (não é o mesmo que `sectionid` do onetopic!)
  - `sr` = número da seção no formato onetopic
- **Salvar seção:** `POST /course/editsection.php`
  - ⚠️ Requer TODOS os campos do formulário (ver SKILL.md)
- **Duplicar seção:** `GET /course/view.php?id={course}&sesskey={SKEY}&sectionid={SECTIONID}&duplicatesection=1`
  - Retorna redirect para `?section=N+1` da nova seção
  - O novo `db_id` está no HTML da página redirecionada

## Atividades

- **Tarefas (assignments):** `GET /mod/assignment/view.php?id={cmid}`
- **Lista de tarefas do curso:** `GET /mod/assignment/index.php?id={course_id}`
- **Entregar tarefa:** `POST /mod/assignment/view.php?id={cmid}` (submit)
- **Fóruns:** `GET /mod/forum/view.php?id={forum_cmid}`
- **Recursos (arquivos):** `GET /mod/resource/view.php?id={cmid}`

## Notas

- **Grades:** `GET /grade/report/overview/index.php` (visão geral)
- **Por curso:** `GET /grade/report/user/index.php?id={course_id}`

## Users

- **Perfil:** `GET /user/profile.php?id={user_id}`
- **Editar perfil:** `GET /user/edit.php?id={user_id}&course={course_id}`
