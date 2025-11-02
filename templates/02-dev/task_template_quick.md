---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"
priority: "high"
type: "feature"
labels: ["ai","backend"]
version: "1.0.0"
project_profile:       # optional - standardize project constants
  env: "{{ENV}}"           # dev | staging | prod
  http_port: "{{HTTP_PORT}}"     # do NOT set numeric default
  frameworks: ["{{FRAMEWORKS}}"]
  db: "{{DB}}"
  auth: "{{AUTH_SYSTEM}}"
  infra: "{{INFRA}}"
---

# AI Task Template — Quick Edition

**Purpose:** Streamlined template for fast tasks (<2 hours). Use this for simple bugfixes, small enhancements, or straightforward features.

---

## Task Overview

**Title:** TODO: short, action-based title

**Goal:** One sentence explaining what success looks like.

**Priority:** ☐ Critical  ☐ High  ☐ Normal  ☐ Low  
**Type:** ☐ Feature  ☐ Enhancement  ☐ Bugfix  ☐ Research  ☐ Refactor

---

## Context Capsule

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

## References & Inputs

External snippets/links cached in `refs/` (gitignored):

- Project profile: `./confer-agent.profile.yml`
- Product brief: `refs/auth-brief.md`
- API notes: `refs/oauth-notes.md`
- Diagram: `refs/arch.mmd`

---

## Context & Problem

- Current state: what exists today (1-2 bullets)
- What's broken or missing (1-2 bullets)
- Who's impacted (1 bullet)

---

## Functional Requirements

- User scenario: "When X → system Y" (bullets)
- System behavior: triggers, edge cases (bullets)
- Non-functional note (if critical): performance target or security requirement

---

## Plan (Mini)

**Step 1:** ...  
**Step 2:** ...  
**Step 3:** ...

**Dependencies:** Other tasks/PRs (if any, 1 line)  
**Rollback:** How to revert (1 line)

---

## File Map & Artifacts

**Files to touch:**
- `/db/migrations/2025-11-01_add_referral_code.sql` (new) → must exist
- `/src/api/auth.ts` (update) → add `exchangeToken()`; include JSDoc
- `/path/to/file2.ts` (update)

**Artifacts:**
- Screenshot of successful OAuth redirect saved at `refs/proof/oauth-success.png`

**Testing:**
- ☐ Unit test for [key function]
- ☐ Integration test for [key flow]
- ☐ Manual QA: [URL/creds, happy path]
- ☐ Manual QA: [error case]

**Acceptance Criteria:**
- ☐ No literal date placeholders remain; created_at and updated_at are populated as above.

---

## AI Agent Actions & Guardrails

**Actions:**
- Resolve date placeholders: created_at = today (America/Chicago, YYYY-MM-DD); updated_at = now (ISO8601 with offset). Do not leave placeholders.
- Generate minimal diff
- Add 1-2 unit tests
- Update docs section

**Guardrails:**
- Resolve all {{TOKEN}} placeholders at instantiation time; leave none unresolved.
- Set `created_at` = {{AUTO:DATE:America/Chicago}}, `updated_at` = {{AUTO:DATETIME_ISO:America/Chicago}}.
- Replace only in YAML/TODO fields; never inject {{TOKEN}} into runtime code.
- Do not change unrelated files
- Keep commits scoped
- Follow existing lint rules
- No literal date placeholders remain; created_at and updated_at are populated as above.

