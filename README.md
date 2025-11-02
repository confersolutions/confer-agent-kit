# Confer Agent Kit

**AI-first templates for planning, building, fixing, and shipping — fast, consistent, and project-agnostic.**

---

## Overview

Confer Agent Kit is a modular template library designed for AI-assisted software development. Use it in new or existing repositories to standardize workflows, ensure consistency, and accelerate delivery.

**What this is:**

- A modular template kit used in new or existing repos
- Standard schema across templates (YAML front matter → Context Capsule → References & Inputs → File Map & Artifacts → AI Actions & Guardrails)
- Project-agnostic by design: no hard-coded infra; all specifics come from a per-project profile

**What this is not:**

- A framework or runtime dependency
- Tied to specific infrastructure or frameworks
- A replacement for project documentation

---

## Quick Start

1. **Copy the profile template:** Copy `confer-agent.profile.example.yml` into your project as `confer-agent.profile.yml`, then fill in your project-specific values.

2. **Optional local overrides:** Create `confer-agent.profile.local.yml` for dev overrides (gitignored).

3. **Browse templates:** Open `TEMPLATE_INDEX.md` and pick a template (e.g., Task Quick for rapid coding tasks).

4. **Generate a task:** Create a new task using a template — it will auto-number into `tasks/NNN_<slug>.md`.

---

## Per-Project Profile

All templates reference a per-project configuration profile to remain project-agnostic. **Never hard-code ports, environments, frameworks, or infrastructure in templates.**

### Profile Files

**`confer-agent.profile.yml`** (checked in, project-specific)
- Contains project-specific configuration (ports, frameworks, auth, infra)
- Copy from `confer-agent.profile.example.yml` and fill in your values
- This file belongs in your project repository
- All templates reference this file via `./confer-agent.profile.yml`

**`confer-agent.profile.local.yml`** (gitignored, local overrides)
- Optional local overrides for development
- Not committed to the repository
- Use for dev-only ports, local service URLs, or personal preferences

### Profile Schema

```yaml
env: dev              # dev | staging | prod
http_port: TBD        # Backend API port (set based on your infra)
frameworks: ["TBD"]   # e.g., ["next@14", "fastapi@0.115"]
db: "TBD"             # e.g., "postgres+drizzle"
auth: "TBD"           # e.g., "clerk"
infra: "TBD"          # e.g., "coolify|vercel|replit"
notes: "This file is per-project. Templates reference it."
```

Templates use placeholders like `{{ENV}}`, `{{HTTP_PORT}}` and reference the profile values dynamically.

---

## Folder Structure

```
templates/
  01-prep/          # Project kickoff → build order
                    # master idea, naming, UI theme, pages, wireframes, data models, system design, build order
  02-dev/           # Daily coding workflow
                    # task templates (full/quick), bugfix, PR review, cleanup, update workflow
  03-ui/            # UI/design aids
                    # color, landing page, diagrams
  04-db/            # DB tooling
                    # migrations, rollback
  05-advanced/       # Orchestration, agent design, specialized workflows
                    # orchestration, agent design playbook, Python tasks, ADK workflows
  06-infra/         # Infrastructure runbooks
                    # platform runbooks (Coolify, Vercel, Replit, n8n, Flowise, Qdrant, Neo4j) + conventions

tasks/              # Auto-numbered tasks (NNN_slug.md)
refs/               # Evidence (screenshots, logs, CSVs) — gitignored
secrets/            # .env.local patterns — gitignored
```

**Note:** Zero-padded folder names (01-, 02-, etc.) ensure stable sorting. Adjust numbers/names to match your repo if you've customized them.

---

## Template Schema

All templates follow a consistent structure for machine parsing and AI agent execution:

### 1. YAML Front Matter

Metadata block at the top of each template:

```yaml
---
task_id: "uuid-here"
created_by: "user.name"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
status: "draft"        # draft | in_progress | review | done
priority: "high"       # critical | high | normal | low
type: "feature"        # feature | bugfix | enhancement | etc.
labels: ["ai","template"]
version: "1.0.0"
project_profile:       # optional - standardize project constants
  env: "TBD"           # dev | staging | prod
  http_port: "TBD"     # do NOT set numeric default
  frameworks: ["TBD"]
  db: "TBD"
  auth: "TBD"
  infra: "TBD"
---
```

