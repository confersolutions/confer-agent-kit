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

# Flowise on Coolify Operations

**Purpose:** Operational guide for managing Flowise on Coolify, including model keys/secrets, connectors to Qdrant/Neo4j, prompt caching, authentication, logs, flow export/import, and rate-limit/timeout strategies.

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

**Reference:** See [00_infra_conventions.md](00_infra_conventions.md) for ports, DNS, and routing conventions. See [coolify_platform.md](coolify_platform.md) for Coolify deployment patterns. See [qdrant_ops.md](qdrant_ops.md) and [neo4j_ops.md](neo4j_ops.md) for database connector details.

---

## 2. References & Inputs

External snippets/links cached in `refs/` (gitignored):

- Project profile: `./confer-agent.profile.yml`

- Flowise connectors: `refs/flowise_connectors.md`
- Flowise ops checklist: `refs/flowise_ops_checklist.md`
- Flowise flow examples: `refs/flowise_flows.md`

---

## 3. Model Keys & Secrets

**LLM Provider Keys:**

| Provider | Env Var | Purpose |
|----------|---------|---------|
| OpenAI | `OPENAI_API_KEY` | GPT models |
| Anthropic | `ANTHROPIC_API_KEY` | Claude models |
| Cohere | `COHERE_API_KEY` | Cohere models |
| Hugging Face | `HUGGINGFACE_API_KEY` | Open-source models |

**Secret Management:**
- Store keys as Coolify env vars (encrypted storage)
- Never commit keys to repo
- Rotate keys periodically
- Use different keys per environment (dev/staging/prod)

**Key Setup Checklist:**
- ☐ Add provider keys as Coolify env vars
- ☐ Verify keys loaded at runtime
- ☐ Test LLM provider connections
- ☐ Document key requirements
- ☐ Rotate keys periodically

---

## 4. Connectors to Qdrant/Neo4j

**Qdrant Connector:**

| Setting | Value | Purpose |
|---------|-------|---------|
| Connection URL | `http://qdrant:6333` | Internal Coolify network |
| Collection Name | `[collection-name]` | Vector store collection |
| Embedding Model | `text-embedding-ada-002` | Embedding generation |

**Qdrant Connection (Flowise):**
- Use internal Coolify network (service name: `qdrant`)
- Port: `6333` (HTTP) or `6334` (gRPC)
- No external authentication needed (internal network)

**Neo4j Connector:**

| Setting | Value | Purpose |
|---------|-------|---------|
| Connection URL | `bolt://neo4j:7687` | Internal Coolify network |
| Username | `neo4j` | Database user |
| Password | `[password]` | Database password (env var) |

**Neo4j Connection (Flowise):**
- Use internal Coolify network (service name: `neo4j`)
- Port: `7687` (Bolt) or `7474` (HTTP)
- Authentication: Username/password (stored as env vars)

**Connector Setup Checklist:**
- ☐ Configure Qdrant connector (internal URL)
- ☐ Configure Neo4j connector (internal URL)
- ☐ Test connections from Flowise
- ☐ Verify data access (read/write)
- ☐ Document connector configurations

---

## 5. Prompt Caching

**Caching Strategy:**

| Cache Type | Duration | Use Case |
|------------|----------|----------|
| Prompt cache | 1 hour | Repeated prompts |
| Embedding cache | 24 hours | Vector embeddings |
| Response cache | 30 minutes | API responses |

**Prompt Cache Configuration:**
- Enable prompt caching in Flowise UI
- Set cache duration per flow
- Monitor cache hit rate
- Clear cache when needed (UI or API)

**Caching Best Practices:**
- Cache static prompts (system prompts, templates)
- Don't cache dynamic prompts (user-specific data)
- Monitor cache storage size
- Rotate cache periodically

---

## 6. Authentication

**Authentication Methods:**

| Method | Use Case | Setup |
|--------|----------|-------|
| Basic Auth | Simple protection | Flowise UI → Settings |
| JWT | API access | External auth service |
| API Key | Service-to-service | Flowise API key |

