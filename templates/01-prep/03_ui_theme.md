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

# Design System Seed

**Purpose:** Define brand tokens, color palette with semantic roles, typography scale, spacing system, and accessibility standards for the design system foundation.

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

- Brand guidelines: `refs/brand-guidelines.md`
- Design inspiration: `refs/design-inspiration.md`
- Accessibility standards: `refs/a11y-standards.md`

---

## 3. Brand Tokens

**Typography Scale:**

| Scale | Font Size | Line Height | Usage |
|-------|-----------|-------------|-------|
| xs    | [size]px  | [height]px  | Captions, labels |
| sm    | [size]px  | [height]px  | Body small |
| base  | [size]px  | [height]px  | Body text |
| lg    | [size]px  | [height]px  | Subheadings |
| xl    | [size]px  | [height]px  | Headings |
| 2xl   | [size]px  | [height]px  | Hero text |

**Font Family:** [primary font], [fallback stack]

**Spacing Scale:**

| Scale | Value | Usage |
|-------|-------|-------|
| xs    | [4px] | Tight spacing |
| sm    | [8px] | Default spacing |
| md    | [16px] | Component padding |
| lg    | [24px] | Section spacing |
| xl    | [32px] | Page spacing |

**Border Radius:**

| Scale | Value | Usage |
|-------|-------|-------|
| sm    | [4px] | Buttons, inputs |
| md    | [8px] | Cards |
| lg    | [12px] | Modals |
| full  | [9999px] | Pills, badges |

---

## 4. Color Palette

**Primary Colors:**

| Role | Light Mode | Dark Mode | Usage |
|------|------------|-----------|-------|
| Primary | #0000FF | #4A90E2 | Main actions, links |
| Primary Hover | #0000CC | #357ABD | Interactive states |
| Primary Disabled | #CCCCCC | #555555 | Disabled states |

**Semantic Colors:**

| Role | Light Mode | Dark Mode | Usage |
|------|------------|-----------|-------|
| Success | #22C55E | #10B981 | Success messages, confirmations |
| Warning | #F59E0B | #FBBF24 | Warnings, cautions |
| Danger | #EF4444 | #DC2626 | Errors, destructive actions |
| Info | #3B82F6 | #60A5FA | Informational messages |

**Surface Colors:**

| Role | Light Mode | Dark Mode | Usage |
|------|------------|-----------|-------|
| Background | #FFFFFF | #1A1A1A | Page background |
| Surface | #F5F5F5 | #2A2A2A | Card backgrounds |
| Border | #E5E5E5 | #404040 | Borders, dividers |
| Text Primary | #1A1A1A | #FFFFFF | Primary text |
| Text Secondary | #666666 | #CCCCCC | Secondary text |

---

## 5. Light/Dark Mode Mapping

**Mode Toggle:** ☐ System preference  ☐ User preference  ☐ Fixed (light only)

**Transition:** Smooth transition duration: [duration]ms

**Storage:** User preference saved in [localStorage | cookie | DB]

---

## 6. Accessibility Checks

**Contrast Targets:**

| Element Type | WCAG Level | Min Contrast Ratio | Status |
|--------------|------------|-------------------|--------|
| Body text    | AA        | 4.5:1            | ☐ Pass |
| Large text   | AA        | 3:1              | ☐ Pass |
| UI components | AA       | 3:1              | ☐ Pass |
| Body text    | AAA       | 7:1              | ☐ Pass |
| Large text   | AAA       | 4.5:1            | ☐ Pass |

**Other Requirements:**
- ☐ Focus indicators visible (≥ 2px outline)
- ☐ Keyboard navigation fully functional
- ☐ Screen reader labels on interactive elements
- ☐ Color not sole indicator of meaning

---

## 7. Component Primitives

**Base Components:**
- Button (primary, secondary, ghost, danger variants)
- Input (text, email, password, number)
- Select/Dropdown
- Checkbox, Radio
- Card
- Modal/Dialog
- Badge/Tag
- Alert/Toast

**Layout Components:**
- Container
- Grid
- Flex
- Stack

---

## 7a. Design Tokens Export Formats

**Export Targets:**

| Format | Path | Use Case |
|--------|------|----------|
| CSS Variables | `/design-system/tokens.css` | Web CSS usage |
| Tailwind Theme | `/tailwind.config.js` | Tailwind integration |
| tokens.json | `/design-system/tokens.json` | Cross-platform reference |

**CSS Variables Example:**
```css
:root {
  --color-primary: #0000FF;
  --spacing-md: 16px;
  --radius-sm: 4px;
}
```

**Tailwind Theme Example:**
```js
theme: {
  colors: { primary: '#0000FF' },
  spacing: { md: '16px' },
  borderRadius: { sm: '4px' }
}
```

---

## 7b. Motion Scale

| Duration | Value | Usage |
|----------|-------|-------|
| Fast | 150ms | Micro-interactions, hover states |
| Normal | 250ms | Standard transitions |
| Slow | 350ms | Page transitions, modal animations |
| Very Slow | 500ms | Complex animations |

| Easing | Value | Usage |
|--------|-------|-------|
| Ease In | `cubic-bezier(0.4, 0, 1, 1)` | Exit animations |
| Ease Out | `cubic-bezier(0, 0, 0.2, 1)` | Entrance animations |
| Ease In Out | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard transitions |

---

## 8. File Map & Artifacts

- `/design-system/tokens.json` (new) → must exist
- `/design-system/colors.ts` (new) → color definitions
- `/design-system/spacing.ts` (new) → spacing scale

**Artifacts required:**
- Token table → saved at `refs/design-tokens.md`
- Contrast checklist → saved at `refs/contrast-checklist.md`

---

## 9. AI Agent Actions & Guardrails

**Actions:** generate token scale tables; define color palette with semantic roles; create accessibility checklist; draft component primitive list.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

