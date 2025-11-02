# Standards — Optional Guidance

**Purpose:** Lightweight coding standards organized by domain. Use these checklists and examples as needed; they're optional guidance, not mandates.

---

## Overview

Standards files provide checklists and examples for common coding patterns. Reference them when filling templates or asking AI to implement features.

**Files:**
- [`global.md`](global.md) — Naming, logging, errors, docs, tokens
- [`backend.md`](backend.md) — API patterns, DTOs, validation, error mapping
- [`frontend.md`](frontend.md) — Component structure, state management, accessibility

---

## How to Reference Standards

### When Filling Templates

Add standards to your task template's "References & Inputs":

```markdown
- Coding standards: `standards/backend.md` (API patterns, DTOs)
- Project profile: `./confer-agent.profile.yml`
```

### When Working with AI

Include standards in your prompts:

```
"Implement this API endpoint following patterns from standards/backend.md"
```

Or reference in context:

```
"Review this code against standards/frontend.md for component structure"
```

---

## Quick Reference

| Standard | Use When | Key Topics |
|----------|----------|------------|
| `global.md` | Any code | Naming, logging, errors, docs |
| `backend.md` | APIs, services | DTOs, validation, error mapping |
| `frontend.md` | UI components | Component structure, state, accessibility |

---

## Profile Reference

Always reference `./confer-agent.profile.yml` for project constants:
- Framework versions: `{{FRAMEWORKS}}`
- Database: `{{DB}}`
- Environment: `{{ENV}}`
- HTTP port: `{{HTTP_PORT}}`

**Never hard-code** infrastructure values in templates or code.
