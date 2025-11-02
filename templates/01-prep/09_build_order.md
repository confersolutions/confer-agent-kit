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

# Phased Build Plan

**Purpose:** Define incremental milestones, dependency graph, staffing/agent allocation, risk-based ordering, definition of done, and release plan for the project build.

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

- Master plan: `refs/master-plan.md`
- Roadmap: `refs/roadmap.md`
- Risk assessment: `refs/risks.md`

---

## 3. Incremental Milestones

| Phase | Focus | Duration | Key Deliverables | Prerequisites |
|-------|-------|----------|-----------------|---------------|
| Phase 0 | Setup | 1 week | Project scaffold, dev environment, CI/CD | Initial research |
| Phase 1 | Foundation | 3 weeks | Auth, database, basic UI, core API | Phase 0 complete |
| Phase 2 | Core Features | 4 weeks | MVP features, integrations, polish | Phase 1 complete |
| Phase 3 | Launch Prep | 2 weeks | Testing, docs, deployment, monitoring | Phase 2 complete |

---

## 4. Dependency Graph

**Phase 0 Dependencies:**
- None (initial setup)

**Phase 1 Dependencies:**
- Phase 0 complete
- Design system defined (from prep phase)
- Database schema finalized

**Phase 2 Dependencies:**
- Phase 1 complete
- API contracts defined
- UI wireframes approved

**Phase 3 Dependencies:**
- Phase 2 complete
- All features implemented
- QA sign-off

**Critical Path:**
Phase 0 → Phase 1 → Phase 2 → Phase 3 (linear dependency chain)

---

## 5. Staffing/Agent Plan

**Team Allocation:**

| Phase | Role | Allocation | Responsibilities |
|-------|------|------------|------------------|
| Phase 0 | DevOps/Infra | 100% | Setup, CI/CD, infrastructure |
| Phase 1 | Backend | 70% | API, database, auth integration |
| Phase 1 | Frontend | 70% | UI components, routing, auth UI |
| Phase 2 | Backend | 80% | Core features, integrations |
| Phase 2 | Frontend | 80% | Feature UI, state management |
| Phase 3 | QA | 100% | Testing, bug fixes |
| Phase 3 | DevOps | 50% | Deployment, monitoring |

**Agent Usage:**
- Code generation: 40% of development time
- Documentation: 20% of development time
- Testing: 30% of development time
- Code review: 10% of development time

---

## 6. Risk-Based Ordering

**High-Risk Items First:**
1. Authentication integration (critical, unknown complexity)
2. Database schema and migrations (foundation, hard to change later)
3. External API integrations (third-party dependencies)
4. Complex business logic (core value, error-prone)

**Low-Risk Items Later:**
- UI polish and styling
- Documentation
- Performance optimization
- Nice-to-have features

**Risk Mitigation:**
- Spike tasks for high-risk items (1–2 day exploration)
- Prototype risky integrations early
- Build fallback plans for external dependencies

---

## 7. Definition of Ready per Milestone

**Phase 0 (Setup) Definition of Ready:**
- ☐ Project requirements defined
- ☐ Team/staffing allocated
- ☐ Development environment access granted
- ☐ Repository and CI/CD tools ready

**Phase 1 (Foundation) Definition of Ready:**
- ☐ Design system finalized (from prep phase)
- ☐ Database schema designed
- ☐ API contracts defined
- ☐ Auth provider selected and configured

**Phase 2 (Core Features) Definition of Ready:**
- ☐ Wireframes approved
- ☐ API endpoints specified
- ☐ External service credentials obtained
- ☐ Integration requirements documented

**Phase 3 (Launch Prep) Definition of Ready:**
- ☐ All features implemented and tested
- ☐ Performance benchmarks defined
- ☐ Security audit scheduled
- ☐ Launch checklist prepared

---

## 7a. Definition of Done per Milestone

**Phase 0 (Setup) Definition of Done:**
- ☐ Project scaffold created (Next.js + FastAPI)
- ☐ Development environment working locally
- ☐ CI/CD pipeline functional (tests, lint, deploy)
- ☐ Basic documentation structure in place

**Phase 1 (Foundation) Definition of Done:**
- ☐ Authentication working (signup, login, logout)
- ☐ Database schema implemented with migrations
- ☐ Basic UI components rendered (design system applied)
- ☐ Core API endpoints functional (CRUD operations)
- ☐ Unit tests for critical paths (≥ 60% coverage)

**Phase 2 (Core Features) Definition of Done:**
- ☐ All MVP features implemented
- ☐ External integrations working
- ☐ End-to-end user flows functional
- ☐ Integration tests passing
- ☐ Code review completed

**Phase 3 (Launch Prep) Definition of Done:**
- ☐ All tests passing (unit, integration, E2E)
- ☐ Documentation complete (README, API docs)
- ☐ Production deployment successful
- ☐ Monitoring and alerting configured
- ☐ Security audit completed
- ☐ Stakeholder sign-off received

---

## 8. Release Plan

**Release Cut-Lines:**

| Release | Cut Date | Includes | Target Users |
|---------|----------|----------|--------------|
| v0.1.0 (Alpha) | [Date] | Phase 1 deliverables | Internal testing |
| v0.5.0 (Beta) | [Date] | Phase 2 deliverables | Beta users |
| v1.0.0 (GA) | [Date] | Phase 3 deliverables | Public launch |

**Release Process:**
1. Feature freeze (1 week before cut)
2. QA testing cycle
3. Bug fix window
4. Final testing
5. Deployment to production
6. Monitoring and rollback plan ready

**Rollback Strategy:**
- Database migrations reversible
- Feature flags for risky features
- Automated rollback script tested
- Rollback decision criteria defined

---

## 8a. Risk Burndown

| Week | Risk Score | High Risks | Medium Risks | Low Risks | Notes |
|------|------------|------------|--------------|----------|-------|
| Week 1 | [1-10] | [count] | [count] | [count] | [notes] |
| Week 2 | [1-10] | [count] | [count] | [count] | [notes] |
| Week 3 | [1-10] | [count] | [count] | [count] | [notes] |

**Risk Scoring:** 1 (low) to 10 (critical). Track weekly to monitor risk reduction.

---

## 8b. Telemetry to Emit

**Product Analytics Events:**
- Phase completion events: `phase_complete` (properties: `phase`, `duration`, `milestone`)
- Build milestone events: `milestone_reached` (properties: `milestone`, `timestamp`)
- Deployment events: `deploy_success` / `deploy_failure` (properties: `environment`, `version`)

**Telemetry to Emit:** Standard build and deployment tracking events for monitoring project progress and identifying bottlenecks across all phases.

---

## 9. File Map & Artifacts

- `/docs/build-plan.md` (new) → must exist
- `/docs/milestones.md` (new) → milestone tracking
- `/docs/release-plan.md` (new) → release schedule

**Artifacts required:**
- Phase table with prerequisites column → saved at `refs/phase-table.md`
- Cut-lines for release → saved at `refs/release-cutlines.md`

---

## 10. AI Agent Actions & Guardrails

**Actions:** generate phased build plan with milestones; create dependency graph; draft staffing allocation; define risk-based ordering and definition of done; plan release cut-lines.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

