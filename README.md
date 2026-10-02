# Personal Claude Skills

A collection of Claude skills — both found online and personally created.

## How Skills Work

Skills are defined in Markdown files and placed in your Claude config directory:

```
%USERPROFILE%\.claude\skills\<skill-name>\SKILL.md
```

## Skills

<!-- - **skill-name** ([Source](url)) — brief remarks -->

- **docx** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — Word doc creation and manipulation
- **frontend-design** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — High-quality UI/frontend generation
- **mcp-builder** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — MCP server scaffolding
- **pdf** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — PDF read, create, merge, split
- **pptx** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — PowerPoint creation and editing
- **skill-creator** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — Build and evaluate new skills
- **theme-factory** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — Apply visual themes to artifacts
- **webapp-testing** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — Playwright-based local app testing
- **writing-tropes** ([tropes.fyi](https://tropes.fyi/), [skill](writing-tropes/SKILL.md)) — Write and review project prose with the bundled AI writing trope catalog
- **xlsx** ([anthropics/claude-skills](https://github.com/anthropics/claude-skills)) — Spreadsheet creation and editing

To use `writing-tropes` in a project, copy the entire `writing-tropes/` folder into `.claude/skills/` for Claude Code or `.agents/skills/` for Codex. Keep `references/` with `SKILL.md`; `agents/openai.yaml` supplies optional Codex UI metadata. Invoke it with `$writing-tropes`, for example: "Use $writing-tropes to revise this README while preserving the technical details."

### Personal Skills

- **professional-readme-architect** (personal) — Generate/rewrite READMEs following Art of README and Standard README philosophies; strips AI filler, enforces information density
- **technical-doc-architect** (personal) — Structure technical docs using the Diátaxis framework (Tutorial/How-to/Reference/Explanation); optimized for cybersecurity, infrastructure, and Obsidian/Git rendering
