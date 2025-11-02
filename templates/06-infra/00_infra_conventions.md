---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"            # draft | in_progress | review | done
priority: "high"           # critical | high | normal | low
type: "infra"              # fixed for infra templates
labels: ["ai","infra"]
version: "1.0.0"
project_profile:           # optional - standardize project constants
  env: "{{ENV}}"               # dev | staging | prod
  http_port: "{{HTTP_PORT}}"         # do NOT set numeric default
  frameworks: ["{{FRAMEWORKS}}"]
  db: "{{DB}}"
  auth: "{{AUTH_SYSTEM}}"
  infra: "{{INFRA}}"
---

# Canonical Infrastructure Conventions

**Purpose:** Single source of truth for ports, routing, DNS/TLS, branch-to-environment mapping, secrets handling, and cross-platform migration patterns across all infrastructure services.

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

- Port routing examples: `refs/ports_routing_matrix.csv`
- DNS configuration: `refs/dns_examples.md`
- Migration patterns: `refs/migration_patterns.md`

---

## 3. Ports & Routing Matrix

| Service | Internal Port | External Port | Routing | Traefik Labels | Notes |
|---------|--------------|---------------|---------|----------------|-------|
| Next.js (Vercel) | - | 80/443 | Auto | - | Vercel-managed |
| FastAPI (Coolify) | 8000 | {{HTTP_PORT}} | Traefik | `traefik.http.routers.api.rule` | Backend API port (defined in project profile) |
| n8n (Coolify) | 5678 | - | Traefik | `traefik.http.routers.n8n.rule` | Behind proxy |
| Flowise (Coolify) | 3000 | - | Traefik | `traefik.http.routers.flowise.rule` | Behind proxy |
| Qdrant (Coolify) | 6333 | - | Internal | - | gRPC/HTTP |
| Neo4j (Coolify) | 7474/7687 | - | Internal | - | Bolt/HTTP |
| Postgres (Coolify) | 5432 | - | Internal | - | DB only |

**Port Conventions:**
- **HTTP=80:** Standard web traffic (Vercel auto-handles)
- **Backend API port:** {{HTTP_PORT}} (set in project profile) - Backend API services (Coolify + Traefik)
- **Internal ports:** Only accessible within Coolify network
- **External ports:** Exposed via Traefik with domain routing

**Traefik Label Pattern:**
```yaml
traefik.enable: "true"
traefik.http.routers.[service].rule: "Host(`[service].yourdomain.com`)"
traefik.http.routers.[service].entrypoints: "websecure"
traefik.http.routers.[service].tls.certresolver: "letsencrypt"
```

---

## 4. Branch → Environment Mapping

| Branch Pattern | Environment | Domain Pattern | Deployment Target |
|----------------|-------------|----------------|-------------------|
| `main` | Production | `*.yourdomain.com` | Coolify (prod) / Vercel (prod) |
| `staging` | Staging | `staging.yourdomain.com` | Coolify (staging) |
| `feature/*` | Preview | `pr-[number].yourdomain.com` | Vercel (preview) |
| `develop` | Development | `dev.yourdomain.com` | Coolify (dev) / Replit |

**Environment Variables:**
- Production: `NODE_ENV=production`
- Staging: `NODE_ENV=staging`
- Preview: `NODE_ENV=development`
- Development: `NODE_ENV=development`

---

## 5. DNS & TLS Conventions

**DNS Record Types:**

| Record Type | Use Case | Example |
|-------------|----------|---------|
| A | Point to IP | `yourdomain.com` → `1.2.3.4` |
| CNAME | Point to domain | `www.yourdomain.com` → `yourdomain.com` |
| CNAME (Wildcard) | Preview deployments | `*.yourdomain.com` → Vercel/Coolify |
| CNAME (Subdomain) | Services | `api.yourdomain.com` → Coolify LB |

