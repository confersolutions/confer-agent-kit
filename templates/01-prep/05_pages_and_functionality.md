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

# App IA & Feature Map

**Purpose:** Define sitemap, core user flows, page responsibilities, acceptance criteria, and non-functional requirements per page/flow.

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

- User flows: `refs/user-flows.md`
- Feature requirements: `refs/feature-requirements.md`
- IA research: `refs/information-architecture.md`

---

## 3. Sitemap

| Page | Path | Purpose | Auth Required | Priority |
|------|------|---------|---------------|----------|
| Home | `/` | Landing page, value prop | No | High |
| Login | `/login` | User authentication | No | High |
| Signup | `/signup` | User registration | No | High |
| Dashboard | `/dashboard` | Main user workspace | Yes | High |
| Profile | `/profile` | User settings | Yes | Medium |
| Settings | `/settings` | Account configuration | Yes | Medium |
| [Page] | `/[path]` | [Purpose] | [Yes/No] | [Priority] |

---

## 4. Core Flows

**Flow 1: User Onboarding**
- Landing page → Signup → Email verification → Dashboard
- Key steps: [bullet points]
- Exit points: [where users might drop off]

**Flow 2: Authentication**
- Login → Dashboard (existing user)
- Signup → Email verification → Dashboard (new user)
- Password reset → New password → Login

**Flow 3: [Core Feature]**
- Entry point → [steps] → Completion
- Key interactions: [bullets]

**Flow 4: [Additional Flow]**
- [Description]

---

## 5. Page Responsibilities (RACI - Optional)

| Page/Component | Responsibility | Auth | Notes |
|----------------|----------------|------|-------|
| Dashboard | Display user data, navigation | Yes | Main workspace |
| Profile | User info display/edit | Yes | Read/write access |
| Settings | System configuration | Yes | Admin-only features |

---

## 6. Acceptance Criteria per Page

**Page: Home**
- ☐ Hero section with clear value proposition
- ☐ CTA buttons functional
- ☐ Responsive on mobile/desktop
- ☐ Fast load time (< 2s)
- ☐ Loading state: skeleton screen during data fetch
- ☐ Empty state: message when no content
- ☐ Error state: error message with retry option

**Page: Dashboard**
- ☐ User data displayed correctly
- ☐ Navigation accessible
- ☐ Real-time updates (if applicable)
- ☐ Error states handled gracefully
- ☐ Loading state: spinner or skeleton during data load
- ☐ Empty state: onboarding message when no data
- ☐ Error state: error message with fallback actions

**Page: [Page Name]**
- ☐ [Criterion 1]
- ☐ [Criterion 2]
- ☐ [Criterion 3]
- ☐ Loading state: [description]
- ☐ Empty state: [description]
- ☐ Error state: [description]

---

## 7. Non-Functional Requirements per Flow

| Flow | Performance | Security | Accessibility | Notes |
|------|-------------|----------|--------------|-------|
| Onboarding | < 3s page load | Encrypt PII | Screen reader support | Critical path |
| Authentication | < 2s login | 2FA available | Keyboard nav | Security critical |
| [Flow] | [Target] | [Requirements] | [Requirements] | [Notes] |

---

## 7a. Event Map (Telemetry)

| Event | When | Properties |
|-------|------|------------|
| `page_view` | Page loaded | `page`, `path`, `user_id` |
| `button_click` | User clicks button | `button_id`, `page`, `user_id` |
| `form_submit` | Form submitted | `form_id`, `page`, `success` |
| `user_signup` | User registration | `method`, `user_id` |
| `user_login` | User login | `method`, `user_id` |
| `feature_used` | Feature interaction | `feature_name`, `user_id` |

**Telemetry to Emit:** Standard product analytics events (page views, button clicks, form submits, feature usage) for consistent tracking across all pages and flows.

---

## 8. File Map & Artifacts

- `/docs/sitemap.md` (new) → must exist
- `/docs/user-flows.md` (new) → flow documentation
- `/docs/acceptance-criteria.md` (new) → criteria per page

**Artifacts required:**
- Sitemap table → saved at `refs/sitemap.md`
- Acceptance criteria checklist → saved at `refs/acceptance-criteria.md`

---

## 9. AI Agent Actions & Guardrails

**Actions:** generate sitemap table; define core user flows; create acceptance criteria checklist; document NFRs per flow.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

