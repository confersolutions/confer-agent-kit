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

### Technology & Architecture

- **Frameworks & Versions:** [e.g., Next.js 14.2, FastAPI 0.115, React 18.3]
- **Language:** [e.g., TypeScript 5.3, Python 3.11]
- **Database & ORM:** [e.g., Postgres 15 + Drizzle ORM 0.29]
- **UI & Styling:** [e.g., Tailwind CSS 3.4, shadcn/ui components]
- **Authentication:** [e.g., Clerk Auth v5]
- **Key Architectural Patterns:** [e.g., Server Actions, RPC pattern, Repository pattern]

### Current State

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

### Performance
- **Response Time:** Target latency / throughput requirements
- **Load Handling:** Expected concurrent users / requests
- **Optimization:** Caching strategies, query optimization needs

### Security
- **Authentication:** Authentication and data protection needs
- **Data Sensitivity:** Encryption requirements, RBAC needs
- **Input Validation:** Data sanitization and validation requirements

### Usability
- **User Experience:** User experience and accessibility standards
- **Accessibility (a11y):** WCAG compliance, screen reader support
- **Error Messages:** User-friendly error handling and messaging

### Responsive Design
- **Mobile Support:** Mobile, tablet, desktop support requirements
- **Breakpoints:** Responsive breakpoints and layout requirements
- **Touch Interactions:** Touch-friendly UI elements where applicable

### Theme Support
- **Light/Dark Mode:** Light/dark mode requirements
- **Brand Requirements:** Color schemes, theming constraints

### Observability
- **Logging:** Logging, monitoring, alerting requirements
- **Metrics:** Key performance indicators to track
- **Debugging:** Debugging and troubleshooting requirements

---

## 9. Data & API Changes

**Data Access Pattern Rules:**
- **Mutations:** Where do create/update/delete operations go? (e.g., `src/lib/actions/`, `app/api/`, server actions)
- **Queries:** Where do read operations go? (e.g., direct in components, `src/lib/queries/`, separate query functions)
- **API Routes:** Structure for REST/GraphQL endpoints? (e.g., `app/api/[route]/route.ts`, `src/routes/`)
- **Database Access:** Direct ORM calls vs abstraction layer? (e.g., Drizzle queries in `src/db/queries/`, or direct in route handlers)

**Schema / Model Updates:**
```sql
-- Example
ALTER TABLE users ADD COLUMN referral_code TEXT;
```

**Server Actions / Backend Operations:**
- Create operations: [list create/mutation actions needed]
- Update operations: [list update operations needed]
- Delete operations: [list delete operations needed]
- Each should follow project's data access pattern rules above

**Database Queries:**
- Fetch operations: [list read/query operations needed]
- Query location: [direct queries vs separate query functions per pattern rules]
- Filtering/sorting: [any complex query requirements]

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

## 13. Second-Order Impact Analysis

**Code Sections at Risk:**
- Which existing code might break or need updates?
- Shared utilities, hooks, or components that depend on this change?
- Other features that rely on affected APIs or data structures?

**Performance Concerns:**
- Will this add latency or increase load? (database queries, API calls, rendering)
- Are new indexes or caching strategies needed?
- Any N+1 query risks or inefficient data fetching?

**User Workflow Impacts:**
- How will user flows be affected?
- Are there breaking UX changes that need communication?
- Do users need to be notified or guided through changes?

**Data & Migration Impacts:**
- Will existing data need transformation?
- Are there backward compatibility requirements?
- What happens to users with old data formats?

**Integration Points:**
- Third-party services or webhooks affected?
- Mobile apps or external clients that consume this API?
- Analytics or monitoring that needs updating?

---

## 14. Rollback Plan

How to safely revert if something breaks:
- Code rollback steps
- Database migration rollback
- Data recovery procedure
- Feature flag disable method

---

## 15. File Map & Artifacts

Exact files to create or update, plus required artifacts:

- `/db/migrations/2025-11-01_add_referral_code.sql` (new) → must exist
- `/src/api/auth.ts` (update) → add `exchangeToken()`; include JSDoc
- `/src/components/SignupForm.tsx` (new)
- **Artifact:** screenshot of successful OAuth redirect saved at `refs/proof/oauth-success.png`

---

## 16. Testing Checklist

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

## 17. AI Agent Actions & Guardrails

### Implementation Workflow

