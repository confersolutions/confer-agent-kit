---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"        # draft | in_progress | review | done
priority: "high"       # critical | high | normal | low
type: "orchestration" # fixed for orchestrator template
labels: ["ai","orchestration"]
version: "1.0.0"
project_profile:       # optional - standardize project constants
  env: "{{ENV}}"           # dev | staging | prod
  http_port: "{{HTTP_PORT}}"     # do NOT set numeric default
  frameworks: ["{{FRAMEWORKS}}"]
  db: "{{DB}}"
  auth: "{{AUTH_SYSTEM}}"
  infra: "{{INFRA}}"
---

# Task Orchestrator Template

**Purpose:** Orchestrate arbitrary tasks in sequential or parallel mode with loop-until-done semantics. Accepts a Declared Tasks YAML block, executes child tasks with auto-numbering, tracks state, and completes only when all tasks meet their `done_when` conditions.

---

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

---

## 2. References & Inputs

External snippets/links cached in `refs/` (gitignored):

- Project profile: `./confer-agent.profile.yml`
- Orchestrator examples: `refs/orchestrator_examples.md`
- Task templates: `templates/02-dev/task_template_full.md`, `templates/02-dev/task_template_quick.md`, `templates/02-dev/bugfix.md`

---

## 3. How to Use

**Before running this orchestrator:**

1. Paste the **Declared Tasks YAML block** below into this document (replace the placeholder).
2. Ensure all referenced templates exist (check paths in `template` fields).
3. Verify `output_dir` paths are correct.
4. Review `depends_on` relationships for cycles (will be validated).

**Then execute:** The orchestrator will process the Declared Tasks block and create child task files with auto-numbering.

---

## 4. Declared Tasks (paste your task list here)

```yaml
mode: "sequential"   # or "parallel"

tasks:
  - id: "T1"
    title: "Human-readable title"
    template: "templates/02-dev/task_template_full.md"   # or quick/bugfix/etc.
    output_dir: "tasks/"
    slug: "create_orchestrator_template"                 # kebab-case, used for filename
    depends_on: []                                       # e.g., ["T0"]
    done_when:
      - "All success criteria in child task are checked"
      - "Required artifacts exist under refs/"
```

---

## 5. Execution Plan

**Step 1: DAG Building**
- Parse `depends_on` relationships from Declared Tasks
- Build dependency graph (DAG)
- Validate: if cycle detected, fail fast with clear error message
- Topological sort to determine execution order

**Step 2: Auto-Numbering Algorithm**
- Scan `output_dir` (e.g., `tasks/`) for filenames matching `^\d{3}_.*\.md$`
- Compute `next = max(NNN) + 1` (or 001 if none found)
- Zero-pad to 3 digits (001, 002, …)
- For each task, assemble filename: `tasks/${NNN}_${slug}.md`
- If collision exists, increment and retry until unique
- **Idempotency:** Re-scan before write to avoid races/collisions

**Step 3: Execution Mode**
- **Sequential:** Execute tasks in topological order, one at a time
- **Parallel:** Execute all ready tasks (no unmet `depends_on`) concurrently
- Track which tasks are ready based on dependency completion

**Step 4: Loop-Until-Done for Each Child Task**
- Create child task file with auto-numbered filename
- Fill front matter with task details from Declared Tasks
- Execute task until `done_when` conditions are satisfied:
  1. Evaluate Success Criteria checkboxes (from child task)
  2. Verify File Map & Artifacts exist (check paths in `refs/`)
  3. Check child task front matter `status` field (if present, prefer this)
  4. If conditions not met: refine implementation, retry
  5. Repeat until child status = `done`
- Update State Tracker after each iteration

**Step 5: Completion**
- Orchestrator completes only when **ALL** children are done
- Write Result Summary with completion status, artifacts, follow-ups

---

## 6. State Tracker (agent updates this table)

| Task ID | Status | Child File | Notes |
|---------|--------|------------|-------|
| T1 | pending | `tasks/NNN_slug.md` | Waiting to start |
| T2 | pending | `tasks/NNN_slug.md` | Waiting for dependency T1 |

*Status values: `pending` | `in_progress` | `done` | `failed`*

---

## 7. Result Summary (agent writes on completion)

**Overall outcome:**
- Completed tasks: X/Y
- Key artifacts produced (paths under `refs/`):
  - [artifact path 1]
  - [artifact path 2]
- Follow-ups / new tasks to open:
  - [follow-up task 1]
  - [follow-up task 2]

---

## 8. Auto-Numbering Rules

