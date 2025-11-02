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

# Architecture Overview

**Purpose:** Define system architecture with context diagrams, service contracts, data flow, caching strategy, observability, failure modes, scaling plan, security model, and cost considerations.

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

- Architecture diagrams: `output/architecture-diagrams.md`
- Service contracts: `output/service-contracts.md`
- Infrastructure docs: `output/infrastructure.md`

---

## 3. Context Diagram Description

**System Boundaries:**
- Frontend: Next.js app (Vercel/Cloudflare Pages)
- Backend API: FastAPI service (VPS/Coolify)
- Database: Postgres (managed service or self-hosted)
- Auth: Clerk (external service)
- Storage: [S3/Coolify volumes/etc.]

**External Integrations:**
- Third-party APIs: [list]
- Webhooks: [incoming/outgoing]
- Email service: [SendGrid/Resend/etc.]

---

## 4. Key Services & Contracts

| Service | Responsibility | Interface | Protocol |
|---------|---------------|-----------|----------|
| Frontend | UI rendering, client-side routing | React/Next.js | HTTP/WebSocket |
| API | Business logic, data processing | REST/GraphQL | HTTP |
| Auth | Authentication, authorization | Clerk API | OAuth 2.0 |
| Database | Data persistence | SQL | Postgres protocol |
| [Service] | [Responsibility] | [Interface] | [Protocol] |

---

## 5. Data Flow

**Request Flow:**
1. User → Frontend (HTTP request)
2. Frontend → API (REST/GraphQL call)
3. API → Auth (token validation)
4. API → Database (query/mutation)
5. Database → API (result)
6. API → Frontend (response)
7. Frontend → User (rendered UI)

**Background Jobs:**
- Queue system: [Redis/BullMQ/etc.]
- Job types: [email sending, data processing, etc.]
- Processing: [async workers, scheduled tasks]

---

## 6. Caching Strategy

**Cache Layers:**

| Layer | Technology | TTL | Use Case |
|-------|------------|-----|----------|
| CDN | Cloudflare | 1h | Static assets |
| Edge | Vercel Edge | 5m | API responses |
| Application | Redis | 15m | User sessions, query results |
| Browser | LocalStorage | Session | User preferences |

**Cache Invalidation:**
- On data updates (immediate)
- Time-based expiration (TTL)
- Manual purge when needed

---

## 7. Observability (Logs/Metrics/Traces)

**Logging:**
- Application logs: [JSON structured logs to stdout]
- Log aggregation: [Cloudflare Logpush / Coolify logs]
- Log levels: ERROR, WARN, INFO, DEBUG

**Metrics:**
- Application metrics: [Prometheus/Grafana]
- Infrastructure metrics: [Coolify monitoring]
- Business metrics: [Custom dashboard]

**Tracing:**
- Distributed tracing: [OpenTelemetry / optional]
- Request IDs: Propagate through all services
- Performance monitoring: [Sentry/DataDog]

---

## 8. Failure Modes & Timeouts

**Failure Scenarios:**

| Failure | Impact | Mitigation | Timeout |
|---------|--------|------------|---------|
| Database down | High | Fallback, retry logic | 30s |
| Auth service down | Critical | Cached tokens, graceful degradation | 10s |
| API timeout | Medium | Client retry, circuit breaker | 30s |
| CDN failure | Low | Direct origin fallback | 5s |

**Circuit Breaker:**
- Open after 5 consecutive failures
- Half-open after 30s
- Close after successful request

---

## 9. Scaling Plan

**Horizontal Scaling:**
- Frontend: Auto-scale on Vercel/Cloudflare (unlimited)
- API: Scale based on CPU/memory usage (2–10 instances)
- Database: Read replicas for read-heavy workloads

**Vertical Scaling:**
- API instances: Start with 2 CPU cores, 4GB RAM
- Database: Start with 4 CPU cores, 16GB RAM

**Auto-scaling Triggers:**
- CPU > 70% for 5 minutes
- Memory > 80% for 5 minutes
- Request rate > [threshold] for 5 minutes

---

## 10. Security Model

**Authentication:**
- Provider: Clerk (OAuth 2.0)
- Session management: JWT tokens
- Token refresh: Automatic via Clerk

**Authorization:**
- Role-based access control (RBAC)
- User → Admin roles
- Resource-level permissions

**Data Protection:**
- Encryption at rest: Database encryption
- Encryption in transit: TLS 1.3
- PII handling: Encrypt sensitive fields
- API security: Rate limiting, CORS, CSRF protection

---

## 11. Cost Notes

**Infrastructure Costs (Monthly Estimate):**

| Service | Tier | Cost |
|---------|------|------|
| Frontend (Vercel) | Pro | $20 |
| API (VPS) | 4 core, 8GB | $40 |
| Database | Managed Postgres | $25 |
| Auth (Clerk) | Pro | $25 |
| CDN/Storage | [Service] | $10 |
| **Total** | | **~$120** |

**Optimization:**
- Use free tiers where possible (dev/staging)
- Monitor usage and adjust tiers
- Cache aggressively to reduce API calls

---

## 11a. Threat Modeling Checklist

**Security Threats:**

| Threat | Mitigation | Status |
|--------|------------|--------|
| Authorization bypass | RBAC, resource-level checks | ☐ Covered |
| SQL injection | Parameterized queries, ORM | ☐ Covered |
| Secrets exposure | Env vars, secrets manager | ☐ Covered |
| Rate limiting | API throttling, DDoS protection | ☐ Covered |
| SSRF (Server-Side Request Forgery) | URL validation, whitelist | ☐ Covered |

---

## 11b. SLO Error Budgets

**Service Level Objectives (SLOs):**

| Service | SLO | Error Budget | Notes |
|--------|-----|--------------|-------|
| API | 99.9% uptime | 0.1% downtime/month | ~43 min/month |
| Frontend | 99.5% uptime | 0.5% downtime/month | ~3.6 hours/month |
| Database | 99.95% uptime | 0.05% downtime/month | ~21 min/month |

**Error Budget Policy:** Once error budget consumed, freeze new features until stability restored.

---

## 12. File Map & Artifacts

- `/docs/architecture.md` (new) → must exist
- `/docs/service-contracts.md` (new) → API contracts
- `/diagrams/architecture.mmd` (new) → Mermaid diagram source

**Artifacts required:**
- Mermaid diagram block (C4-ish) → saved at `output/architecture-diagram.mmd`
- SLOs table → saved at `output/slos-table.md`

---

## 13. AI Agent Actions & Guardrails

**Actions:** generate context diagram description; define service contracts; create data flow diagrams; draft caching and scaling plans; document SLOs.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

