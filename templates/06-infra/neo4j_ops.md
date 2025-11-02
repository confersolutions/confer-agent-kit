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

# Neo4j on Coolify Operations

**Purpose:** Operational guide for managing Neo4j graph database on Coolify, including image/tag selection, APOC configuration, Bolt/HTTP ports, volumes for data/logs, authentication and roles, backup/restore procedures, tuning basics (heap/pagecache), and connectors to application services.

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

**Reference:** See [00_infra_conventions.md](00_infra_conventions.md) for ports, DNS, and routing conventions. See [coolify_platform.md](coolify_platform.md) for Coolify deployment patterns. See [flowise_ops.md](flowise_ops.md) for Flowise connector configuration.

---

## 2. References & Inputs

External snippets/links cached in `refs/` (gitignored):

- Project profile: `./confer-agent.profile.yml`

- Neo4j backup runbook: `refs/neo4j_backup_runbook.md`
- Neo4j config examples: `refs/neo4j_config_examples.md`
- Neo4j tuning guide: `refs/neo4j_tuning.md`

---

## 3. Image & Tag Selection

**Image Selection:**

| Image | Tag | Use Case |
|-------|-----|----------|
| `neo4j` | `5.x` | Latest stable |
| `neo4j` | `5.15` | Specific version |
| `neo4j:enterprise` | `5.x` | Enterprise features |

**Version Selection Guidelines:**
- **Production:** Pin to specific version (e.g., `5.15`)
- **Staging:** Use minor version (e.g., `5.x`)
- **Development:** Use latest (e.g., `latest`) or specific version

**Image Configuration (docker-compose.yml):**
```yaml
image: neo4j:5.15
# or
image: neo4j:enterprise:5.15
```

**Tag Selection Checklist:**
- ☐ Pin to specific version for production
- ☐ Use enterprise image if needed (APOC, plugins)
- ☐ Test new versions in staging first
- ☐ Document version in deployment config

---

## 4. APOC Configuration

**APOC (Awesome Procedures on Cypher):**

| Feature | Use Case | Configuration |
|---------|----------|----------------|
| APOC Core | Basic procedures | Pre-installed |
| APOC Extended | Advanced procedures | Requires config |
| APOC Full | All procedures | Requires config |

**APOC Configuration:**
```yaml
# docker-compose.yml
environment:
  - NEO4J_PLUGINS=["apoc"]
  - NEO4J_apoc_export_file_enabled=true
  - NEO4J_apoc_import_file_enabled=true
```

**APOC Usage Examples:**
- **Import CSV:** `CALL apoc.load.csv('file.csv')`
- **Export JSON:** `CALL apoc.export.json.all('file.json')`
- **Data import/export:** Various APOC procedures

**APOC Configuration Checklist:**
- ☐ Enable APOC plugins in environment variables
- ☐ Verify APOC procedures available (`CALL apoc.help()`)
- ☐ Test APOC procedures in staging
- ☐ Document APOC usage in code/docs

---

## 5. Bolt & HTTP Ports

**Port Configuration:**

| Port | Protocol | Purpose | Access |
|------|----------|---------|--------|
| 7474 | HTTP | Browser UI | Internal/external |
| 7687 | Bolt | Database protocol | Internal/external |

**Port Access Patterns:**

| Access Type | URL Format | Use Case |
|-------------|------------|----------|
| Internal (Bolt) | `bolt://neo4j:7687` | Application connections |
| Internal (HTTP) | `http://neo4j:7474` | Browser UI (internal) |
| External (HTTP) | `https://neo4j.yourdomain.com` | Browser UI (external) |

**Port Configuration (docker-compose.yml):**
```yaml
ports:
  - "7474:7474"  # HTTP
  - "7687:7687"  # Bolt
```

**Port Security:**
- **Internal:** Only accessible within Coolify network
- **External:** Expose via Traefik (if needed)
- **TLS:** Use Traefik for HTTPS (if external)

---

## 6. Volumes for Data & Logs

**Volume Configuration:**

| Volume Type | Path | Purpose | Backup Strategy |
|-------------|------|---------|----------------|
| Data volume | `/data` | Database data | Daily snapshots |
| Logs volume | `/logs` | Application logs | Rotation + archival |
| Config volume | `/config` | Configuration files | Git repo |

**Volume Setup (docker-compose.yml):**
```yaml
volumes:
  - neo4j-data:/data
  - neo4j-logs:/logs
  - neo4j-config:/config

volumes:
  neo4j-data:
    driver: local
  neo4j-logs:
    driver: local
  neo4j-config:
    driver: local
```

**Volume Backup Checklist:**
- ☐ Identify critical volumes (data, logs)
- ☐ Set up automated backups (daily/weekly)
- ☐ Test restore process regularly
- ☐ Store backups off-server (S3, external drive)

---

## 7. Authentication & Roles

**Authentication Methods:**

