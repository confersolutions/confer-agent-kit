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

# Wireframe Planning

**Purpose:** Plan wireframe creation with page lists, component breakdowns, layout heuristics, responsive breakpoints, and annotation standards.

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

External snippets/links cached in `output/` (gitignored):

- Project profile: `./confer-agent.profile.yml`

- Sitemap: `output/sitemap.md`
- User flows: `output/user-flows.md`
- Design inspiration: `output/wireframe-inspiration.md`

---

## 3. Wireframe List by Page

| Page | Wireframe Files | Priority | Status |
|------|----------------|----------|--------|
| Home | `home-desktop.png`, `home-mobile.png` | High | ☐ Draft |
| Login | `login-desktop.png`, `login-mobile.png` | High | ☐ Draft |
| Dashboard | `dashboard-desktop.png`, `dashboard-mobile.png` | High | ☐ Draft |
| Profile | `profile-desktop.png`, `profile-mobile.png` | Medium | ☐ Draft |
| [Page] | `[page]-desktop.png`, `[page]-mobile.png` | [Priority] | ☐ Draft |

---

## 4. Key Components per Frame

**Home Page:**
- Hero section (headline, CTA, image)
- Feature highlights (3-column grid)
- Testimonials section
- Footer (links, copyright)

**Dashboard:**
- Navigation sidebar
- Main content area
- Data visualization widget
- Action buttons/CTAs

**Login Page:**
- Logo/brand mark
- Login form (email, password)
- "Forgot password" link
- Signup link

---

## 5. Layout Heuristics

**Grid System:**
- Desktop: 12-column grid, 1440px max width
- Tablet: 8-column grid, 768px–1024px
- Mobile: 4-column grid, 320px–767px

**Spacing:**
- Section spacing: 64px desktop, 32px mobile
- Component spacing: 24px desktop, 16px mobile
- Content padding: 16px mobile, 24px desktop

**Typography Hierarchy:**
- H1: Hero/Page titles
- H2: Section headers
- H3: Subsection headers
- Body: Content text

---

## 6. Mobile/Desktop Breakpoints

| Breakpoint | Width | Device Type | Notes |
|------------|-------|-------------|-------|
| Mobile | 320px–767px | Phones | Single column, stacked layout |
| Tablet | 768px–1024px | Tablets | 2-column layout, condensed nav |
| Desktop | 1025px+ | Desktop | Full layout, sidebar nav |

**Responsive Considerations:**
- ☐ Navigation collapses to hamburger on mobile
- ☐ Tables become cards/stacked on mobile
- ☐ Images scale proportionally
- ☐ Touch targets ≥ 44px on mobile

**Responsive Pitfalls Checklist:**
- ☐ Tables → Cards: Data tables convert to card layout on mobile
- ☐ Overflow rules: Horizontal scroll handled or content wrapped
- ☐ Long i18n strings: Text expansion (e.g., German 30% longer) accommodated
- ☐ Fixed widths: No fixed pixel widths (use relative units)
- ☐ Text truncation: Long text truncated with ellipsis or tooltip
- ☐ Modal size: Modals fit mobile viewport (max-width constraints)

---

## 7. Annotation Checklist

**Required Annotations:**
- ☐ Interactive elements labeled (buttons, links)
- ☐ Form field labels and validation states
- ☐ Loading states indicated
- ☐ Error states shown
- ☐ Empty states represented
- ☐ Data placeholders labeled ("User Name", "Email")
- ☐ Component relationships noted
- ☐ User flow arrows between frames

**Annotation Template:**
```
Component: [Component Name]
Type: [Button/Link/Form/etc.]
State: [Default/Hover/Active/Disabled]
Action: [What happens when clicked]
Data: [Sample data to display]
Notes: [Additional context]
```

---

## 8. File Map & Artifacts

- `/wireframes/[page]-desktop.png` (new) → must exist
- `/wireframes/[page]-mobile.png` (new) → must exist
- `/docs/wireframe-annotations.md` (new) → annotation documentation

**Artifacts required:**
- List of frames to produce → saved at `output/wireframe-list.md`
- Annotation template (markdown block) → saved at `output/annotation-template.md`

---

## 9. AI Agent Actions & Guardrails

**Actions:** generate wireframe list by page; define key components per frame; create layout heuristics; draft annotation checklist and template.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

