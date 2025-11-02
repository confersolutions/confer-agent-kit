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

External snippets/links cached in `output/` (gitignored):

- Project profile: `./confer-agent.profile.yml`
- Logs: `output/logs/oauth-callback.txt`
- Screenshot: `output/proof/oauth-error.png`
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

**Data Access Impact (if applicable):**
- Which mutations/queries are affected? [if backend bug]
- Code location per project patterns: [where the fix goes]

---

## 6. Fix Plan

| Step | Description | Prerequisites/Dependencies |
|------|-------------|----------------------------|
| 1    |             |                            |
| 2    |             |                            |
| 3    |             |                            |

**Rollback (one line):** how to revert safely (code + data).

**Side Effects Check:**
- Could this fix break other code? [related functions/components]
- Performance impact? [queries, rendering, etc.]
- User workflow changes? [if fix changes UX]

---

## 7. File Map & Artifacts

- `/src/api/auth.ts` (update) → fix `exchangeToken()`; add JSDoc
- `/db/migrations/2025-11-01_revert_bad_constraint.sql` (new) → must exist

**Artifacts required:**
- Screenshot of successful flow → `output/proof/oauth-success.png`

---

## 8. Tests & Validation

**Unit:** ☐ covers failing branch  ☐ edge case covered

**Integration:** ☐ end-to-end flow passes  ☐ error path verified

**Manual QA:** URL + creds; happy path; sad path; multi-browser (if applicable)

**Regression Protection:** ☐ Added test to cover this scenario permanently

---

## 9. AI Agent Actions & Guardrails

**Implementation Workflow:**
- Review reproduction steps and root cause before fixing
- Follow fix plan sequentially (Section 6)
- Update progress in real-time (see below)
- Verify all Tests & Validation criteria (Section 8) before completion

**Actions:**
- **Update progress:** Mark front matter `status` as work progresses (draft → in_progress → review → done). Update Tests & Validation checkboxes when satisfied.
- Generate minimal diff
- Add targeted unit test(s)
- Update docs line in this file

**Communication Preferences:**
- Update status and checkboxes in real-time as work completes
- If blocked during fix, note it in Side Effects Check (Section 6) or Triage section
- Document fix decisions immediately
- Flag questions explicitly rather than making assumptions

**Code Quality Standards:**
- Follow existing project lint rules and formatting
- Include proper error handling for fix
- Add regression protection test (Section 8)
- Follow data access pattern rules if backend changes (per project structure)

**Guardrails:**
- Do not modify unrelated files
- Keep commits scoped
- Follow existing lint rules
- Follow data access pattern rules if backend changes (per project structure)