🎯 **MANDATORY PROCESS:**

1. **Planning Phase:**
   - Review all sections before starting implementation
   - Understand Context Capsule (Section 2) and Current State (Section 4)
   - Verify all dependencies are met (Section 12)
   - Check Second-Order Impact Analysis (Section 13) for risks

2. **Implementation Phase:**
   - Follow data access pattern rules (Section 9) for code placement
   - Update progress in real-time (see Real-Time Progress Tracking below)
   - Follow plan phases (Section 11) sequentially
   - Update File Map & Artifacts (Section 15) as files are created/modified

3. **Validation Phase:**
   - Ensure all Success Criteria (Section 5) are met
   - Complete Testing Checklist (Section 16)
   - Verify no breaking changes per constraints (Section 6)
   - Document any deviations from plan

**Actions:**
- **Update progress in real-time:** Mark checkboxes in Success Criteria (Section 5) as work completes. Update front matter `status` field incrementally: `draft` → `in_progress` → `review` → `done`.
- **Track file changes:** Update Section 15 (File Map & Artifacts) as files are created or modified. Note completion status for each file.
- **Document as you go:** Update relevant sections (API Contracts, Frontend Impact, etc.) as implementation decisions are made, not just at the end.
- Resolve date placeholders: created_at = today (America/Chicago, YYYY-MM-DD); updated_at = now (ISO8601 with offset). Do not leave placeholders.
- Generate minimal diff
- Add 2 unit tests
- Update docs section

**Real-Time Progress Tracking:**
- **Status Updates:** Update YAML front matter `status` field as work progresses (draft → in_progress → review → done)
- **Checklist Progress:** Mark Success Criteria checkboxes (Section 5) when each criterion is met
- **File Completion:** Update Section 15 (File Map & Artifacts) with completion status: `☐` → `☑` or add `(done)` markers
- **Progress Communication:** If blocked or making significant changes, update relevant sections immediately to maintain transparency

### Communication Preferences

**How the AI agent should communicate:**
- **Progress Updates:** Update this document's status and checkboxes in real-time as work completes (see Real-Time Progress Tracking above)
- **Blockers:** If blocked, explicitly update the relevant section (e.g., Dependencies, Impact Analysis) with blocker details
- **Decisions:** Document implementation decisions immediately in relevant sections (API Contracts, Frontend Impact, etc.) rather than waiting until completion
- **Questions:** If something is unclear, flag it explicitly in the relevant section rather than making assumptions
- **Changes from Plan:** If deviating from the original plan (Section 11), update the plan and document rationale in Wrap-Up section
- **Completion:** When finished, mark all checkboxes, update status to `done`, and complete Wrap-Up / Reflection (Section 18)

### Code Quality Standards

**Coding standards the AI agent must follow:**
- **Code Style:** Follow existing project lint rules and formatting conventions
- **Error Handling:** Include proper error handling and validation for all inputs
- **Type Safety:** Use TypeScript types strictly; avoid `any` types
- **Documentation:** Add JSDoc comments for all public functions and complex logic
- **Testing:** Write unit tests for critical paths (minimum 2 tests per task)
- **Performance:** Consider performance implications; avoid N+1 queries, unnecessary re-renders
- **Security:** Follow security best practices; validate inputs, sanitize outputs
- **Accessibility:** Ensure accessibility standards are met (a11y goals from Section 8)
- **Code Organization:** Follow data access pattern rules (Section 9) for proper code placement
- **Commit Scope:** Keep commits focused and scoped to the task

**Guardrails:**
- Resolve all {{TOKEN}} placeholders at instantiation time; leave none unresolved.
- Set `created_at` = {{AUTO:DATE:America/Chicago}}, `updated_at` = {{AUTO:DATETIME_ISO:America/Chicago}}.
- Replace only in YAML/TODO fields; never inject {{TOKEN}} into runtime code.
- Do not change unrelated files
- Keep commits scoped
- Follow existing lint rules
- No literal date placeholders remain; created_at and updated_at are populated as above.
- Follow data access pattern rules (Section 9) - place code in correct locations per project structure

---

## 18. Wrap-Up / Reflection (Optional)

**What changed:** Quick summary of actual implementation vs. plan

**Lessons:** Notes for future tasks (what worked, what didn't)

**Follow-ups:** Related tasks or improvements to consider

---

