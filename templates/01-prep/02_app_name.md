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

# Naming & Positioning

**Purpose:** Generate and evaluate candidate app names with criteria for memorability, domain availability, trademark safety, and positioning alignment.

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

- Competitor names: `refs/competitor-names.md`
- Brand mood board: `refs/brand-mood.md`
- Domain research: `refs/domain-research.md`

---

## 3. Naming Criteria

**Must-Have:**
- ☐ Memorable and easy to pronounce
- ☐ Domain available (.com, .ai, or equivalent)
- ☐ Trademark search passed (USPTO, EU)
- ☐ No negative connotations in target markets
- ☐ SEO-friendly (if applicable)

**Nice-to-Have:**
- ☐ Short (≤ 10 characters preferred)
- ☐ Available on major social platforms
- ☐ Works in multiple languages

---

## 4. Positioning Statements

**Target Audience:** [primary user group]

**Positioning:** "[App name] helps [target audience] [achieve outcome] by [key differentiator]."

**Value Proposition:** One sentence that captures core value.

---

## 5. Name Candidates by Theme

**Theme 1: [Theme Name]**
- Candidate 1
- Candidate 2
- Candidate 3

**Theme 2: [Theme Name]**
- Candidate 1
- Candidate 2
- Candidate 3

**Theme 3: [Theme Name]**
- Candidate 1
- Candidate 2
- Candidate 3

*Total: 15–25 candidates across 3–5 themes*

---

## 6. Shortlist Rubric

| Candidate | Memorable | Domain | Trademark | Brand Fit | Total Score |
|-----------|-----------|--------|-----------|-----------|-------------|
| Name 1    | [1-5]     | [1-5]  | [1-5]     | [1-5]     | [sum]       |
| Name 2    | [1-5]     | [1-5]  | [1-5]     | [1-5]     | [sum]       |
| Name 3    | [1-5]     | [1-5]  | [1-5]     | [1-5]     | [sum]       |

*Score each on scale 1–5; total determines shortlist*

---

## 7. Final Selection Worksheet

**Top 3 Finalists:**
1. **Name:** [name]
   - Domain: [status]
   - Trademark: [status]
   - Rationale: [why this name]

2. **Name:** [name]
   - Domain: [status]
   - Trademark: [status]
   - Rationale: [why this name]

3. **Name:** [name]
   - Domain: [status]
   - Trademark: [status]
   - Rationale: [why this name]

**Selected Name:** [final choice]

**Decision Rationale:** [brief explanation]

---

## 7a. Legal Checklist

**USPTO Search:**
- ☐ USPTO trademark search completed: [link to search](https://www.uspto.gov/trademarks/search)
- ☐ Class selection: [International Class #] for [goods/services]
- ☐ Conflict log: [document any similar marks found]

**Trademark Considerations:**
- ☐ No conflicts with existing marks in target markets
- ☐ Available for registration (if applicable)
- ☐ Clearance letter from legal (if needed)

**Pronunciation & Accessibility:**
- **Pronunciation:** [phonetic spelling, e.g., "con-fer" or "CON-fur"]
- **Screen reader test:** ☐ Tested with screen reader software
- **A11y notes:** [any pronunciation challenges, alternatives]

---

## 8. File Map & Artifacts

- `/docs/app-naming.md` (new) → must exist
- `/docs/positioning.md` (new) → positioning statement document

**Artifacts required:**
- Name candidates CSV → saved at `refs/name-candidates.csv`
- Positioning one-liner → saved at `refs/positioning-oneliner.txt`

---

## 9. AI Agent Actions & Guardrails

**Actions:** generate name candidates across themes; evaluate domain/trademark availability; create scoring rubric; draft positioning statements.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