**Important:** Never use numeric defaults in templates; use `"TBD"` and reference `./confer-agent.profile.yml`.

### 2. Context Capsule

Copy-paste constants section referencing the project profile:

```markdown
## 1. Context Capsule

**Copy-paste constants for this task:**

- **Project:** [project-name]
- **Runtime profile:** {{ENV}} *(alt: staging | prod)*
- **Default ports:** HTTP={{HTTP_PORT}} (set in project profile)
- **Frameworks:** Frontend=[name@ver], Backend=[name@ver]
- **DB/ORM:** [e.g., Postgres + Drizzle]
- **Auth:** [e.g., Clerk]
- **Infra:** [e.g., Coolify on VPS; Vercel preview for PRs]
- **Secrets location (local only):** `[project-name]/secrets/.env`
- **Project profile:** `./confer-agent.profile.yml` (and optional `./confer-agent.profile.local.yml`)
- **Non-negotiables:** Do NOT change ports without updating the project profile and ingress config.
```

### 3. References & Inputs

External snippets/links cached in `refs/` (gitignored):

```markdown
## 2. References & Inputs

External snippets/links cached in `refs/` (gitignored):

- Project profile: `./confer-agent.profile.yml`
- Task templates: `templates/02-dev/task_template_full.md`, `templates/02-dev/task_template_quick.md`
```

### 4. File Map & Artifacts

Explicit "must exist" outputs:

```markdown
## File Map & Artifacts

**Files to touch:**
- `path/to/file.md` (new) → must exist with [requirements]
- `path/to/other.ts` (update) → must include [feature]

**Artifacts:**
- Screenshot: `refs/ui_before_after.png`
- Test report: `refs/test_coverage.html`
```

### 5. AI Actions & Guardrails

Short, machine-parsable instructions:

```markdown
## AI Agent Actions & Guardrails

**Actions:**
- Generate [specific output] at [path]
- Update [file] to include [feature]
- Verify [condition] before proceeding

**Guardrails:**
- Do not [specific constraint]
- Keep [alignment requirement]
- Ensure [validation rule]
```

---

## Auto-numbering Rule

All new tasks must follow the auto-numbering convention to maintain order and prevent conflicts.

### Filename Convention

New tasks must be named `tasks/NNN_<kebab-slug>.md` where:
- `NNN` is a zero-padded 3-digit integer (001, 002, 003, ...)
- `<kebab-slug>` is a lowercase, hyphenated identifier (e.g., `create-auth-system`)

### Algorithm

1. **Scan** `tasks/` directory for filenames matching `^\d{3}_.*\.md$`
2. **Compute** `next = max(NNN) + 1` (or `001` if none found)
3. **Zero-pad** to 3 digits and assemble `tasks/${NNN}_${slug}.md`
4. **Re-scan** before writing to avoid collisions
5. **Idempotency:** Auto-numbering MUST re-scan before write to avoid races/collisions

### Example

If `tasks/` contains:
- `001_setup_auth.md`
- `002_add_login.md`
- `005_refactor_api.md`

The next task with slug `add_logout` will be created as `tasks/006_add_logout.md` (max is 005, so next is 006).

---

## Orchestrator

Run multiple tasks sequentially or in parallel with dependency management.

### Template Location

`templates/05-advanced/task_orchestrator.md`

### Usage

1. Open the orchestrator template
2. Paste a **Declared Tasks** YAML block into the document:

```yaml
mode: "sequential"   # or "parallel"

tasks:
  - id: "T1"
    title: "Human-readable title"
    template: "templates/02-dev/task_template_full.md"   # or quick/bugfix/etc.
    output_dir: "tasks/"
    slug: "my_task_slug"
    depends_on: []                                       # e.g., ["T0"]
    done_when:
      - "All success criteria in child task are checked"
      - "Required artifacts exist under refs/"
  - id: "T2"
    title: "Another task"
    template: "templates/02-dev/task_template_quick.md"
    output_dir: "tasks/"
    slug: "related_task"
    depends_on: ["T1"]                                  # Runs after T1
    done_when:
      - "Child task status is 'done'"
```

### How It Works

The orchestrator:

1. **Builds a DAG** from `depends_on` relationships
   - Validates for cycles (fails fast if detected)
   - Topologically sorts tasks for execution order

