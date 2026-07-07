---
name: convert-pptx
description: Convert PowerPoint (.pptx) presentations in the ia/ folder into Reveal.js decks for the CPVBCDD framework. Use when asked to convert a PPTX to slides, "converter aula NN", "transformar pptx em reveal", or produce ia/aulaNN-<slug>.html from a .pptx.
---

# Converter PPTX → Reveal.js (pasta `ia/`)

Base de instruções para converter as apresentações PowerPoint da pasta `ia/` em decks
Reveal.js do framework CPVBCDD. Validado na conversão da Aula 01
(`ia/aula01-introducao-ia.html`) — use esse arquivo como referência de estilo.

## Trigger
Quando o usuário pedir para converter um `.pptx` da pasta `ia/` em slides Reveal.js, dizer
"converter aula NN", "transformar pptx em reveal", ou gerar `ia/aulaNN-<slug>.html`.

## Regras gerais

- Leia e siga **exatamente** `.opencode/skills/create-slides/SKILL.md` (boilerplate HTML,
  super-sections, componentes Vue, convenções de estilo) e
  `.opencode/skills/slide-design/SKILL.md` (qualidade visual).
- Saída: `ia/aulaNN-<slug>.html` com imagens em `ia/images/aulaNN[-slug]/`.
- Cover: `<header1 aula="NN" curso="Inteligência Artificial" title-size="24" title="...">`.
- Conteúdo em pt-BR, fiel ao PPTX. Reorganize os slides em super-sections ("Etapa N: ...")
  por tópico; capa, resumo e referências ficam no nível raiz.
- Fragments com moderação (ver skill). `<ls-u>` só para motivação, passos de exercício e resumo.
- Slides que no PPTX são só uma imagem inteira viram slide com título + imagem centralizada.
- Código (se houver) em `<code-block lang="python">`; decodifique entidades (`&gt;` → `>`).
- Termine com slide "Resumo da aula" (+ "Próxima aula: ..." se souber) e "Referências"
  (links do PPTX como `<a>` clicáveis).

## Passo 1 — Extrair texto e mapa de imagens

Sem dependências externas (não use `unpack.py`/`defusedxml` — não está instalado):

```bash
python -c "
import zipfile, re, sys
sys.stdout.reconfigure(encoding='utf-8')
z = zipfile.ZipFile('ARQUIVO.pptx')
def natnum(n): return int(re.search(r'(\d+)', n).group(1))
slides = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=natnum)
for s in slides:
    xml = z.read(s).decode('utf-8'); num = natnum(s)
    paras = []
    for p in re.findall(r'<a:p>(.*?)</a:p>', xml, re.S):
        t = ''.join(re.findall(r'<a:t>(.*?)</a:t>', p, re.S)).strip()
        if t: paras.append(t)
    rels = z.read(f'ppt/slides/_rels/slide{num}.xml.rels').decode('utf-8')
    rmap = dict(re.findall(r'Id=\"(rId\d+)\"[^>]*Target=\"\.\./media/([^\"]+)\"', rels))
    used = set(re.findall(r'r:embed=\"(rId\d+)\"', xml))
    imgs = [m for rid, m in rmap.items() if rid in used]
    print(f'=== SLIDE {num} ===')
    for t in paras: print(' ', t)
    if imgs: print('  [IMAGES]:', ', '.join(imgs))
"
```

## Passo 2 — Extrair, inspecionar e renomear imagens

1. Extraia só as imagens **usadas** pelos slides para `images/aulaNN/`.
2. Gere um contact sheet com PIL (grade ~5 colunas, thumbs 260px, nome em vermelho) e
   **leia a imagem** com a ferramenta Read para saber o que cada uma é. Delete o contact
   sheet depois.
3. Renomeie para nomes descritivos em kebab-case pt-BR (ex.: `alan-turing.jpg`,
   `deteccao-fraude-fluxo.png`).
4. Comprima as pesadas: se >500 KB, redimensione para largura máx. 1200 e regrave
   (JPG q85 se não tiver transparência; PNG otimizado se tiver).
