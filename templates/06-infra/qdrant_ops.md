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

# Qdrant on Coolify Operations

**Purpose:** Operational guide for managing Qdrant vector database on Coolify, including collection schema strategy, distance/quantization choices, snapshots/backups, memory/CPU sizing, gRPC/HTTP ports, and networking to application services.

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

External snippets/links cached in `output/` (gitignored):

- Project profile: `./confer-agent.profile.yml`

- Qdrant snapshot runbook: `output/qdrant_snapshot_runbook.md`
- Qdrant collections table: `output/qdrant_collections_table.csv`
- Qdrant configuration: `output/qdrant_config.md`

---

## 3. Collection Schema Strategy

**Collection Naming Convention:**

| Pattern | Example | Use Case |
|---------|---------|----------|
| `[app]_[type]_[env]` | `confer_embeddings_prod` | Production embeddings |
| `[app]_[type]_[env]` | `confer_embeddings_staging` | Staging embeddings |
| `[app]_[type]_v[version]` | `confer_embeddings_v1` | Versioned collections |

**Collection Schema Example:**

| Field | Type | Purpose |
|-------|------|---------|
| `id` | UUID | Unique identifier |
| `vector` | Float array | Embedding vector |
| `payload` | JSON | Metadata (text, tags, etc.) |
| `score` | Float | Similarity score (computed) |

**Schema Strategy:**
- Use consistent collection names across environments
- Include environment suffix (prod/staging/dev)
- Version collections when schema changes
- Document collection purposes and schemas

---

## 4. Distance & Quantization Choices

**Distance Metrics:**

| Metric | Use Case | Performance |
|--------|----------|-------------|
| Cosine | Text embeddings | Best for semantic similarity |
| Euclidean | Spatial data | Good for geometric similarity |
| Dot Product | Dense vectors | Fast but less accurate |

**Quantization Options:**

| Method | Accuracy | Storage | Performance |
|--------|----------|---------|-------------|
| Scalar | Medium | High | Fast |
| Product | High | Medium | Medium |
| Binary | Low | Very High | Very Fast |

**Distance Selection Guidelines:**
- **Text embeddings:** Cosine (recommended)
- **Image embeddings:** Cosine or Euclidean
- **Dense vectors:** Dot Product (if applicable)

**Quantization Selection Guidelines:**
- **Production (high accuracy):** Product quantization
- **Development (speed):** Scalar quantization
- **Large datasets (storage):** Binary quantization

---

## 5. Snapshots & Backups

**Snapshot Strategy:**

| Frequency | Retention | Location | Use Case |
|-----------|-----------|----------|----------|
| Daily | 7 days | Local storage | Short-term recovery |
| Weekly | 30 days | External storage | Medium-term recovery |
| Monthly | 90 days | External storage | Long-term archive |

**Snapshot Creation (Manual):**
```bash
# Via Qdrant API
curl -X POST "http://qdrant:6333/collections/{collection_name}/snapshots"

# Via Qdrant CLI (if available)
qdrant snapshot create --collection {collection_name}
```

**Snapshot Restore:**
```bash
# Via Qdrant API
curl -X POST "http://qdrant:6333/collections/{collection_name}/snapshots/{snapshot_name}/recover"

# Via Qdrant CLI (if available)
qdrant snapshot recover --collection {collection_name} --snapshot {snapshot_name}
```

**Backup Checklist:**
- ☐ Enable automated snapshots (if supported)
- ☐ Create manual snapshots before major changes
- ☐ Store snapshots off-server (S3, external drive)
- ☐ Test restore process regularly
- ☐ Document restore procedures

---

## 6. Memory & CPU Sizing

**Resource Allocation:**

| Workload | CPU | Memory | Storage | Use Case |
|----------|-----|--------|---------|----------|
| Small (<100K vectors) | 2 cores | 4GB | 50GB | Development |
| Medium (100K–1M vectors) | 4 cores | 8GB | 200GB | Staging |
| Large (>1M vectors) | 8 cores | 16GB | 500GB | Production |

**Sizing Guidelines:**
- **Memory:** Allocate 2–4GB per 100K vectors (rough estimate)
- **CPU:** More cores for concurrent queries (scales linearly)
- **Storage:** Vector storage ≈ 4 bytes per dimension per vector

**Resource Monitoring:**
- Monitor memory usage (Qdrant metrics)
- Monitor CPU usage (system metrics)
- Monitor disk usage (snapshots + data)
- Scale up resources if needed

---

## 7. gRPC & HTTP Ports

**Port Configuration:**

| Port | Protocol | Purpose | Access |
|------|----------|---------|--------|
| 6333 | HTTP | REST API | Internal/external |
| 6334 | gRPC | High-performance API | Internal/external |

**Port Access Patterns:**

| Access Type | URL Format | Use Case |
|-------------|------------|----------|
| Internal (HTTP) | `http://qdrant:6333` | Coolify internal services |
| Internal (gRPC) | `qdrant:6334` | High-performance queries |
| External (HTTP) | `https://qdrant.yourdomain.com` | Public API (if needed) |

**Port Configuration (docker-compose.yml):**
```yaml
ports:
  - "6333:6333"  # HTTP
  - "6334:6334"  # gRPC
```

**Port Security:**
- **Internal:** Only accessible within Coolify network
- **External:** Expose via Traefik (if needed)
- **TLS:** Use Traefik for HTTPS (if external)

---

## 8. Networking to Application Services

**Service Communication:**

| Service | Connection Method | URL | Authentication |
|---------|-------------------|-----|----------------|
| Flowise | Internal HTTP | `http://qdrant:6333` | None (internal) |
| FastAPI | Internal HTTP | `http://qdrant:6333` | None (internal) |
| n8n | Internal HTTP | `http://qdrant:6333` | None (internal) |

**Connection Configuration (Flowise):**
- Use internal Coolify network (service name: `qdrant`)
- Port: `6333` (HTTP) or `6334` (gRPC)
- No authentication needed (internal network)

**Connection Configuration (FastAPI):**
```python
# Example Qdrant client configuration
from qdrant_client import QdrantClient

client = QdrantClient(
    url="http://qdrant:6333",  # Internal Coolify network
    prefer_grpc=True,  # Use gRPC for better performance
)
```

**Network Security:**
- **Internal:** No authentication (trusted network)
- **External:** Use Traefik with TLS (if exposed)
- **Firewall:** Restrict access to internal services only

---

## 9. Collections Management

**Collection Operations:**

| Operation | Method | Use Case |
|-----------|--------|----------|
| Create | API/CLI | New collection setup |
| List | API/CLI | Collection inventory |
| Delete | API/CLI | Collection cleanup |
| Update | API/CLI | Schema changes |

**Collection Management Checklist:**
- ☐ Document collection purposes and schemas
- ☐ Version collections when schema changes
- ☐ Backup collections before major changes
- ☐ Monitor collection sizes and performance
- ☐ Archive old collections (if needed)

---

## 10. File Map & Artifacts

- `/docs/qdrant-runbook.md` (new) → must exist
- `/docker-compose.yml` (update) → Qdrant service config

**Artifacts required:**
- Qdrant snapshot runbook → saved at `output/qdrant_snapshot_runbook.md`
- Qdrant collections table → saved at `output/qdrant_collections_table.csv`

---

## 11. AI Agent Actions & Guardrails

**Actions:** generate collection schema templates; create snapshot/backup procedures; document distance/quantization choices; draft networking configuration guides.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