2. **Auto-numbers child tasks**
   - Applies the auto-numbering algorithm to each child
   - Creates files like `tasks/007_my_task_slug.md`

3. **Executes tasks**
   - **Sequential mode:** Runs tasks one by one, respecting dependencies
   - **Parallel mode:** Runs all "ready" tasks (no unmet dependencies) concurrently

4. **Loops until done**
   - For each child task, evaluates `done_when` conditions
   - If not satisfied, refines/retries the child task
   - Repeats until child task status is `done`
   - Child status detection: prefers child task front matter `status` field; if absent, infers from success criteria checkboxes + artifact existence

5. **Completes only when all children are done**
   - Orchestrator finishes only when ALL child tasks meet their `done_when` conditions

6. **Writes a Result Summary**
   - Reports overall outcome, completed tasks count, key artifacts, and follow-ups

---

## Common Workflows

### Plan a Project

1. Start with `01-prep/01_master_idea.md` → define vision, metrics, roadmap
2. Continue through `02_app_name.md` → `03_ui_theme.md` → ... → `09_build_order.md`
3. Generate artifacts: wireframes, data models, system design documents

### Ship a Unit of Work

1. Use `02-dev/task_template_quick.md` for rapid tasks or `task_template_full.md` for comprehensive features
2. Fill in Context Capsule, References & Inputs
3. Code, test, and generate artifacts (screenshots, logs) in `refs/`
4. Mark success criteria as complete

### Fix a Bug

1. Use `02-dev/bugfix.md` template
2. Document reproduction steps
3. Implement patch
4. Validate with tests/verification checklist
5. Generate artifacts (before/after screenshots, test results)

### Set Up Infrastructure

1. Read `06-infra/00_infra_conventions.md` for canonical conventions
2. Follow platform-specific runbooks (Coolify, Vercel, Replit, n8n, Flowise, Qdrant, Neo4j, etc.)
3. Reference project profile for ports, env vars, and secrets
4. Document setup steps and generate `refs/` artifacts

### Orchestrate Multiple Tasks

1. Use `05-advanced/task_orchestrator.md`
2. Define Declared Tasks YAML with dependencies
3. Choose sequential or parallel mode
4. Let orchestrator create and manage child tasks
5. Review Result Summary on completion

---

## Conventions & Gotchas

### ✅ Do

- **Use the project profile** for all infrastructure values (ports, env, frameworks)
- **Place artifacts** in `refs/` directory (screenshots, logs, CSVs)
- **Store secrets** in `secrets/` or platform environment variables
- **Keep commits scoped** to single tasks or logical units
- **Update TEMPLATE_INDEX.md** when adding new templates
- **Follow auto-numbering** for all new tasks
- **Re-scan before write** to avoid numbering collisions

### ❌ Don't

- **Never hard-code ports/infra** in templates; use the per-project profile
- **Don't commit** `confer-agent.profile.local.yml` or files in `refs/`, `secrets/`
- **Don't skip** auto-numbering (manual numbering causes conflicts)
- **Don't bypass** DAG validation in orchestrator (cycles will break execution)

---

## Contributing

### Style Guide

- **Concise:** Use machine-parsable tables and checkboxes; minimal emojis
- **Consistent:** Keep the schema consistent across templates
- **Placeholders:** Prefer placeholders (`TBD`, `{{ENV}}`) over examples
- **Explicit:** Clearly state what must exist vs. what's optional

### Template Standards

- Follow the standard template schema (Front Matter → Context Capsule → ... → AI Actions & Guardrails)
- Reference `./confer-agent.profile.yml` in Context Capsule
- Use zero-padded folder names for stable sorting
- Include a "Testing/Verification checklist" section

### Process

1. Pick a template from `TEMPLATE_INDEX.md` or create a new one
2. Ensure it follows the schema and conventions
3. Add yourself to the changelog in your PR
4. Update `TEMPLATE_INDEX.md` if adding a new template

---

## License

[Add license info or link if applicable.]

---

## Resources

- **Template Index:** See `TEMPLATE_INDEX.md` for all available templates organized by category
- **Profile Example:** See `confer-agent.profile.example.yml` for profile schema
- **Orchestrator:** See `templates/05-advanced/task_orchestrator.md` for multi-task execution
