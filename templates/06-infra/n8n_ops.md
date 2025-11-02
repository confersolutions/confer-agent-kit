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

# n8n on Coolify Operations

**Purpose:** Operational guide for managing n8n on Coolify, including webhook URL patterns behind Traefik, auth/credentials vaulting, queues/concurrency, execution database, backups, version pinning, safe updates, rollbacks, and workflow export/import.

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

**Reference:** See [00_infra_conventions.md](00_infra_conventions.md) for ports, DNS, and routing conventions. See [coolify_platform.md](coolify_platform.md) for Coolify deployment patterns.

---

## 2. References & Inputs

External snippets/links cached in `output/` (gitignored):

- Project profile: `./confer-agent.profile.yml`

- n8n webhook patterns: `output/n8n_webhook_patterns.md`
- n8n backup restore: `output/n8n_backup_restore.md`
- n8n workflow examples: `output/n8n_workflows.md`

---

## 3. Webhook URL Patterns (Traefik)

**Webhook URL Structure:**

| Pattern | URL Format | Use Case |
|---------|------------|----------|
| Production | `https://n8n.yourdomain.com/webhook/[workflow-id]` | Production workflows |
| Staging | `https://n8n-staging.yourdomain.com/webhook/[workflow-id]` | Staging workflows |
| Test | `https://n8n.yourdomain.com/webhook-test/[workflow-id]` | Test workflows |

**Traefik Configuration:**
- Domain: `n8n.yourdomain.com`
- Internal port: `5678`
- Path prefix: `/webhook/*`
- TLS: Auto-certificate via Let's Encrypt

**Webhook URL Examples:**
```
Production: https://n8n.yourdomain.com/webhook/abc123
Staging: https://n8n-staging.yourdomain.com/webhook/xyz789
Test: https://n8n.yourdomain.com/webhook-test/test123
```

**Webhook Checklist:**
- ☐ Verify Traefik routing configured
- ☐ Test webhook URLs accessible
- ☐ Verify TLS certificate active
- ☐ Document webhook patterns
- ☐ Update workflows with correct URLs

---

## 4. Authentication & Credentials Vaulting

**Credential Storage:**

| Storage Type | Use Case | Security |
|--------------|----------|----------|
| n8n Credentials | Built-in vault | Encrypted at rest |
| Environment Variables | External API keys | Platform-managed |
| Secrets Manager | Sensitive credentials | External service |

**n8n Credentials Setup:**
1. **Create Credential:**
   - n8n UI → Credentials → New
   - Select credential type (API key, OAuth, etc.)
   - Enter credentials securely

2. **Use Credential in Workflow:**
   - Node configuration → Credentials
   - Select saved credential
   - Credentials encrypted and stored securely

**Environment Variables (Coolify):**
- Store API keys as Coolify env vars
- Access via `$env.API_KEY` in n8n
- Never hardcode in workflows

**Credential Vaulting Checklist:**
- ☐ Use n8n credentials for sensitive data
- ☐ Store external API keys as env vars
- ☐ Rotate credentials periodically
- ☐ Never commit credentials to repo
- ☐ Document credential requirements

---

## 5. Queues & Concurrency

**Queue Configuration:**

| Setting | Value | Impact |
|---------|-------|--------|
| Execution timeout | 3600s (1 hour) | Long-running workflows |
| Max concurrent executions | 10 | Parallel processing |
| Queue buffer | 100 | Pending executions |
| Retry attempts | 3 | Failed execution retries |

**Concurrency Settings (docker-compose.yml):**
```yaml
environment:
  - N8N_EXECUTIONS_TIMEOUT=3600
  - N8N_EXECUTIONS_TIMEOUT_MAX=7200
  - N8N_EXECUTIONS_PROCESS=main
  - N8N_EXECUTIONS_DATA_PRUNE=true
  - N8N_EXECUTIONS_DATA_MAX_AGE=168  # 7 days
```

**Queue Management:**
- **Active executions:** Monitor via n8n UI → Executions
- **Failed executions:** Retry or delete manually
- **Queue overflow:** Increase buffer or reduce concurrency

---

## 6. Executions Database

**Executions Storage:**

| Storage Type | Location | Retention |
|--------------|----------|-----------|
| Database | Postgres (n8n DB) | 7 days (auto-prune) |
| Logs | Application logs | 30 days |
| Archive | External backup | 90 days |

**Database Configuration:**
- Use Postgres database for executions
- Auto-prune old executions (7 days default)
- Backup database regularly (see Backup section)

