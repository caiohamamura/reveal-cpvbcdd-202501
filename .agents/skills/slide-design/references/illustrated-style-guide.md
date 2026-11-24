# Illustrated Pedagogical Style Guide

Blueprint distilled from Prof. Caio Hamamura's reference presentations (e.g., *2026IA - Aula 11 - Do VAE ao Stable Diffusion*) adapted for this repository's Dracula Reveal.js framework.

## Core Philosophy

Every technical concept in Inteligência Artificial is taught as a **visual story anchored in real research and intuition**:

1. **Show the real artifact first** — the seminal paper header, the paper's iconic diagram, a real generated sample grid, a real distribution/gradient plot, or a clear custom technical infographic.
2. **Guide the eye progressively** — highlight one sentence of an abstract, box one sub-module of an architecture with an arrow, or color-code one term of a loss function at a time, adding a single plain-Portuguese intuitive caption underneath.
3. **Keep text radically sparse** — most content slides carry **0 to 35 words**. Let the diagram, visual progression, and spoken lecture carry the explanation; never turn a slide into a paragraph or a 6-bullet summary card.
4. **Connect ideas across slides** — reuse an earlier diagram at smaller scale alongside a new plot (e.g., LDM architecture next to the VAE latent-space scatter plot) so students see *how* pieces connect.
5. **Anchor practice right where theory lands** — drop a `.colab-pill` notebook link right below the slide that finishes explaining a model/experiment (e.g., VAE architecture → Colab VAE; MNIST médio → Colab MNIST; Stable Diffusion → Colab do zero + pré-treinado).

---

## Narrative Arc for an IA Lesson

Use this natural rhythm (adapt as needed per topic):

1. **Cover (`<header1>`)**: Recognizable tool logos or iconic visual in the slot + lesson number + title.
2. **Visual Recap ("Na aula passada")**: Open with `<section-banner title="Na aula passada">` followed by 1 visual anchor slide from the previous lesson (e.g., previous paper header + real output grid), NOT a 5-bullet text recap.
3. **High-Level Intuition First**: Before any history or equations, show a 1-slide intuitive diagram + 2 numbered steps explaining *what the new idea does at a high level* (e.g., noise → iterative denoising → image).
4. **Historical / Problem-Driven Chapters**: Wrap each major conceptual step in a super-section starting with `<section-banner>` (IFSP green-striped banner). Follow the chain:
   - *Seminal paper & year* → *Core visual mechanism* → *Explicit limitation* → *Next paper that solves it*.
5. **Progressive Math & Architecture Deconstruction**: Unpack key equations (`.formula-stage`) and architectures (`.figure-stage` + `.annotate-box` + `.annotate-svg` / `<leader-line>`) step by step.
6. **Real Visual Evidence & Tradeoffs**: Real benchmark comparisons, sample grids, latent manifolds, failure cases, and intuitive takeaways (`.slide-takeaway`).
7. **Hands-On Notebooks & References**: Contextual `.colab-pill` links during the deck + clean closing summary and clickable academic references (`arXiv` / `DOI`).

---

## Reusable Slide Patterns

All classes and components below are globally available via `dist/custom.css` and `components/components.js`.

### Pattern 1: IFSP Green-Striped Section Divider (`<section-banner>`)

Mirrors the green diagonal-striped section transitions (`img/fundo.png`). Optionally place a paper card or iconic diagram inside the default slot.

```html
        <section data-auto-animate>
          <section-banner
            eyebrow="Etapa 2"
            title="Difusão estável: uma outra abordagem"
            subtitle="Como transformar ruído puro em imagem passo a passo">
            <div class="figure-card">
              <img src="images/aula11/markov-chain.png" alt="Cadeia de Markov de difusão" height="120" />
            </div>
            <paper-card
              compact
              title="Diffusion Models Beat GANs on Image Synthesis"
              authors="Prafulla Dhariwal, Alex Nichol — OpenAI"
              year="2021"
              url="https://arxiv.org/abs/2105.05233">
            </paper-card>
          </section-banner>
        </section>
```

### Pattern 2: Seminal Paper + Progressive Abstract Highlight (`<paper-card>`)

Replaces raw text citations with a high-contrast academic card where key sentences light up progressively like a yellow highlighter.

```html
        <section data-auto-animate>
          <h2>Autoencoders (2006)</h2>
          <paper-card
            title="Reducing the Dimensionality of Data with Neural Networks"
            authors="G. E. Hinton and R. R. Salakhutdinov"
            venue="Science"
            year="2006"
            url="https://www.science.org/doi/10.1126/science.1127647">
            <p>
              <mark class="paper-mark fragment" data-fragment-index="1">High-dimensional data can be converted to low-dimensional codes by training a multilayer neural network with a small central layer to reconstruct high-dimensional input vectors.</mark>
              Gradient descent can be used for fine-tuning the weights in such "autoencoder" networks,
              <mark class="paper-mark fragment" data-fragment-index="2">allowing deep autoencoder networks to learn low-dimensional codes that work much better than PCA.</mark>
            </p>
          </paper-card>
        </section>
```

For compact corner anchoring next to a figure or formula, use `.title-with-paper` + `<paper-card compact ...>`.

### Pattern 3: Progressive Visual Annotations over a Real Figure (`.figure-stage`)

Walk students through an architecture diagram one piece at a time using percentage-positioned translucent `.annotate-box` regions and SVG arrows (or `<leader-line>`).

