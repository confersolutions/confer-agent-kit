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

# Coolify Platform Runbook

**Purpose:** Operational guide for deploying and managing services on Coolify, including app types, Traefik routing, volumes, health checks, backups, env vars, logs, and rollbacks.

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

**Reference:** See [00_infra_conventions.md](00_infra_conventions.md) for ports, DNS, and routing conventions.

---

## 2. References & Inputs

External snippets/links cached in `output/` (gitignored):

- Project profile: `./confer-agent.profile.yml`

- Traefik examples: `output/coolify_traefik_examples.md`
- Backup checklist: `output/coolify_backup_checklist.md`
- Platform docs: `output/coolify_docs.md`

---

## 3. App/Service Types

**Application Types:**

| Type | Use Case | Build Method | Port Config |
|------|----------|--------------|-------------|
| Docker Compose | Multi-container apps | Build from repo | Define in compose |
| Dockerfile | Single container | Build from Dockerfile | Expose in Dockerfile |
| Static Site | Frontend only | Build step then serve | Nginx/Apache |
| Database | Data store | Pre-built image | Default DB ports |
| One-Click | Templates | Pre-configured | Template defaults |

**Service Selection:**
- **Backend APIs:** Dockerfile (FastAPI, Node.js, etc.)
- **Full-stack apps:** Docker Compose (frontend + backend + DB)
- **Databases:** One-Click templates (Postgres, Neo4j, etc.)
- **Automation:** Docker Compose (n8n, Flowise, etc.)

---

## 4. Traefik Routing & Ports

**Traefik Configuration (via Labels):**

| Label | Value | Purpose |
|-------|-------|---------|
| `traefik.enable` | `"true"` | Enable Traefik routing |
| `traefik.http.routers.[name].rule` | `Host([domain])` | Domain routing |
| `traefik.http.routers.[name].entrypoints` | `websecure` | HTTPS only |
| `traefik.http.routers.[name].tls.certresolver` | `letsencrypt` | Auto TLS |
| `traefik.http.services.[name].loadbalancer.server.port` | `[port]` | Internal port |

**Port/Ingress Matrix:**

| Service | Internal Port | Traefik Domain | External Access |
|--------|--------------|----------------|------------------|
| n8n | 5678 | `n8n.yourdomain.com` | Via Traefik |
| Flowise | 3000 | `flowise.yourdomain.com` | Via Traefik |
| FastAPI | 8000 | `api.yourdomain.com` | Via Traefik (port {{HTTP_PORT}}, defined in project profile) |
| Qdrant | 6333 | - | Internal only |
| Neo4j | 7474/7687 | `neo4j.yourdomain.com` | Via Traefik |
| Postgres | 5432 | - | Internal only |

**Traefik Example (docker-compose.yml):**
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.api.rule=Host(`api.yourdomain.com`)"
  - "traefik.http.routers.api.entrypoints=websecure"
  - "traefik.http.routers.api.tls.certresolver=letsencrypt"
  - "traefik.http.services.api.loadbalancer.server.port=8000"
```

---

## 5. Volumes & Persistent Storage

**Volume Types:**

| Volume Type | Use Case | Path | Backup Strategy |
|-------------|----------|------|----------------|
| Database data | Postgres, Neo4j | `/var/lib/postgresql/data` | Daily snapshots |
| Application data | n8n workflows, Flowise flows | `/app/data` | Export/import |
| Uploads/files | User uploads | `/app/uploads` | External storage (S3) |
| Logs | Application logs | `/app/logs` | Rotation + archival |

**Volume Configuration:**
- **Local:** `coolify/postgres-data` (managed by Coolify)
- **Named:** `postgres-data:/var/lib/postgresql/data`
- **Backup:** Use Coolify backup feature or manual `docker exec` commands

**Volume Backup Checklist:**
- ☐ Identify critical volumes (databases, application data)
- ☐ Set up automated backups (daily/weekly)
- ☐ Test restore process
- ☐ Store backups off-server (S3, external drive)

---

## 6. Health Checks

**Health Check Configuration:**

| Check Type | Endpoint | Interval | Timeout | Success Criteria |
|-----------|----------|----------|---------|------------------|
| HTTP | `/health` | 30s | 10s | 200 OK |
| TCP | `:8000` | 30s | 5s | Port open |
| Command | `pg_isready` | 60s | 10s | Exit code 0 |

**Health Check Examples:**

**FastAPI:**
```yaml
healthcheck:
  path: /health
  interval: 30
  timeout: 10
  retries: 3
