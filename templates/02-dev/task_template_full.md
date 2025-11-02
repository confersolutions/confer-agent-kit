---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"        # draft | in_progress | review | done
priority: "high"       # critical | high | normal | low
type: "feature"        # feature | enhancement | bugfix | research | refactor
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

# AI Task Template — Full Edition

**Purpose:** A comprehensive framework for AI-assisted task planning and execution. Use this for complex features, refactors, or multi-phase work where thorough context ensures consistent AI reasoning and implementation.

---

## 1. Task Overview

**Title:** TODO: short, action-based title

**Goal:** Explain what success looks like and why it matters (1-2 sentences, outcome-oriented).

| Priority | Type |
|----------|------|
| ☐ Critical  ☐ High  ☐ Normal  ☐ Low | ☐ Feature  ☐ Enhancement  ☐ Bugfix  ☐ Research  ☐ Refactor |

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
- Product brief: `refs/auth-brief.md`
- API notes: `refs/oauth-notes.md`
- Diagram: `refs/arch.mmd`

---

## 4. Context (Current State)

**Summary:** What exists today? What relevant tech is in use? Any known constraints or limitations?

| Layer | Notes |
|-------|-------|
| Frontend | framework + version |
| Backend | framework + version |
| Database | type/ORM + impacted tables |
| Auth/Security | method + notes |
| Infra | Coolify/Vercel/GCP etc. |

---

## 5. Problem & Success

**Problem:** What's missing or broken? Who's impacted?

**Success Criteria:**
- ☐ Clear, measurable outcome
- ☐ Performance or UX goal met
- ☐ All tests passing
- ☐ Documentation updated
- ☐ Peer review approved
- ☐ No literal date placeholders remain; created_at and updated_at are populated as above.

---

## 6. Development Mode & Constraints

**Mode:** ☐ Greenfield  ☐ Integration  ☐ Refactor  ☐ Migration

**Constraints:**
- ☐ Breaking changes allowed?
- ☐ New dependencies allowed?
- ☐ Data loss allowed?
- ☐ External API changes allowed?
- ☐ Backward compatibility required?

---

## 7. Functional Requirements

**User Scenarios:**
- "When user does X → system should Y"
- "If condition Z → show message Q"
- ...

**System Behaviors:**
- Triggers, background jobs, scheduled tasks
- Permissions or edge cases to enforce
- Event listeners or webhooks
- ...

---

## 8. Non-Functional & Compliance (Optional)

**Performance:** Target latency / throughput

**Security:** Data sensitivity, encryption, RBAC needs

**Accessibility:** Responsive design, dark mode, a11y goals

**Observability:** Logging, monitoring, alerting requirements

---

## 9. Data & API Changes

**Schema / Model Updates:**
```sql
-- Example
ALTER TABLE users ADD COLUMN referral_code TEXT;
```

**API Contracts:**
- Endpoint(s) impacted or added
- Expected payloads / responses
- Versioning strategy

---

## 10. Frontend Impact (Optional)

**Components to add / modify:** ...

**Pages touched:** ...

**State management notes:** store, context, signals, etc.

**Visual references:** Figma links, diagram URLs

---

## 11. Plan & Phases

| Phase | Description | Prerequisites/Dependencies | Est. Time |
|-------|-------------|---------------------------|-----------|
| 1 | Setup + scaffolding | | |
| 2 | Core logic | | |
| 3 | Integration + testing | | |
| 4 | Review + merge | | |

---

## 12. Dependencies

- Other tasks/PRs that must complete first (links/IDs)
- External services or APIs required
- Team coordination needs

---

## 13. Rollback Plan

How to safely revert if something breaks:
- Code rollback steps
- Database migration rollback
- Data recovery procedure
- Feature flag disable method

---

## 14. File Map & Artifacts

Exact files to create or update, plus required artifacts:

- `/db/migrations/2025-11-01_add_referral_code.sql` (new) → must exist
- `/src/api/auth.ts` (update) → add `exchangeToken()`; include JSDoc
- `/src/components/SignupForm.tsx` (new)
- **Artifact:** screenshot of successful OAuth redirect saved at `refs/proof/oauth-success.png`

---

## 15. Testing Checklist

**Unit Tests:**
- ☐ What to cover (list key scenarios)
- ☐ ...

**Integration Tests:**
- ☐ What paths/fixtures (endpoints, flows)
- ☐ ...

**Manual QA:**
- ☐ URLs, test credentials, happy path
- ☐ Sad path / error cases
- ☐ Browser/device testing if applicable

---

## 16. AI Agent Actions & Guardrails

**Actions:**
- Resolve date placeholders: created_at = today (America/Chicago, YYYY-MM-DD); updated_at = now (ISO8601 with offset). Do not leave placeholders.
- Generate minimal diff
- Add 2 unit tests
- Update docs section

**Guardrails:**
- Resolve all {{TOKEN}} placeholders at instantiation time; leave none unresolved.
- Set `created_at` = {{AUTO:DATE:America/Chicago}}, `updated_at` = {{AUTO:DATETIME_ISO:America/Chicago}}.
- Replace only in YAML/TODO fields; never inject {{TOKEN}} into runtime code.
- Do not change unrelated files
- Keep commits scoped
- Follow existing lint rules
- No literal date placeholders remain; created_at and updated_at are populated as above.

---

## 17. Wrap-Up / Reflection (Optional)

**What changed:** Quick summary of actual implementation vs. plan

**Lessons:** Notes for future tasks (what worked, what didn't)

**Follow-ups:** Related tasks or improvements to consider

---

