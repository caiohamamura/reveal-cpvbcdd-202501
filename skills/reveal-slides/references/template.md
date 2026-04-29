# Template Completo — Reveal.js CPVBCDD

Copie este template EXATAMENTE para criar novos slides.

## Arquivo: `{aula}-{tema}.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

  <title>{CURSO} - {TITULO}</title>

  <link rel="stylesheet" href="../dist/reset.css" />
  <link rel="stylesheet" href="../dist/reveal.css" />
  <link rel="stylesheet" href="../dist/theme/dracula.css" />
  <link rel="stylesheet" href="../dist/custom.css" />
  <link rel="stylesheet" href="../plugin/highlight/monokai.css" />
</head>

<body>

  <div id="app" class="reveal">
    <div class="slides">

      <!-- ============================================================
         SLIDE 1: CAPA
         ============================================================ -->
      <section data-auto-animate>
        <header1 aula="{NUM}" curso="{CURSO}" title-size="24"
                 title="{TITULO COMPLETO}">
          <!-- Slot para diagrama opcional -->
        </header1>
      </section>

      <!-- ============================================================
         SEÇÃO: {NOME DA SEÇÃO}
         ============================================================ -->
      <section>

        <!-- Header da seção -->
        <section data-auto-animate>
          <h2 style="color: #8be9fd;">Seção: {TÍTULO}</h2>
          <p>Subtítulo ou introdução da seção</p>
        </section>

        <!-- Slides de conteúdo -->
        <section data-auto-animate>
          <h2>{TÍTULO DO SLIDE}</h2>
          <multi-col style="gap:15px">
            <div style="flex: 1;">
              <p>Texto explicativo...</p>
            </div>
            <div style="flex: 1; text-align: center;">
              <img src="{URL}" alt="{ALT TEXT}" />
            </div>
          </multi-col>
        </section>

        <!-- Slide de código -->
        <section data-auto-animate>
          <h2>{TÍTULO}</h2>
          <code-block class="lang-sql">
SELECT * FROM exemplo;
          </code-block>
        </section>

        <!-- Slide de código COM HIGHLIGHT SINCRONIZADO -->
        <section data-auto-animate>
          <h2>{TÍTULO}</h2>
          <multi-col style="gap: 30px;">
            <div style="flex: 1;">
              <code-block lang="r" data-line-numbers="1-14|2|5|8-11|14" data-fragment-index="1">
# 1. Começa com modelo vazio
modelo_null <- glm(Target ~ 1, data = treino, family = "binomial")

# 2. Define modelo completo
modelo_full <- glm(Target ~ ., data = treino, family = "binomial")

# 3. Stepwise iterativo
modelo_step <- step(modelo_null,
  scope = list(lower = modelo_null, upper = modelo_full),
  direction = "both",
  k = log(nrow(treino)))  # BIC

# 4. Avalia
BIC(modelo_step)
              </code-block>
            </div>
            <div style="flex: 1;">
              <ol>
                <li class="fragment" data-fragment-index="1">
                  <strong>Passo 1:</strong> Começa com modelo só intercepto
                </li>
                <li class="fragment" data-fragment-index="2">
                  <strong>Passo 2:</strong> Define modelo com todas features
                </li>
                <li class="fragment" data-fragment-index="3">
                  <strong>Passo 3:</strong> Adiciona/remove iterativamente
                </li>
                <li class="fragment" data-fragment-index="4">
                  <strong>Passo 4:</strong> Extrai melhor BIC
                </li>
              </ol>
            </div>
          </multi-col>
        </section>

      </section><!-- fim SEÇÃO -->

      <!-- ============================================================
         SLIDE FINAL: ENCERRAMENTO
         ============================================================ -->
      <section data-auto-animate>
        <h2>Resumo da Aula</h2>
        <ls-u font-size="22pt">
          <li>Tópico 1</li>
          <li>Tópico 2</li>
          <li>Tópico 3</li>
        </ls-u>
        <div style="text-align: center; margin-top: 20px;">
          <p>Próxima aula: <strong>{TÓPICO}</strong></p>
        </div>
      </section>

    </div>
  </div>

  <!-- Scripts na ordem EXATA abaixo -->
  <script src="../dist/reveal.js"></script>
  <script src="../plugin/notes/notes.js"></script>
  <script src="../plugin/math/math.js"></script>
  <script src="../plugin/markdown/markdown.js"></script>
  <script src="../plugin/highlight/highlight.js"></script>
  <script src="../plugin/zoom/zoom.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@11.6.0/plugin/mermaid/mermaid.js"></script>
  <script src="../plugin/leader-line.min.js"></script>
  <script src="../dist/vue.js"></script>
  <script src="../slides_template/header1.js"></script>
  <script src="../components/md.js"></script>
  <script src="../components/components.js"></script>
  <script src="../slides_template/init.js"></script>

  <script>
    window.app = mountSlideApp();
  </script>

</body>

</html>
```

## Checklist de Verificação

Antes de entregar, verificar:

- [ ] `<header1>` usado no slide de capa (não h2+p)
- [ ] `custom.css` linkado no `<head>`
- [ ] `init.js` incluído antes do inline `<script>`
- [ ] `mountSlideApp()` chamado no inline `<script>`
- [ ] `<code-block>` para todo código (não `<pre><code>`)
- [ ] `<code-block>` com conteúdo contendo `<` ou `>` deve usar `<textarea>` wrapper
- [ ] `<multi-col>` para layouts de 2 colunas (não flex divs)
- [ ] `<ls-u>` para listas com animação (resumo, exercícios)
- [ ] `<ul>` para listas estáticas (definições, infos)
- [ ] Super sections (`<section>` envolvendo cada tópico)
- [ ] `data-auto-animate` em todas as seções
- [ ] Sections dividers usam `h2` colorido dentro de super section

## Componentes Vue Disponíveis

| Componente | Attrs | Uso |
|------------|-------|-----|
| `header1` | `aula`, `curso`, `title-size`, `title` | Capa da aula |
| `code-block` | `class="lang-xxx"` | Bloco de código com copiar |
| `multi-col` | `style="gap:15px"` | Colunas |
| `ls-u` | `font-size="22pt"` | Lista animada |
| `copy-btn` | — | Botão copiar (após tabela) |
| `leader-line` | `from`, `to`, `class="fragment"` | Setas |