---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"            # draft | in_progress | review | done
priority: "high"           # critical | high | normal | low
type: "bugfix"             # fixed value for this template
labels: ["ai","bugfix"]
version: "1.0.0"          # increment only if bugfix template structure changes
project_profile:           # optional - standardize project constants
  env: "{{ENV}}"               # dev | staging | prod
  http_port: "{{HTTP_PORT}}"         # do NOT set numeric default
  frameworks: ["{{FRAMEWORKS}}"]
  db: "{{DB}}"
  auth: "{{AUTH_SYSTEM}}"
  infra: "{{INFRA}}"
---

# Bugfix Template — Confer-Agent Edition

**Purpose:** A concise, AI-first bug remediation template that standardizes reproduce → analyze → patch → validate → prevent regressions.

---

## 1. Summary

One line describing the defect and user impact.

**Example:** "OAuth callback fails on Chrome; users remain on /login."

**Severity:** ☐ Critical  ☐ Major  ☐ Minor  ☐ Cosmetic

---

## 2. Context Capsule

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

## 3. References & Inputs

External snippets/links cached in `refs/` (gitignored):

- Project profile: `./confer-agent.profile.yml`
- Logs: `refs/logs/oauth-callback.txt`
- Screenshot: `refs/proof/oauth-error.png`
- Related task/PR: [ID or link]

---

## 4. Reproduction (Deterministic)

**Environment:** [browser/os/device], **Branch:** [name], **Seed data:** [if any]

1. Step…
2. Step…
3. Step…

**Expected:** …

**Actual:** …

---

## 5. Triage & Root Cause (Brief)

- Hypothesis / finding #1
- Minimal failing path or function
- Scope of impact (feature flags? tenants? roles?)

---

## 6. Fix Plan

| Step | Description | Prerequisites/Dependencies |
|------|-------------|----------------------------|
| 1    |             |                            |
| 2    |             |                            |
| 3    |             |                            |

**Rollback (one line):** how to revert safely (code + data).

---

## 7. File Map & Artifacts

- `/src/api/auth.ts` (update) → fix `exchangeToken()`; add JSDoc
- `/db/migrations/2025-11-01_revert_bad_constraint.sql` (new) → must exist

**Artifacts required:**
- Screenshot of successful flow → `refs/proof/oauth-success.png`

---

## 8. Tests & Validation

**Unit:** ☐ covers failing branch  ☐ edge case covered

**Integration:** ☐ end-to-end flow passes  ☐ error path verified

**Manual QA:** URL + creds; happy path; sad path; multi-browser (if applicable)

**Regression Protection:** ☐ Added test to cover this scenario permanently

---

## 9. AI Agent Actions & Guardrails

**Actions:** generate minimal diff; add targeted unit test(s); update docs line in this file.

**Guardrails:** do not modify unrelated files; keep commits scoped; follow existing lint rules.

