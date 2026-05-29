---
name: slide-design
description: Design or refine Reveal.js teaching slides with strong visual quality, pedagogical clarity, and CPVBCDD course conventions. Use when creating slides, improving slide aesthetics, replacing generic diagrams, fixing layouts, choosing visual assets, or making a deck feel intentionally designed rather than generic.
---

# Slide Design

Use this skill to make teaching slides visually intentional, readable, and pedagogically useful. It adapts frontend design principles to Reveal.js course decks: the goal is not decorative polish, but a clear visual point of view that helps students understand the lesson.

## Design Thinking

Before editing a deck, choose a concrete visual direction from the lesson itself:

- **Purpose**: What should students understand, practice, or question after this slide?
- **Audience**: Assume technical students in class, reading from a projected screen or mobile screenshot.
- **Tone**: Match the subject. Database, programming, and operational tools should usually feel precise, legible, and concrete, not like a marketing landing page.
- **Memory hook**: Each major section should have one visual idea students can remember: a real screenshot, a table shape, a data file tree, a query result, a timeline, a model diagram, or a concrete classroom example.
- **Constraint**: Preserve the course sequence and pedagogy unless the user asks for a redesign of the narrative.

## Slide Aesthetics

- Prefer **real artifacts** over generic diagrams: logos, screenshots, generated outputs, file trees, query results, database diagrams, notebook plots, API responses, terminal snippets, and local assets.
- Use Mermaid only when it clarifies structure or flow; do not use Mermaid as default decoration.
- Choose one visual emphasis per slide. Avoid mixing a chart, table, long bullet list, and diagram on the same screen.
- Use the CPVBCDD Dracula theme and existing components first; add custom CSS only when it solves a specific layout or visual problem.
- Keep typography functional: large enough for projection, short line lengths, no dense paragraphs.
- Make examples concrete and local to students when possible: real files, real commands, actual output, familiar systems, classroom datasets, web/app behaviors.
- Create contrast through structure, spacing, and one strong accent color; avoid timid, evenly distributed decoration.
- Use motion and fragments only for pedagogy: reveal reasoning steps, sync code with explanation, or stage an exercise. Do not fragment ordinary reference lists.

## Layout Rules

- Fit within the Reveal logical slide height; for this workspace, assume a 700px canvas when judging vertical density.
- Avoid text overlap with headers, footers, logos, and IFSP branding.
- Use stable dimensions for images, code blocks, tables, charts, and diagrams so the layout does not shift between fragments.
- Keep cover slides visually memorable: a real logo/image/asset is often better than a generic flowchart.
- Do not place UI cards inside other cards. Use callout boxes sparingly and only for emphasis.
- Tables must be scannable: short labels, enough padding, and no more columns than can fit comfortably.
- Code slides should show runnable code plus nearby output/result when it helps interpretation.

## Layout Enrichment Patterns (Breaking Monotony)

When multiple slides in a row use the same layout (e.g., just a title and a code block), use these patterns to make them visually distinct:
- **Comparison Cards**: When analyzing multiple approaches, build visual cards (using `artifact-card` in a grid or flex layout) with appropriate accent colors and icons, instead of using boring two-column bullet lists.
- **Flow Rows**: Use `<div class="flow-row">` with `flow-node` and `flow-arrow` to illustrate data movement, pipelines, or architecture (e.g., CSV File → DuckDB Table).
- **Icon Lists**: Instead of standard `<ul>` bullets, wrap lists in an `artifact-card` and use FontAwesome icons (`fa-check`, `fa-xmark`, `fa-magnifying-glass`) to make the points highly scannable.
- **Mock Outputs**: Next to a complex SQL `GROUP BY` or data transformation, place a `<table class="mini-table">` with a mock result (e.g., Category = 10, Total = 20) to ground the abstraction visually.

## Visual Asset Rules

- Prefer local, versioned assets for slides that will be taught offline or in labs.
- Every image needs concise `alt` text.
- Validate that image paths load, return a real image MIME type, and are not tiny placeholder files.
- When using external assets, prefer official project assets or clearly attributable sources.
- Keep lesson-specific assets under a lesson-specific folder such as `planos/aulaNN_topic_assets/`.

## Review Checklist

Before finishing slide work:

- The first slide gives an immediate visual signal of the topic.
- Every major section has a clear purpose and not just content accumulation.
- There is no text or visual overlap at desktop screenshot size.
- Commands, code, data files, and output shown in slides have been tested when feasible.
- The deck still follows the original pedagogical sequence unless explicitly changed.
- HTML parses successfully and referenced local images exist.
