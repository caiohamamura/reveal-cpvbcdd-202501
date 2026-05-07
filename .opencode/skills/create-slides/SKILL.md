---
name: create-slides
description: Create Reveal.js slide files for the CPVBCDD educational framework (IoT, BDD1, BDD2 courses)
license: MIT
compatibility: opencode
metadata:
  audience: instructors
  framework: cpvbcdd
---

## What I do

- Generate complete `.html` slide decks using Reveal.js + Vue components
- Follow the CPVBCDD framework conventions (Dracula theme, specific components, indentation rules)
- Place files in the correct course subfolder (`iot/`, `bdd1/`, `bdd2/`)
- Include boilerplate HTML, cover slide, content sections, exercises, and summary

## When to use me

Use this skill when the user asks to create slides, a new lesson, a new presentation, or says things like "create slides for...", "nova aula...", "slides para...".

Ask the user for: course name, lesson number, and topic if not provided.

## How I work

1. Read `docs/ECOSSISTEMA.md` for the complete framework documentation — Vue components (`<header1>`, `<code-block>`, `<multi-col>`, `<ls-u>`, `<md>`, `<poll-question>`, `<leader-line>`, `<copy-btn>`), plugins (chalkboard, chart, poll, seminar, customcontrols), CSS conventions (Dracula palette, utility classes), and initialization patterns (`mountSlideApp()`).
2. Use the HTML boilerplate with `mountSlideApp()` from `slides_template/init.js`.
3. Apply 4-space indentation inside `<div class="slides">`.
4. Structure content with: Cover → Review (if applicable) → Motivation → Concepts → Practical Exercise → Summary.
5. Use Portuguese (Brazilian) for all slide content; technical terms may remain in English.
