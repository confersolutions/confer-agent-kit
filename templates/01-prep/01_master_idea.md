---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"        # draft | in_progress | review | done
priority: "high"       # critical | high | normal | low
type: "planning"       # fixed for prep templates
labels: ["ai","planning"]
version: "1.0.0"
project_profile:       # optional - standardize project constants
  env: "{{ENV}}"           # dev | staging | prod
  http_port: "{{HTTP_PORT}}"     # do NOT set numeric default
  frameworks: ["{{FRAMEWORKS}}"]
  db: "{{DB}}"
  auth: "{{AUTH_SYSTEM}}"
  infra: "{{INFRA}}"
---

# Project Master Plan

**Purpose:** Define the core vision, problem statement, success metrics, scope boundaries, risks, roadmap, and governance for the project.

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

External snippets/links cached in `output/` (gitignored):

- Project profile: `./confer-agent.profile.yml`
- Market research: `output/market-research.md`
- Competitor analysis: `output/competitors.md`
- User interviews: `output/user-insights.md`

---

## 3. Vision & Problem

**Vision Statement:** One sentence describing the desired future state.

**Problem Statement:** What specific problem are we solving? Who experiences it?

**Opportunity Size:** Market size, user count, or business value estimate.

---

## 4. Users & Jobs-to-Be-Done

**Primary Users:**
- User persona #1: [role, goals, pain points]
- User persona #2: [role, goals, pain points]

**Jobs-to-Be-Done:**
- "When [situation], I want to [motivation], so I can [expected outcome]"
- ...

---

## 5. Success Metrics (KPIs)

| Metric | Baseline | Target | Timeframe | Measurement Method |
|--------|----------|--------|-----------|-------------------|
| User adoption | 0 | [target] | [timeframe] | Analytics |
| Engagement rate | 0% | [target]% | [timeframe] | Event tracking |
| Revenue/Value | $0 | $[target] | [timeframe] | Financial data |

---

## 6. Scope (In/Out)

**In Scope:**
- Core feature set #1
- Core feature set #2
- Essential integrations

**Out of Scope (v1):**
- Feature X (defer to v2)
- Integration Y (future consideration)
- Platform Z (not supported initially)

---

## 6a. Non-Goals & Constraints

**Non-Goals:**
- Feature X (explicitly out of scope)
- Platform Y (not supported)
- Integration Z (future consideration)

**Budget Constraints:**
- Monthly budget: $[amount]
- Annual budget: $[amount]
- Resource allocation: [limits]

**Time Constraints:**
- MVP deadline: [date]
- Launch deadline: [date]
- Phase milestones: [dates]

**Regulatory/Compliance Constraints:**
- GDPR compliance required
- SOC2 certification (if applicable)
- Industry-specific regulations: [list]

---

## 7. Risks & Assumptions

**Key Assumptions:**
- Assumption #1: [validity check needed]
- Assumption #2: [validation plan]

**Risks:**
- Risk #1: [mitigation strategy]
- Risk #2: [contingency plan]

---

## 8. High-Level Roadmap

| Phase | Focus | Duration | Key Deliverables | Prerequisites |
|-------|-------|----------|-----------------|---------------|
| Phase 1 | MVP/Foundation | [timeframe] | Core features, auth, basic UI | Initial research |
| Phase 2 | Enhancement | [timeframe] | Advanced features, integrations | Phase 1 complete |
| Phase 3 | Scale | [timeframe] | Performance, polish, launch prep | Phase 2 complete |

---

## 9. Integration Landscape

**External Services:**
- Service #1: [purpose, API requirements]
- Service #2: [authentication needs, rate limits]

**Third-Party Dependencies:**
- Library/framework dependencies
- Compliance requirements (GDPR, SOC2, etc.)

---

## 10. Governance

**Decision Cadence:**
- Weekly review meetings
- Milestone gates before proceeding

**Review Process:**
- Technical review at [stage]
- Product review at [stage]
- Stakeholder sign-off required for [decisions]

**Stakeholder RACI:**

| Stakeholder | Role | Responsibility | Notes |
|-------------|------|----------------|-------|
| Product Owner | Responsible | Feature decisions, priorities | Final approval |
| Tech Lead | Accountable | Technical architecture, quality | Sign-off required |
| Developer | Consulted | Implementation details | Input on feasibility |

---

## 11. Dependencies

**Prerequisites:**
- External service access/approvals
- Team/staffing requirements
- Budget/timeline constraints

---

## 12. File Map & Artifacts

- `/docs/master-plan.md` (new) → must exist
- `/docs/kpi-tracker.md` (new) → KPI tracking template

**Artifacts required:**
- KPI table → saved at `output/kpi-table.md`
- 3-phase roadmap table → saved at `output/roadmap.md`

---

## 13. Decision Log

| Decision | Date | Rationale | Owner |
|----------|------|-----------|-------|
| [Decision] | [YYYY-MM-DD] | [Why this decision] | [Owner] |
| [Decision] | [YYYY-MM-DD] | [Why this decision] | [Owner] |
| [Decision] | [YYYY-MM-DD] | [Why this decision] | [Owner] |

---

## 14. AI Agent Actions & Guardrails

**Actions:** generate project vision statement; create KPI tracking table; draft roadmap phases; compile risk assessment.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

