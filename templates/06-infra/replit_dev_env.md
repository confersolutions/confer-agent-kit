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

# Replit Dev Workflow

**Purpose:** Guide for using Replit as a development environment, including when to use Replit vs local dev, secrets handling, connecting to Coolify services via tunnels, preview URLs, and env sync scripts.

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

- Replit dev checklist: `output/replit_dev_checklist.md`
- Replit env sync script: `output/replit_env_sync.sh`
- Replit tunnel guide: `output/replit_tunnels.md`

---

## 3. When to Use Replit vs Local Dev

**Use Replit When:**

| Scenario | Reason | Benefit |
|----------|--------|---------|
| Quick prototyping | Fast setup, no local config | Immediate start |
| Collaborative debugging | Shared environment | Real-time pair programming |
| Cross-platform testing | Works on any OS | No local setup needed |
| Learning new tech | Pre-configured environments | Focus on code |

**Use Local Dev When:**

| Scenario | Reason | Benefit |
|----------|--------|---------|
| Production-like setup | Full control over environment | Matches production |
| Performance testing | Local resources faster | Better performance |
| Offline development | No internet required | Work anywhere |
| Custom tooling | Full shell access | More flexibility |

**Decision Matrix:**
- **Prototyping:** Replit (faster)
- **Production development:** Local dev (matches prod)
- **Collaborative work:** Replit (shared access)
- **Performance-critical:** Local dev (better performance)

---

## 4. Secrets Handling

**Replit Secrets:**

| Location | Access | Use Case |
|----------|--------|----------|
| Replit Secrets UI | Project Settings → Secrets | Production secrets |
| `.env` file | Replit Files | Development defaults |
| Environment variables | Runtime access | Runtime config |

**Secret Management Checklist:**
- ☐ Store sensitive secrets in Replit Secrets UI
- ☐ Use `.env` for non-sensitive defaults
- ☐ Never commit secrets to repo
- ☐ Rotate secrets periodically
- ☐ Sync secrets from Coolify (use sync script)

**Secret Sync Pattern:**
1. Export secrets from Coolify (via UI or API)
2. Import to Replit Secrets (manual or script)
3. Verify secrets loaded at runtime
4. Test connections to external services

---

## 5. Connecting to Coolify Services

**Connection Methods:**

| Method | Use Case | Setup |
|--------|----------|-------|
| Tunnels | Secure access to internal services | Replit Tunnel extension |
| Exposed ports | Public API access | Coolify Traefik routing |
| SSH tunneling | Direct DB access | `ssh -L` command |

**Tunnel Setup (Replit → Coolify):**

1. **Install Replit Tunnel Extension:**
   - Add extension to Replit project
   - Configure tunnel target (Coolify service URL)
   - Set up authentication (if needed)

2. **Tunnel Configuration:**
   ```
   Tunnel Target: https://api.yourdomain.com
   Local Port: 8000
   Protocol: HTTPS
   ```

3. **Access Coolify Service:**
   - Use `localhost:8000` in Replit code
   - Tunnel forwards to Coolify backend
   - HTTPS/TLS handled by tunnel

**Exposed Ports (Public Access):**

| Service | Public URL | Replit Access |
|---------|------------|---------------|
| API | `https://api.yourdomain.com` | Direct HTTPS call |
| n8n | `https://n8n.yourdomain.com` | Direct HTTPS call |
| Flowise | `https://flowise.yourdomain.com` | Direct HTTPS call |

**Internal Services (Tunnels Required):**

| Service | Internal URL | Tunnel Setup |
|---------|--------------|--------------|
| Postgres | `postgres:5432` (internal) | SSH tunnel via Coolify |
| Qdrant | `qdrant:6333` (internal) | SSH tunnel via Coolify |
| Neo4j | `neo4j:7474` (internal) | SSH tunnel via Coolify |

---

## 6. Preview URLs

**Replit Preview Deployment:**

| Deployment Type | URL Pattern | Use Case |
|----------------|-------------|----------|
| Always-on | `https://[project].replit.dev` | Persistent deployment |
| Auto-reload | `https://[project].replit.dev` | Development preview |
| Custom domain | `https://[your-domain]` | Production preview |

**Preview URL Workflow:**

1. **Enable Always-On (if needed):**
   - Project Settings → Run → Always On
   - Preview URL generated automatically

2. **Access Preview:**
   - Use URL from Replit UI
   - Share with team for testing
   - Update documentation with URL

3. **Deploy to Coolify (when ready):**
   - Export code from Replit
   - Deploy to Coolify via git push
   - Update service URLs

**Preview URL Checklist:**
- ☐ Enable Always-On (if needed)
- ☐ Note preview URL
- ☐ Test preview deployment
- ☐ Share URL with team
- ☐ Update docs with URL

---

## 7. Quick Scripts for Syncing Envs

**Env Sync Scripts:**

| Script | Purpose | Path |
|-------|---------|------|
| `replit_env_sync.sh` | Sync env vars from Coolify | `output/replit_env_sync.sh` |
| `replit_env_check.sh` | Verify env vars loaded | Local script |
| `replit_tunnel_setup.sh` | Configure tunnels | Local script |

**Env Sync Pattern:**

1. **Export from Coolify:**
   ```bash
   # Manual export via Coolify UI
   # Or use Coolify API (if available)
   ```

2. **Import to Replit:**
   ```bash
   # Use Replit Secrets UI
   # Or use Replit API (if available)
   ```

3. **Verify Sync:**
   ```bash
   # Check env vars loaded at runtime
   # Test connections to external services
   ```

**Script Location Note:**
- Script paths stored in `output/` (gitignored)
- Scripts not included in repo (security)
- Document script usage in checklist

---

## 8. Replit → Coolify Deployment

**Deployment Workflow:**

| Step | Action | Result |
|------|--------|--------|
| 1. Develop in Replit | Build/test locally | Working code |
| 2. Export code | Push to git repo | Code in repo |
| 3. Deploy to Coolify | Coolify auto-deploy | Production deployment |
| 4. Update env vars | Sync env vars to Coolify | Production config |

**Deployment Checklist:**
- ☐ Code tested in Replit
- ☐ Code pushed to git repo
- ☐ Coolify connected to repo
- ☐ Environment variables synced
- ☐ Health checks passing
- ☐ Test production deployment

---

## 9. File Map & Artifacts

- `/docs/replit-runbook.md` (new) → must exist
- `/replit.nix` (update) → Replit environment config
- `/.replit` (update) → Replit project settings

**Artifacts required:**
- Replit dev checklist → saved at `output/replit_dev_checklist.md`
- Replit env sync script path → saved at `output/replit_env_sync.sh` (path only, no content)

---

## 10. AI Agent Actions & Guardrails

**Actions:** generate Replit tunnel configurations; create env sync scripts; draft deployment checklists; document connection patterns to Coolify.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