| Method | Use Case | Configuration |
|--------|----------|---------------|
| Native | Default | `NEO4J_AUTH=neo4j/password` |
| LDAP | Enterprise | LDAP configuration |
| SSO | Enterprise | SSO configuration |

**Role-Based Access Control (RBAC):**

| Role | Permissions | Use Case |
|------|------------|----------|
| Admin | Full access | Database administration |
| Publisher | Read/write | Application access |
| Reader | Read-only | Reporting/analytics |

**Authentication Setup:**
```yaml
# docker-compose.yml
environment:
  - NEO4J_AUTH=neo4j/[secure-password]
  # or
  - NEO4J_AUTH=none  # Disable auth (dev only)
```

**Role Configuration (Cypher):**
```cypher
CREATE ROLE publisher;
GRANT WRITE ON GRAPH * TO publisher;
GRANT READ ON GRAPH * TO publisher;
```

**Authentication Checklist:**
- ☐ Set secure password via env var
- ☐ Create roles for application access
- ☐ Assign roles to users
- ☐ Test authentication in staging
- ☐ Document authentication requirements

---

## 8. Backup & Restore

**Backup Strategy:**

| Frequency | Retention | Location | Use Case |
|-----------|-----------|----------|----------|
| Daily | 7 days | Local storage | Short-term recovery |
| Weekly | 30 days | External storage | Medium-term recovery |
| Monthly | 90 days | External storage | Long-term archive |

**Backup Methods:**

| Method | Use Case | Command |
|--------|----------|---------|
| `neo4j-admin dump` | Full backup | `neo4j-admin database dump` |
| APOC export | Data export | `CALL apoc.export.graphml.all()` |
| Volume snapshot | Volume-level | Docker volume backup |

**Backup Creation (Manual):**
```bash
# Via neo4j-admin (in container)
docker exec neo4j neo4j-admin database dump --database=neo4j --to=/backups/neo4j.dump

# Via APOC (Cypher)
CALL apoc.export.graphml.all('backup.graphml', {})
```

**Restore Procedure:**
```bash
# Via neo4j-admin (in container)
docker exec neo4j neo4j-admin database load --database=neo4j --from=/backups/neo4j.dump --overwrite-destination=true
```

**Backup Checklist:**
- ☐ Enable automated backups (if supported)
- ☐ Create manual backups before major changes
- ☐ Store backups off-server (S3, external drive)
- ☐ Test restore process regularly
- ☐ Document restore procedures

---

## 9. Tuning Basics (Heap & Pagecache)

**Memory Configuration:**

| Setting | Default | Recommended | Purpose |
|---------|---------|--------------|---------|
| Heap Size | 512MB | 4GB–8GB | JVM heap memory |
| Pagecache | 512MB | 4GB–8GB | File system cache |

**Memory Configuration (docker-compose.yml):**
```yaml
environment:
  - NEO4J_dbms_memory_heap_initial__size=4g
  - NEO4J_dbms_memory_heap_max__size=4g
  - NEO4J_dbms_memory_pagecache_size=4g
```

**Memory Sizing Guidelines:**
- **Heap:** 50% of available memory (max 8GB)
- **Pagecache:** 50% of available memory (max 8GB)
- **Total:** Don't exceed available system memory

**Tuning Checklist:**
- ☐ Set appropriate heap size (4GB–8GB)
- ☐ Set appropriate pagecache size (4GB–8GB)
- ☐ Monitor memory usage (metrics/logs)
- ☐ Adjust based on workload
- ☐ Document tuning decisions

---

## 10. Connectors to Application Services

**Service Communication:**

| Service | Connection Method | URL | Authentication |
|---------|-------------------|-----|---------------|
| Flowise | Bolt protocol | `bolt://neo4j:7687` | Username/password |
| FastAPI | Bolt protocol | `bolt://neo4j:7687` | Username/password |
| n8n | HTTP API | `http://neo4j:7474` | Username/password |

**Connection Configuration (Flowise):**
- Use internal Coolify network (service name: `neo4j`)
- Port: `7687` (Bolt) or `7474` (HTTP)
- Authentication: Username/password (stored as env vars)

**Connection Configuration (FastAPI):**
```python
# Example Neo4j driver configuration
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://neo4j:7687",  # Internal Coolify network
    auth=("neo4j", os.getenv("NEO4J_PASSWORD"))
)
```

**Network Security:**
- **Internal:** Use username/password authentication
- **External:** Use Traefik with TLS (if exposed)
- **Firewall:** Restrict access to internal services only

---

## 11. File Map & Artifacts

- `/docs/neo4j-runbook.md` (new) → must exist
- `/docker-compose.yml` (update) → Neo4j service config

**Artifacts required:**
- Neo4j backup runbook → saved at `refs/neo4j_backup_runbook.md`
- Neo4j config examples → saved at `refs/neo4j_config_examples.md`

---

## 12. AI Agent Actions & Guardrails

**Actions:** generate image/tag selection guidelines; create APOC configuration templates; draft backup/restore procedures; document memory tuning and connector setup.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

