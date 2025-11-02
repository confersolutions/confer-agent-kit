# Template Commands Reference

**Purpose:** Quick guide on how to invoke templates with AI agents. Works with any AI coding assistant (Cursor, Claude Code, Windsurf, etc.).

---

## How to Use Templates

**Direct Reference:**
```
"Help me implement this task: tasks/001_add_user_auth.md"
```

**Copy Template:**
```
"I need to add authentication. Here's my task plan:

[paste filled template]

Please implement this following the plan."
```

**Template + Standards:**
```
"Implement this following tasks/002_api_endpoints.md. 
Use patterns from standards/backend.md for API design."
```

---

## Common Patterns

**Feature:** `cp templates/02-dev/task_template_quick.md tasks/001_feature.md` → Fill Context Capsule → Share: `"Help me complete: tasks/001_feature.md"`

**Bug Fix:** `cp templates/02-dev/bugfix.md tasks/002_fix.md` → Document reproduction → Share: `"Fix this bug: tasks/002_fix.md"`

**Testing:** `cp templates/02-dev/testing_checklist.md tasks/003_test.md` → Fill test scope → Share: `"Create tests per: tasks/003_test.md"`

---

## Examples by Tool

**Cursor:** `@tasks/001_feature.md Help me implement this task`

**Claude Code / Windsurf:** `"Here's my task template: tasks/001_feature.md. Please implement it."`

---

## Tips

- Fill Context Capsule from `./confer-agent.profile.yml`
- Reference standards in "References & Inputs"
- Quick template for <2 hours; full template for complex features
- Update status: `draft → in_progress → review → done`

---

**Related:** [README.md](../../README.md), [TEMPLATE_INDEX.md](../../TEMPLATE_INDEX.md)