5. **Gotcha PIL/Windows:** `Image.open()` mantém o arquivo aberto — use
   `with Image.open(f) as im: im.load()` antes de `os.rename`/`os.remove`, senão
   `PermissionError: WinError 32`.
6. Descarte imagens inúteis (quase pretas, fotos pessoais enormes, duplicadas).
   Ao final, confira que não sobrou asset órfão nem referência quebrada.
7. Screenshots de texto claro sobre fundo branco: exiba com
   `style="background: #f8f8f2; border-radius: 8px; padding: 10px;"` para legibilidade
   no tema escuro. Fotos: só `border-radius: 8px`.

## Passo 3 — Escrever o deck

Use o boilerplate exato da skill create-slides (o mesmo de `aula01-introducao-ia.html`).
Indentação de 4 espaços dentro de `<div class="slides">`. Todo `<img>` com `alt` conciso
em pt-BR e `width` **ou** `height` (não ambos).

## Passo 4 — QA (obrigatório)

1. **Validador estático:**
   `python ../.opencode/skills/validate-slides/scripts/validate_slide_deck.py aulaNN-<slug>.html`
   → 0 erros/0 warnings.
2. **Referências de imagem:** todo `src="images/..."` existe em disco; nenhum asset sem uso.
3. **Sem caracteres CJK**, nenhum `<img>` sem `alt`.
4. **Links externos** respondem 200 (`curl -s -o /dev/null -w "%{http_code}" -L -A "Mozilla/5.0" URL`).
5. **Overflow no navegador:** suba o preview com a config indicada no seu prompt
   (`.claude/launch.json` já tem uma entrada por aula — NÃO edite esse arquivo),
   navegue até `http://localhost:PORTA/ia/aulaNN-<slug>.html` e rode via eval:

```js
(() => {
  const deck = window.deck; const cw = 960, ch = 700;
  const indices = [];
  document.querySelectorAll('.slides > section').forEach((h, hi) => {
    const verts = h.querySelectorAll(':scope > section');
    if (verts.length) verts.forEach((v, vi) => indices.push([hi, vi]));
    else indices.push([hi, 0]);
  });
  const results = [];
  for (const [h, v] of indices) {
    deck.slide(h, v);
    const s = deck.getCurrentSlide();
    const sRect = s.getBoundingClientRect(); const scale = deck.getScale();
    let maxRight = 0, maxBottom = 0;
    s.querySelectorAll('img, table, pre, div, ul, p, blockquote').forEach(el => {
      const r = el.getBoundingClientRect(); if (!r.width) return;
      maxRight = Math.max(maxRight, (r.right - sRect.left) / scale);
      maxBottom = Math.max(maxBottom, (r.bottom - sRect.top) / scale);
    });
    results.push({ h, v, title: (s.querySelector('h2,h1')||{}).textContent?.trim().slice(0,40),
                   maxRight: Math.round(maxRight), maxBottom: Math.round(maxBottom) });
  }
  deck.slide(0, 0);
  return { over: results.filter(r => r.maxBottom > ch + 10 || r.maxRight > cw + 10), total: results.length };
})()
```

   `over` deve ficar **vazio**. Se um slide estourar, reduza `height`/`width` das imagens,
   fontes ou margens e repita. Cheque também imagens quebradas
   (`[...document.querySelectorAll('img')].filter(i => i.complete && !i.naturalWidth)`) e o
   console (sem erros).

   **Nota:** `preview_screenshot` pode dar timeout neste ambiente — não insista; o check
   programático acima substitui a inspeção visual de overflow.

## Checklist final

- [ ] Validador: 0 erros / 0 warnings
- [ ] `over: []` no check de overflow (canvas 960×700)
- [ ] Sem imagens quebradas nem assets órfãos
- [ ] Links externos 200
- [ ] pt-BR correto, sem CJK, sem meta-comentários para o professor
- [ ] Estrutura: capa → etapas em super-sections → resumo → referências
</content>
</invoke>
