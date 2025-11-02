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

# Domain & Schema Outline

**Purpose:** Define domain objects, relationships, canonical IDs, normalization choices, privacy flags, audit fields, and migration principles for the data model foundation.

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

- Domain research: `refs/domain-research.md`
- ER diagrams: `refs/er-diagrams.md`
- Data requirements: `refs/data-requirements.md`

---

## 3. Domain Objects & Relationships

**Entity Table:**

| Entity | Description | Primary Key | Key Attributes |
|--------|-------------|-------------|----------------|
| users | User accounts | id (UUID) | email, name, created_at |
| sessions | User sessions | id (UUID) | user_id, token, expires_at |
| [entity] | [description] | [key type] | [attributes] |

**Relationship Table:**

| Relationship | From Entity | To Entity | Type | Constraints |
|--------------|------------|-----------|------|-------------|
| user-session | users | sessions | one-to-many | on delete cascade |
| [relationship] | [entity] | [entity] | [type] | [constraints] |

---

## 4. Canonical IDs

**ID Strategy:**
- **Primary Keys:** UUID v4 (universally unique, no collisions)
- **Foreign Keys:** UUID references to parent entities
- **External IDs:** String identifiers for third-party services (e.g., Clerk user_id)

**ID Format Examples:**
- User ID: `550e8400-e29b-41d4-a716-446655440000`
- Session ID: `550e8400-e29b-41d4-a716-446655440001`

---

## 5. Normalization Choices

**Normalization Level:** 3NF (Third Normal Form)

**Denormalization Exceptions:**
- **User display names** cached on related tables (for performance)
- **Count aggregations** stored in summary tables (to avoid COUNT queries)
- **JSON columns** for flexible, schema-less data (e.g., metadata, preferences)

**Rationale:** Balance query performance with data consistency

---

## 6. Privacy Flags

**PII (Personally Identifiable Information):**
- ☐ Email addresses (encrypted at rest)
- ☐ Names (plain text, indexed)
- ☐ Phone numbers (encrypted)
- ☐ Addresses (encrypted)

**GDPR Compliance:**
- ☐ Right to deletion (soft delete with retention policy)
- ☐ Right to data export (JSON export functionality)
- ☐ Consent tracking (opt-in/opt-out flags)

**Access Control:**
- User data accessible only to owning user
- Admin roles required for cross-user queries

---

## 7. Audit Fields

**Standard Audit Columns:**
- `created_at` (timestamp, NOT NULL)
- `updated_at` (timestamp, auto-updated)
- `created_by` (user_id, nullable for system records)
- `updated_by` (user_id, nullable)
- `deleted_at` (timestamp, nullable, for soft deletes)
- `version` (integer, for optimistic locking if needed)

**Audit Log Table:**
- `audit_logs` table for critical operations (who, what, when, changes)

---

## 8. Soft-Delete/Versioning Strategy

**Soft Delete:**
- ☐ Use `deleted_at` timestamp column
- ☐ Filter out deleted records in default queries
- ☐ Retention policy: [30 days / 90 days / permanent]
- ☐ Physical deletion after retention period (GDPR compliance)

**Versioning:**
- ☐ Optimistic locking with `version` column
- ☐ Audit trail via `audit_logs` table
- ☐ No full version history tables (use audit logs if needed)

---

## 9. Index Strategy

**Primary Indexes:**
- Primary key columns (automatic)
- Foreign key columns (for join performance)

**Secondary Indexes:**
- Frequently queried columns (e.g., `email`, `user_id`)
- Composite indexes for multi-column queries
- Partial indexes for soft-delete filtering (`WHERE deleted_at IS NULL`)

**Index Considerations:**
- Balance read performance with write overhead
- Monitor slow queries and add indexes as needed

---

## 9a. Multi-Tenant Strategy

**Tenant Isolation:**

| Strategy | Approach | Pros | Cons |
|----------|----------|------|------|
| Single DB w/ tenant_id | All tenants in one DB | Cost-effective, easy queries | Data leakage risk (needs RLS) |
| Schema-per-tenant | Separate schema per tenant | Strong isolation | Higher complexity, cost |

**Selected Strategy:** [Single DB w/ tenant_id | Schema-per-tenant]

**Row-Level Security (RLS) Policy Notes:**
- Enable RLS on tenant-scoped tables
- Policy: `WHERE tenant_id = current_setting('app.tenant_id')::uuid`
- Enforce at application layer (defense in depth)

**Retention & Backups:**
- **Data retention:** [30 days / 90 days / permanent] per tenant
- **Backup frequency:** Daily snapshots with 7-day retention
- **Restore procedure:** Tenant-specific restore available
- **Compliance:** GDPR deletion handled via soft-delete → physical delete after retention period

---

## 10. Migration Principles

**Migration Rules:**
- ☐ All migrations reversible (up and down migrations)
- ☐ No data loss in up migrations
- ☐ Test migrations on staging before production
- ☐ Backup production database before major migrations
- ☐ Migrations are atomic (all or nothing)

**Migration Naming:**
- Format: `YYYYMMDD_HHMMSS_description.sql`
- Example: `20251101_120000_add_referral_code.sql`

**Schema Changes:**
- Add columns as nullable first, then backfill, then make NOT NULL
- Use transactions for multi-step schema changes

---

## 11. File Map & Artifacts

- `/db/schema.sql` (new) → must exist
- `/db/migrations/` (new) → migration folder
- `/docs/data-model.md` (new) → data model documentation

**Artifacts required:**
- Entity table → saved at `refs/entity-table.md`
- Relationship list → saved at `refs/relationship-list.md`
- Draft ER notes (bullets) → saved at `refs/er-notes.md`

---

## 12. AI Agent Actions & Guardrails

**Actions:** generate entity table with relationships; define canonical ID strategy; create normalization and privacy guidelines; draft migration principles.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

