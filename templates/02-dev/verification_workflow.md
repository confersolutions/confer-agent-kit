---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"        # draft | in_progress | review | done
priority: "high"       # critical | high | normal | low
type: "verification"   # feature | enhancement | bugfix | research | refactor | verification
labels: ["ai","verification"]
version: "1.0.0"
project_profile:       # optional - standardize project constants
  env: "{{ENV}}"           # dev | staging | prod
  http_port: "{{HTTP_PORT}}"     # do NOT set numeric default
  frameworks: ["{{FRAMEWORKS}}"]
  db: "{{DB}}"
  auth: "{{AUTH_SYSTEM}}"
  infra: "{{INFRA}}"
---

# Verification Workflow Template

**Purpose:** Post-merge verification steps and rollback checklist. Use this after merging a PR or deploying changes to verify everything works and document rollback procedures. Produces concrete artifacts under `refs/`.

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
- **Deployment URL:** [production/staging URL]
- **Secrets location (local only):** `[project-name]/secrets/.env`
- **Project profile:** `./confer-agent.profile.yml` (and optional `./confer-agent.profile.local.yml`)
- **Non-negotiables:** Do NOT change ports without updating the project profile and ingress config.

---

## 2. References & Inputs

External snippets/links cached in `refs/` (gitignored):

- Project profile: `./confer-agent.profile.yml`
- Merged PR: `refs/pr-XXX-merge-info.md`
- Deployment config: `refs/deployment-config.yml`
- Health check endpoint: `refs/health-response.json`

**Standards reference:**
- Backend verification: `standards/backend.md`
- Frontend verification: `standards/frontend.md`
- Global conventions: `standards/global.md`

---

## 3. Pre-Verification Checklist

**Before Running Verification:**
- ☐ PR merged to target branch (main/staging)
- ☐ Deployment triggered (CI/CD pipeline)
- ☐ Deployment status: [success/failed] (from CI/CD logs)
- ☐ Database migrations: [applied/not needed]
- ☐ Environment variables: [updated/not needed]

**Deployment Info:**
- Commit SHA: [commit hash]
- Deployment URL: [production/staging URL]
- Deployment time: [timestamp]
- Rollback commit: [previous commit hash] (for rollback reference)

**Artifacts:**
- Deployment logs: `refs/deployment-logs-YYYYMMDD.txt`
- CI/CD status: `refs/ci-status-YYYYMMDD.json`

---

## 4. Verification Steps

### Health Checks

**API Health:**
- ☐ Health endpoint: `GET [deployment-url]/api/health` (fill in deployment URL)
  - Expected: 200 OK with status: "ok"
  - Actual: [status code, response body]
  - Artifact: `refs/proof/health-check-YYYYMMDD.json`

**Database Connectivity:**
- ☐ Database connection: [test query]
  - Expected: [query result]
  - Actual: [query result]
  - Artifact: `refs/proof/db-connection-YYYYMMDD.txt`

**External Services:**
- ☐ Auth service: [Clerk/Auth0/etc. status]
- ☐ Email service: [SendGrid/Postmark/etc. status]
- ☐ CDN/Caching: [Cloudflare/Vercel/etc. status]

### Functional Verification

**Critical User Flows:**
- ☐ [Flow name]: [steps and expected result]
  - URL: [test URL]
  - Steps: 1) ... 2) ... 3) ...
  - Expected: [what should happen]
  - Actual: [what happened]
  - Screenshot: `refs/proof/flow-YYYYMMDD-*.png`

**API Endpoints:**
- ☐ [Endpoint name]: [method, path]
  - Request: [request body/params]
  - Expected: [status, response body]
  - Actual: [status, response body]
  - Artifact: `refs/proof/api-YYYYMMDD-*.json`

**UI Components:**
- ☐ [Component/page name]: [what to verify]
  - URL: [test URL] (fill in deployment URL)
  - Expected: [what should render]
  - Actual: [what rendered]
  - Screenshot: `refs/proof/ui-YYYYMMDD-*.png`

### Performance Verification