**Basic Auth Setup:**
1. **Enable in Flowise:**
   - Flowise UI → Settings → Authentication
   - Enable basic auth
   - Set username/password (env vars)

2. **Configure Env Vars:**
   ```
   FLOWISE_USERNAME=admin
   FLOWISE_PASSWORD=[secure-password]
   ```

**API Key Setup:**
1. **Generate API Key:**
   - Flowise UI → Settings → API Keys
   - Generate new API key
   - Save key securely (Coolify env vars)

2. **Use API Key:**
   - Include in API requests: `Authorization: Bearer [key]`
   - Store in external services (as env var)

**Authentication Checklist:**
- ☐ Enable basic auth (if needed)
- ☐ Generate API keys for service access
- ☐ Store credentials securely (env vars)
- ☐ Test authentication
- ☐ Document auth requirements

---

## 7. Logs & Monitoring

**Log Access:**

| Location | Access Method | Use Case |
|----------|---------------|----------|
| Flowise UI | Built-in logs | Recent executions |
| Coolify UI | Container logs | System logs |
| External | Log aggregation service | Centralized logging |

**Log Levels:**
- ERROR: Critical issues (LLM failures, connector errors)
- WARN: Potential issues (rate limits, timeouts)
- INFO: Normal operations (flow executions, API calls)
- DEBUG: Verbose logging (disable in production)

**Log Configuration:**
- Configure log levels in Flowise settings
- Export logs to external service (if needed)
- Monitor logs for errors/warnings
- Archive old logs (external storage)

---

## 8. Flow Export/Import

**Export Flows:**
1. **Single Flow:**
   - Flowise UI → Flow → Export
   - Export as JSON
   - Save to git repo or external storage

2. **Multiple Flows:**
   - Flowise UI → Flows → Select multiple → Export
   - Export as ZIP or JSON
   - Save to git repo or external storage

**Import Flows:**
1. **Import Flow:**
   - Flowise UI → Flows → Import
   - Select exported file
   - Verify flow imported correctly

2. **Import Multiple:**
   - Flowise UI → Flows → Import
   - Select ZIP file with multiple flows
   - Verify all flows imported correctly

**Flow Management Checklist:**
- ☐ Export flows regularly (weekly)
- ☐ Version control flows (git repo)
- ☐ Test import/export process
- ☐ Document flow dependencies
- ☐ Update flows in staging before production

---

## 9. Rate-Limit & Timeout Strategy

**Rate Limiting:**

| Provider | Rate Limit | Strategy |
|----------|------------|----------|
| OpenAI | 60 req/min | Throttle requests |
| Anthropic | 50 req/min | Throttle requests |
| Cohere | 100 req/min | Throttle requests |

**Timeout Configuration:**

| Timeout Type | Duration | Use Case |
|--------------|----------|----------|
| LLM request | 60s | Standard requests |
| Long context | 120s | Large prompts |
| Embedding | 30s | Vector generation |
| Connector | 30s | Qdrant/Neo4j queries |

**Rate-Limit Strategy:**
- Implement request queuing for high-volume flows
- Use exponential backoff for rate-limited requests
- Monitor rate-limit errors (logs/alerts)
- Scale up providers if needed (higher tier plans)

**Timeout Strategy:**
- Set appropriate timeouts per operation type
- Implement retry logic for timeouts
- Monitor timeout errors (logs/alerts)
- Optimize slow operations (reduce context size, etc.)

---

## 10. File Map & Artifacts

- `/docs/flowise-runbook.md` (new) → must exist
- `/docker-compose.yml` (update) → Flowise service config

**Artifacts required:**
- Flowise connectors → saved at `refs/flowise_connectors.md`
- Flowise ops checklist → saved at `refs/flowise_ops_checklist.md`

---

## 11. AI Agent Actions & Guardrails

**Actions:** generate connector configurations for Qdrant/Neo4j; create rate-limit and timeout strategies; draft backup/restore procedures; document authentication setup.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