**Execution Data Management:**
- ☐ Enable auto-prune (7 days retention)
- ☐ Monitor database size
- ☐ Archive old executions (if needed)
- ☐ Test restore from backup

---

## 7. Backups & Restore

**Backup Strategy:**

| Backup Type | Frequency | Retention | Location |
|-------------|-----------|-----------|----------|
| Workflow export | Weekly | 90 days | Git repo / external storage |
| Database backup | Daily | 30 days | External storage |
| Credentials backup | Monthly | 1 year | Encrypted external storage |

**Workflow Export:**
1. **Export Workflows:**
   - n8n UI → Workflows → Select workflows → Export
   - Export as JSON or ZIP
   - Save to git repo or external storage

2. **Import Workflows:**
   - n8n UI → Workflows → Import
   - Select exported file
   - Verify workflows imported correctly

**Database Backup:**
- Use Coolify backup feature (Postgres snapshots)
- Manual backup via `docker exec` commands
- Test restore process regularly

**Backup Checklist:**
- ☐ Export workflows weekly
- ☐ Backup database daily
- ☐ Store backups off-server (S3, external drive)
- ☐ Test restore process monthly
- ☐ Document restore procedures

---

## 8. Version Pinning & Safe Updates

**Version Pinning:**

| Component | Version | Pin Method |
|-----------|---------|------------|
| n8n image | `n8nio/n8n:latest` | Tag to specific version |
| n8n image | `n8nio/n8n:1.0.0` | Pin to version tag |
| Postgres | `postgres:15` | Pin to major version |

**Update Strategy:**
1. **Pin Current Version:**
   - Update docker-compose.yml with specific tag
   - Deploy to staging first
   - Test workflows in staging

2. **Safe Update Process:**
   - Backup workflows and database before update
   - Update image tag in docker-compose.yml
   - Deploy to staging → Test → Deploy to production
   - Monitor for errors after update

3. **Rollback Plan:**
   - Keep previous image tag available
   - Revert to previous version if issues occur
   - Restore from backup if needed

**Update Checklist:**
- ☐ Pin current version before update
- ☐ Backup workflows and database
- ☐ Test update in staging first
- ☐ Deploy to production after testing
- ☐ Monitor for errors after update
- ☐ Have rollback plan ready

---

## 9. Rollbacks

**Rollback Methods:**

| Method | Use Case | Steps |
|--------|----------|-------|
| Image rollback | Bad update | Revert image tag → Redeploy |
| Workflow restore | Corrupted workflows | Import previous export |
| Database restore | Data loss | Restore from backup |

**Rollback Process:**
1. **Image Rollback:**
   - Revert to previous image tag in docker-compose.yml
   - Deploy previous version
   - Verify workflows working

2. **Workflow Restore:**
   - Import previous workflow export
   - Verify workflows imported correctly
   - Test workflow execution

3. **Database Restore:**
   - Stop n8n service
   - Restore database from backup
   - Start n8n service
   - Verify data restored correctly

**Rollback Checklist:**
- ☐ Identify target version/backup
- ☐ Stop current deployment (if needed)
- ☐ Restore to previous version/backup
- ☐ Verify workflows working
- ☐ Monitor logs for errors
- ☐ Update documentation if needed

---

## 10. Workflow Export/Import

**Export Workflows:**
1. **Single Workflow:**
   - n8n UI → Workflow → Export
   - Export as JSON
   - Save to git repo or external storage

2. **Multiple Workflows:**
   - n8n UI → Workflows → Select multiple → Export
   - Export as ZIP or JSON
   - Save to git repo or external storage

**Import Workflows:**
1. **Import Workflow:**
   - n8n UI → Workflows → Import
   - Select exported file
   - Verify workflow imported correctly

2. **Import Multiple:**
   - n8n UI → Workflows → Import
   - Select ZIP file with multiple workflows
   - Verify all workflows imported correctly

**Workflow Management Checklist:**
- ☐ Export workflows regularly (weekly)
- ☐ Version control workflows (git repo)
- ☐ Test import/export process
- ☐ Document workflow dependencies
- ☐ Update workflows in staging before production

---

## 11. File Map & Artifacts

- `/docs/n8n-runbook.md` (new) → must exist
- `/docker-compose.yml` (update) → n8n service config

**Artifacts required:**
- n8n webhook patterns → saved at `output/n8n_webhook_patterns.md`
- n8n backup restore → saved at `output/n8n_backup_restore.md`

---

## 12. AI Agent Actions & Guardrails

**Actions:** generate webhook URL patterns; create credential vaulting guidelines; draft backup/restore procedures; document version pinning and rollback strategies.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