```

**Postgres:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 60
  timeout: 10
  retries: 3
```

---

## 7. Environment Variable Management

**Env Var Sources:**

| Source | Priority | Use Case |
|--------|----------|----------|
| Coolify UI | Highest | Production secrets |
| `.env` file (repo) | Medium | Non-sensitive defaults |
| Dockerfile ENV | Lowest | Build-time defaults |

**Env Var Naming:**
- UPPER_SNAKE_CASE (e.g., `DATABASE_URL`, `API_KEY`)
- Prefix by service if needed (e.g., `N8N_API_KEY`, `FLOWISE_OPENAI_KEY`)

**Managing Secrets:**
1. Add via Coolify UI (encrypted storage)
2. Never commit to repo
3. Use `.env.example` for documentation
4. Rotate periodically (update in Coolify UI)

---

## 8. One-Click Deploy Patterns

**Available Templates:**
- Postgres, MySQL, MongoDB, Redis
- n8n, Flowise, Qdrant, Neo4j
- GitLab, Gitea, Jellyfin

**Deployment Steps:**
1. Select template from Coolify UI
2. Configure basic settings (name, domain)
3. Set environment variables
4. Deploy → Auto-configured with Traefik

**Post-Deploy Configuration:**
- ☐ Update default passwords
- ☐ Configure Traefik labels (if not auto-set)
- ☐ Set up health checks
- ☐ Enable backups (if applicable)

---

## 9. Logs & Monitoring

**Log Access:**
- **Coolify UI:** View logs per service (real-time)
- **Docker CLI:** `docker logs [container]` (SSH to server)
- **Log Aggregation:** Set up external service (Grafana Loki, etc.)

**Log Levels:**
- ERROR: Critical issues requiring immediate attention
- WARN: Potential issues, monitor closely
- INFO: Normal operations, useful for debugging
- DEBUG: Verbose logging (disable in production)

**Log Rotation:**
- Configure in Dockerfile or docker-compose.yml
- Use logrotate or Docker logging drivers
- Archive old logs (external storage)

---

## 10. Rollbacks (Revert Image/Tag)

**Rollback Methods:**

| Method | Use Case | Steps |
|--------|----------|-------|
| Revert to previous image | Recent bad deployment | Coolify UI → Deployments → Select previous |
| Pin specific tag | Stable version | Update image tag → Redeploy |
| Git revert + redeploy | Code-level fix | Revert commit → Push → Auto-deploy |

**Rollback Checklist:**
- ☐ Identify target version/image tag
- ☐ Stop current deployment (if needed)
- ☐ Deploy previous version
- ☐ Verify health checks pass
- ☐ Monitor logs for errors
- ☐ Update documentation if needed

**Safe Rollback Pattern:**
1. Keep last 3-5 deployments in history
2. Test rollback process in staging first
3. Have rollback plan documented before deployment

---

## 11. Backup Strategy

**Backup Types:**

| Type | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Database snapshots | Daily | 7 days | Local + S3 |
| Volume backups | Weekly | 30 days | External storage |
| Configuration exports | Monthly | 1 year | Git repo |

**Backup Checklist:**
- ☐ Automate database backups (cron or Coolify scheduler)
- ☐ Test restore process regularly
- ☐ Store backups off-server (S3, external drive)
- ☐ Document restore procedures
- ☐ Monitor backup success/failure

---

## 12. File Map & Artifacts

- `/docs/coolify-runbook.md` (new) → must exist
- `/docker-compose.yml` (update) → Traefik labels

**Artifacts required:**
- Traefik examples → saved at `output/coolify_traefik_examples.md`
- Backup checklist → saved at `output/coolify_backup_checklist.md`

---

## 13. AI Agent Actions & Guardrails

**Actions:** generate Traefik label configurations; create health check examples; draft backup checklist; document rollback procedures.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