**TLS Certificate Strategy:**
- **Production:** Let's Encrypt (auto-renew via Coolify Traefik)
- **Staging:** Let's Encrypt (auto-renew via Coolify Traefik)
- **Preview:** Vercel-managed certificates (automatic)
- **Local Dev:** Self-signed or HTTP only

**Certificate Resolver (Coolify Traefik):**
- Resolver: `letsencrypt`
- Email: [your-email]
- Staging: `letsencrypt-staging` (for testing)

---

## 6. Secrets Policy

**Local Development:**
- Location: `[project-name]/secrets/.env`
- Status: **Gitignored** (never commit)
- Format: Standard `.env` file
- Access: Local only, never pushed to repo

**Platform Secrets (Coolify/Vercel):**
- Location: Platform environment variables
- Management: Platform UI (Coolify) or CLI (Vercel)
- Naming: UPPER_SNAKE_CASE (e.g., `API_KEY`, `DATABASE_URL`)
- Rotation: Manual update via platform UI

**Secrets Hierarchy:**
1. Platform env vars (production)
2. Local `.env` file (development)
3. Never hardcode in code/configs

**Required Secrets (Examples):**
- `DATABASE_URL` (Postgres connection string)
- `API_KEY` (Third-party API keys)
- `JWT_SECRET` (Auth token signing)
- `OAUTH_CLIENT_ID` / `OAUTH_CLIENT_SECRET` (OAuth providers)

---

## 7. Cross-Platform Migration Notes

**Coolify ⇄ Vercel Pattern:**

1. **Frontend Migration (Vercel → Coolify):**
   - Export Vercel build config → Coolify build settings
   - Map Vercel env vars → Coolify env vars
   - Update DNS: Remove Vercel CNAME → Add Coolify CNAME
   - Deploy on Coolify → Verify Traefik routing

2. **Backend Migration (Coolify → Vercel):**
   - Not recommended (use Coolify for backend APIs)
   - If needed: Convert to Vercel Serverless Functions
   - Update port references ({{HTTP_PORT}} → default Vercel port, defined in project profile)

3. **Replit ⇄ Coolify Pattern:**

   **Replit → Coolify:**
   - Export Replit env vars → Coolify env vars
   - Convert Replit run commands → Coolify Dockerfile/docker-compose
   - Update service connections (use Coolify internal networking)
   - Deploy on Coolify → Verify health checks

   **Coolify → Replit:**
   - Import Coolify env vars → Replit secrets
   - Use Replit tunnel to connect to Coolify services
   - Set up port forwarding for internal services

**Migration Checklist:**
- ☐ Export environment variables from source platform
- ☐ Import environment variables to target platform
- ☐ Update DNS records (if applicable)
- ☐ Verify service health checks
- ☐ Test integrations and connections
- ☐ Update documentation with new paths/URLs

---

## 8. Service Communication Patterns

**Internal Service Communication (Coolify):**
- Use service names as hostnames (e.g., `postgres://postgres:5432`)
- No external ports needed (internal Docker network)
- Example: `http://flowise:3000` from n8n container

**External Service Communication (Cross-Platform):**
- Use full domain URLs (e.g., `https://api.yourdomain.com`)
- Handle authentication via env vars
- Use TLS/HTTPS for all external calls

**Port Exposure Rules:**
- **Public:** Only via Traefik with TLS
- **Internal:** Docker network only
- **Never:** Expose database ports externally

---

## 9. File Map & Artifacts

- `/docs/infra-conventions.md` (new) → must exist
- `/docs/migration-guides.md` (new) → migration documentation

**Artifacts required:**
- Ports & Routing Matrix CSV → saved at `refs/ports_routing_matrix.csv`
- DNS examples → saved at `refs/dns_examples.md`

---

## 10. AI Agent Actions & Guardrails

**Actions:** generate ports routing matrix; define DNS/TLS conventions; create branch-to-env mapping; draft migration patterns and checklists.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