**Filename Convention:**
- Format: `{output_dir}/NNN_{slug}.md`
- NNN: Zero-padded 3-digit integer (001, 002, …)
- slug: Kebab-case identifier from Declared Tasks

**Algorithm (enforced):**
1. Scan `output_dir` for `^\d{3}_.*\.md$` pattern
2. Extract all NNN values, compute `max(NNN) + 1` (or 001 if none)
3. Zero-pad to 3 digits
4. Assemble full path: `{output_dir}/{NNN}_{slug}.md`
5. Check for collision; if exists, increment NNN and retry
6. **Idempotency:** Re-scan directory before each write operation

---

## 9. DAG Validation

**Cycle Detection:**
- Build graph from `depends_on` relationships
- Check for cycles using DFS (depth-first search)
- If cycle found, fail immediately with error:
  ```
  ERROR: Circular dependency detected in depends_on relationships:
  T1 -> T2 -> T3 -> T1
  ```

**Execution Order:**
- Use topological sort to determine valid execution order
- For parallel mode, identify ready tasks (no unmet dependencies)
- For sequential mode, execute in topological order

---

## 10. Loop-Until-Done Semantics

**For Each Child Task:**

1. **Create Task File:**
   - Apply auto-numbering to generate filename
   - Copy template from `template` field
   - Fill front matter with task details
   - Write to `{output_dir}/{NNN}_{slug}.md`

2. **Execute Until Done:**
   - Evaluate child task Success Criteria (checkboxes)
   - Verify File Map & Artifacts exist (paths in `refs/`)
   - Check child task front matter `status` field (preferred if present)
   - If all `done_when` conditions met → mark child as `done`
   - If not satisfied → refine implementation, update child task, retry
   - Repeat loop until child is `done`

3. **Status Detection Priority:**
   1. Child task front matter `status: "done"` (highest priority)
   2. All Success Criteria checkboxes checked
   3. All required artifacts exist in `refs/`
   4. All `done_when` conditions verified

**Orchestrator Completion:**
- Only mark orchestrator `done` when **ALL** children have status = `done`
- Write Result Summary before completing

---

## 11. File Map & Artifacts

**Child Task Artifacts (expected in `refs/`):**
- Screenshots: `refs/proof/*.png`
- Logs: `refs/logs/*.txt`
- Test reports: `refs/test-results/*.json`
- Documentation: `refs/docs/*.md`
- Data exports: `refs/exports/*.csv`

**Orchestrator Artifacts:**
- State Tracker table (updated during execution)
- Result Summary (written on completion)
- Child task files: `tasks/NNN_{slug}.md` (auto-numbered)

---

## 12. Testing/Verification Checklist

- ☐ Auto-numbering produced `tasks/NNN_<slug>.md`
- ☐ Sequential mode respected dependencies
- ☐ Parallel mode ran ready tasks concurrently
- ☐ Loop stopped only when all children met `done_when`
- ☐ No hard-coded infra values; profile referenced
- ☐ DAG validation detected cycles correctly
- ☐ State tracking updated correctly
- ☐ Result summary written on completion
- ☐ Child task files created with correct numbering
- ☐ No literal date placeholders remain; created_at and updated_at are populated as above.

---

## 13. AI Agent Actions & Guardrails

**Actions:** 
- Resolve date placeholders: created_at = today (America/Chicago, YYYY-MM-DD); updated_at = now (ISO8601 with offset). Do not leave placeholders.
- Parse Declared Tasks YAML block
- Build DAG from `depends_on` and validate for cycles
- Apply auto-numbering algorithm for each child task
- Create child task files from templates
- Execute loop-until-done semantics for each child
- Update State Tracker after each iteration
- Write Result Summary when all children complete

**Guardrails:**
- Resolve all {{TOKEN}} placeholders at instantiation time; leave none unresolved.
- Set `created_at` = {{AUTO:DATE:America/Chicago}}, `updated_at` = {{AUTO:DATETIME_ISO:America/Chicago}}.
- Replace only in YAML/TODO fields; never inject {{TOKEN}} into runtime code.
- Do not modify existing templates or task files unnecessarily
- Keep child tasks aligned with house style (Context Capsule, References & Inputs, etc.)
- Follow existing template formatting rules
- Re-scan directory before each auto-numbering operation (idempotency)
- Fail fast on cycle detection or missing dependencies
- Only mark orchestrator done when ALL children are done
- No literal date placeholders remain; created_at and updated_at are populated as above.

---

## Links

**Related:** [01_master_idea.md](../01-prep/01_master_idea.md), [09_build_order.md](../01-prep/09_build_order.md), [08_system_design.md](../01-prep/08_system_design.md)