```html
        <section data-auto-animate>
          <h2>Stable Diffusion: usa VAE?</h2>
          <div style="text-align: center;">
            <div class="figure-card">
              <div class="figure-stage">
                <img src="images/aula11/ldm-arquitetura.png"
                     alt="Arquitetura Latent Diffusion Models com Encoder E, espaço latente e Decoder D"
                     height="360" />
                <div class="annotate-box annotate-box--yellow fragment" data-fragment-index="1"
                     style="left: 9%; top: 5%; width: 13%; height: 67%;"></div>
                <div class="annotate-box annotate-box--green fragment" data-fragment-index="2"
                     style="left: 23%; top: 5%; width: 57%; height: 67%;"></div>
              </div>
            </div>
          </div>
          <p class="slide-takeaway fragment" data-fragment-index="1">
            <strong style="color: #f1fa8c;">Encoder \(\mathcal{E}\) + Decoder \(\mathcal{D}\):</strong> isso é o VAE.
          </p>
          <p class="slide-takeaway fragment" data-fragment-index="2">
            <strong style="color: #50fa7b;">Espaço latente:</strong> o ruído atua nos códigos do VAE, não nos pixels.
          </p>
          <p class="source">Fonte: Rombach et al. (2022), <a href="https://arxiv.org/abs/2112.10752" target="_blank" rel="noopener">Latent Diffusion Models, Fig. 3</a></p>
        </section>
```

For multi-step diagram composition (like connecting Autoencoder output → VGG → `fc7` → `Loss = diferença`), use `data-auto-animate` across 2–3 slides or `<leader-line class="fragment" ...></leader-line>` between figure anchors!

### Pattern 4: Step-by-Step Equation Breakdown (`.formula-stage`)

Show the full equation on a crisp light strip, frame each conceptual term in a distinct color, and reveal its plain-Portuguese meaning directly underneath.

```html
        <section data-auto-animate>
          <div class="title-with-paper">
            <h2>VAE (2013)</h2>
            <paper-card compact title="Auto-Encoding Variational Bayes" authors="Kingma &amp; Welling" year="2013" url="https://arxiv.org/abs/1312.6114"></paper-card>
          </div>
          <p>Força o espaço latente a seguir aproximadamente uma distribuição normal:</p>
          <div class="formula-stage">
            <span>\(\mathcal{L}(\theta, \phi; \mathbf{x}) \simeq\)</span>
            <span class="formula-term formula-term--yellow">\(\tfrac{1}{2}\sum_{j}(1 + \log \sigma_j^2 - \mu_j^2 - \sigma_j^2)\)</span>
            <span>\(+\)</span>
            <span class="formula-term formula-term--pink">\(\tfrac{1}{L}\sum_{l}\log p_\theta(\mathbf{x} \mid \mathbf{z}^{(l)})\)</span>
          </div>
          <div class="formula-captions">
            <p class="formula-caption formula-caption--yellow fragment">Penaliza se a predição se afasta de \(\mu = 0\) e \(\sigma = 1\)</p>
            <p class="formula-caption formula-caption--pink fragment">Mede quão ruim ficou a imagem reconstruída</p>
          </div>
        </section>
```

### Pattern 5: Custom Illustrated Infographic + Contextual Notebook

When explaining an end-to-end architecture or visual transformation (e.g., EBlock/DBlock VAE pipeline, denoising progression from `t=500` to `t=0`, attention flow), generate or craft a dedicated high-resolution visual asset (via image generation, clean SVG, or Matplotlib/Python script) and pair it with a contextual `.colab-pill`:

```html
        <section data-auto-animate>
          <h2>Arquitetura do VAE na prática</h2>
          <div style="text-align: center;">
            <div class="figure-card">
              <img src="images/aula11/arquitetura-vae-infografico.png"
                   alt="Infográfico da arquitetura VAE com blocos EBlock, espaço latente e DBlock"
                   height="430" />
            </div>
            <div>
              <a class="colab-pill" href="https://colab.research.google.com/..." target="_blank" rel="noopener">
                Abrir implementação no Colab ↗
              </a>
            </div>
          </div>
        </section>
```

---

## Anti-Patterns: What Went Wrong Before vs. Target Style

| Earlier AI-Generated Anti-Pattern | Illustrated Style Replacement |
|-----------------------------------|-------------------------------|
| Crude FontAwesome icons (`fa-car-side`, `fa-plane`) + CSS boxes/blobs simulating object detection or clustering | Real photo/synthetic realistic scene + crisp SVG/CSS overlay, cropped paper figure, or real Python/Matplotlib plot |
| Repetitive dark `pipeline-node` text boxes (`Imagem → CNN → Classe`) on 5+ slides | Custom illustrated diagram / real paper architecture figure with progressive highlight overlays |
| Dense 5–6 bullet text slides explaining an algorithm abstractly | 1 seminal `<paper-card>` or paper figure + 1–2 concise intuitive lines (`≤35` words) |
| Generic `artifact-grid` 3-column card walls | Asymmetric `.multi-col` pairing a large hero visual (`1.3fr`) with 2–3 short key points (`1fr`) |
| Uncited architecture claims or text-only bibliography hidden at the end | Inline `<paper-card>` / `<paper-card compact>` right where each paper enters the story, with clickable `arXiv`/`DOI` links |
| Dumping an entire multi-term equation without intuition | `.formula-stage` highlighting each term in yellow/pink with a plain-Portuguese caption right below |
| Artificial boilerplate exercise bolted onto the end | Contextual `.colab-pill` links placed right after the slide explaining that exact model/concept |