**Response Times:**
- ☐ API endpoint: `GET [deployment-url]/api/users` (fill in deployment URL)
  - Expected: < 500ms
  - Actual: [response time]
  - Artifact: `refs/proof/performance-YYYYMMDD.json`

**Page Load Times:**
- ☐ Homepage: `[deployment-url]/` (fill in deployment URL)
  - Expected: < 2s
  - Actual: [load time]
  - Artifact: `refs/proof/performance-YYYYMMDD.json`

**Database Query Performance:**
- ☐ Slow queries: [check for queries > 1s]
  - Results: [list any slow queries]
  - Artifact: `refs/proof/slow-queries-YYYYMMDD.json`

---

## 5. Rollback Plan

**When to Rollback:**
- ☐ Health checks fail (API returns 500, DB connection fails)
- ☐ Critical user flows broken (unable to login, checkout fails)
- ☐ Performance degraded (response times > 5s, page load > 10s)
- ☐ Data integrity issues (missing data, corrupted records)

**Rollback Steps:**
1. **Identify rollback commit:** [previous stable commit hash]
2. **Revert deployment:**
   - [Platform-specific rollback command]
   - Or: `git revert [commit hash]` + redeploy
3. **Verify rollback:**
   - ☐ Health checks pass
   - ☐ Critical flows work
   - ☐ Database state consistent
4. **Document rollback:**
   - Artifact: `refs/rollback-report-YYYYMMDD.md`
   - Include: reason, commit reverted to, verification results

**Rollback Artifacts:**
- Rollback report: `refs/rollback-report-YYYYMMDD.md`
- Rollback logs: `refs/rollback-logs-YYYYMMDD.txt`
- Post-rollback verification: `refs/proof/rollback-verification-YYYYMMDD.json`

---

## 6. Post-Verification Summary

**Verification Status:**
- ☐ All health checks passed
- ☐ All critical flows working
- ☐ Performance within acceptable range
- ☐ No data integrity issues
- ☐ Rollback plan ready (if needed)

**Issues Found (if any):**
- [Issue description]: [severity, impact, fix plan]

**Artifacts Produced:**
- `refs/proof/health-check-YYYYMMDD.json`
- `refs/proof/flow-YYYYMMDD-*.png` (screenshots)
- `refs/proof/api-YYYYMMDD-*.json` (API responses)
- `refs/proof/performance-YYYYMMDD.json` (performance metrics)
- `refs/rollback-report-YYYYMMDD.md` (if rollback occurred)

**Next Steps:**
- [Follow-up tasks if needed]
- [Monitoring recommendations]

---

## 7. AI Agent Actions & Guardrails

**Actions:**
- Review deployment status and commit info
- Run health checks and capture results
- Verify critical user flows
- Test API endpoints
- Check performance metrics
- Document any issues found
- Generate verification artifacts under `refs/`
- Update verification checklist

**Guardrails:**
- Resolve all {{TOKEN}} placeholders at instantiation time; leave none unresolved.
- Set `created_at` = {{AUTO:DATE:America/Chicago}}, `updated_at` = {{AUTO:DATETIME_ISO:America/Chicago}}.
- Replace only in YAML/TODO fields; never inject {{TOKEN}} into runtime code.
- Never hard-code ports or environment values; use `{{HTTP_PORT}}`, `{{ENV}}` from profile.
- Deployment URLs are user-provided (not in profile); fill in `[production/staging URL]` sections.
- Store verification artifacts under `refs/proof/` or `refs/`.
- Follow verification standards in `standards/backend.md`, `standards/frontend.md`.
- Use project profile (`./confer-agent.profile.yml`) for deployment environment values.
- Document rollback procedure clearly; never skip rollback verification.

---

## Links

**Related:** [testing_checklist.md](testing_checklist.md), [task_template_full.md](task_template_full.md), [bugfix.md](bugfix.md)

**Standards:** [standards/backend.md](../../standards/backend.md), [standards/frontend.md](../../standards/frontend.md), [standards/global.md](../../standards/global.md)

