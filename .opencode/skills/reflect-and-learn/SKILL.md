---
name: reflect-and-learn
description: Post-task reflection protocol — evaluate what was learned and update skills proactively
---

Post-task reflection protocol. Run this after completing any non-trivial task (editing slides, debugging, adding features, migrating code, etc.).

## Trigger
After completing a task that involved: debugging, discovering workarounds, learning new API patterns, finding gotchas, or doing anything that took more than 3 tool calls to resolve.

## Protocol

### Step 1: Reflect
Ask yourself these questions about the task just completed:

1. **Gotchas encountered?** Did anything fail in a non-obvious way? (e.g., mermaid edge label syntax, HTML parser mangling)
2. **New patterns discovered?** Did you find a reusable solution pattern? (e.g., mountSlideApp() override for Vue reactive state)
3. **Library-specific knowledge?** Did you learn API details that aren't obvious from docs? (e.g., AsyncTelegram2's MessageQuery type, endQuery() requirement)
4. **Errors in existing skills/docs?** Did you find outdated or incorrect info in AGENTS.md, SKILL.md, or ECOSSISTEMA.md?
5. **Process improvements?** Did you discover a better workflow? (e.g., compile-testing Arduino code with PlatformIO before finalizing)

### Step 2: Evaluate
If ANY answer is "yes", determine where this knowledge belongs:

| Knowledge Type | Where to Store |
|---------------|----------------|
| Slide creation gotcha (HTML, Mermaid, Reveal.js, Vue) | `.opencode/skills/create-slides/SKILL.md` → "Gotchas & Tips" section |
| New reusable pattern for slides | `.opencode/skills/create-slides/SKILL.md` → appropriate section |
| Library/API reference for a specific tech | `.opencode/skills/create-slides/SKILL.md` → "Gotchas & Tips" (if slide-related) or new skill if broad enough |
| Project-level workflow or convention | `AGENTS.md` |
| Component/plugin documentation | `docs/ECOSSISTEMA.md` |
| Generic reusable skill (image search, plotting, notebooks) | New skill in `.opencode/skills/<name>/SKILL.md` |

### Step 3: Act
- **Update existing skill**: Edit the relevant SKILL.md or AGENTS.md section. Add concise, actionable entries — not prose.
- **Create new skill**: Only if the knowledge is self-contained and reusable across sessions (e.g., a new tool, a new workflow). Use the skill directory structure: `.opencode/skills/<name>/SKILL.md` with frontmatter.

### Step 4: Notify
Tell the user briefly what you learned and where you stored it. Example:
> Learned that Mermaid edge labels break with inner quotes. Added to create-slides skill gotchas.

## Rules
- **Be proactive** — don't wait for the user to ask. Do this automatically after non-trivial tasks.
- **Be concise** — add bullet points, not paragraphs. Skills should be scannable.
- **Don't duplicate** — check existing skill content before adding.
- **Don't over-skill** — don't create a new skill for one-off knowledge that belongs in an existing skill.
- **Keep AGENTS.md lean** — only add project-wide conventions there, not implementation details.
