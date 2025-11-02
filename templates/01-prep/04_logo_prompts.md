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

# Logo Prompt Pack

**Purpose:** Generate high-quality, style-diverse logo design prompts with placeholders for brand identity, icon metaphors, geometric constraints, and iteration guidance.

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

- Brand identity: `output/brand-identity.md`
- Logo inspiration: `output/logo-inspiration.md`
- Competitor logos: `output/competitor-logos.md`

---

## 3. Brand Foundation

**Brand Name:** [app name]

**Brand Values:** [3-5 core values]

**Target Audience:** [primary users]

**Icon Metaphor:** [key visual metaphor or concept]

**Design Principles:** Modern, minimal, [other descriptors]

---

## 4. Logo Prompt Templates

**Style 1: Minimal Wordmark**
"Design a clean, modern wordmark logo for [brand name]. Use [font style] typography with subtle custom letterforms. Color: [primary color]. Minimalist approach with negative space emphasis. No icons or symbols."

**Style 2: Icon + Wordmark**
"Create a logo combining a geometric icon symbolizing [metaphor] with a wordmark for [brand name]. Icon should be simple, scalable, and work at small sizes. Style: [modern/classic/playful]. Color palette: [colors]."

**Style 3: Abstract Symbol**
"Design an abstract logo mark for [brand name] representing [concept]. Geometric or organic shapes, highly recognizable at small sizes. Works in monochrome. Style: [descriptor]."

**Style 4: Lettermark**
"Create a letterform logo using [initial/letters]. Custom typography that's distinctive but readable. Incorporate subtle reference to [brand concept]. Color: [color]. Minimal detail."

**Style 5: Emblem/Badge**
"Design an emblem-style logo for [brand name] with [symbol/element] inside a badge shape. Classic yet modern. Suitable for stamps, seals, premium branding. Colors: [palette]."

**Style 6: Pictorial Mark**
"Design a pictorial logo representing [object/concept] in a simplified, iconic style. Should work as standalone mark and with text. Scalable, recognizable silhouette. Style: [descriptor]."

**Style 7: Combination Mark**
"Create a combination logo with [icon style] icon above [wordmark/below]. Balanced composition, works horizontally and vertically stacked. Colors: [palette]. Professional and approachable."

**Style 8: Mascot/Character**
"Design a friendly mascot logo character for [brand name] representing [personality/trait]. Stylized, memorable, works in color and B&W. Appropriate for [target audience]. Style: [descriptor]."

**Style 9: Monogram**
"Design a monogram logo using [letters/initials]. Elegant interlocking letters with subtle [detail/pattern]. Works as standalone mark. Colors: [palette]. Timeless and sophisticated."

**Style 10: Textural/Handcrafted**
"Create a handcrafted logo for [brand name] with organic, textural feel. Natural imperfections, warm aesthetic. Suitable for [industry/audience]. Color: [palette]. Authentic and human."

**Style 11: Tech/Geometric**
"Design a tech-forward logo for [brand name] using geometric shapes, clean lines, precision. Represents [concept] through abstract forms. Color: [tech palette]. Modern and futuristic."

**Style 12: Vintage/Retro**
"Create a vintage-inspired logo for [brand name] with [decade/style] aesthetic. Nostalgic yet contemporary. Works in [colors]. Classic typography with period-appropriate details."

---

## 5. Selection Criteria

**Functional Requirements:**
- ☐ Scalable (works at 16px to billboard size)
- ☐ Works in monochrome/B&W
- ☐ Recognizable when rotated or mirrored
- ☐ Versatile (horizontal and vertical layouts)

**Brand Alignment:**
- ☐ Reflects brand values
- ☐ Appropriate for target audience
- ☐ Differentiates from competitors
- ☐ Memorable and distinctive

**Technical:**
- ☐ Vector format (SVG preferred)
- ☐ Clear edges, no blur/pixels
- ☐ Minimal colors for cost efficiency

---

## 6. Iteration Guidance

**Round 1:** Generate 10–12 diverse concepts from prompts above
**Round 2:** Refine top 3–5 based on selection criteria
**Round 3:** Final polish and color variations

**Refinement Prompts:**
- "Simplify the logo, remove unnecessary details"
- "Make it more [adjective] while maintaining core concept"
- "Create 3 color variations: light, dark, and full color"
- "Generate icon-only and wordmark-only versions"

---

## 6a. Deliverables Spec

**Required Formats:**

| Format | Requirement | Use Case |
|--------|-------------|----------|
| SVG | Primary format, vector | Scalable, web usage |
| PNG | High-res (1024x1024) | Print, fallback |
| Monochrome | B&W version required | Single-color printing |
| Min Size | Must work at 16px | Favicon, small spaces |
| Clear Space | 1x logo height around | Brand guidelines |

**Deliverables Checklist:**
- ☐ SVG (vector, primary format)
- ☐ Monochrome version (B&W)
- ☐ Minimum size: 16px (verified)
- ☐ Clear space guidelines (1x logo height)
- ☐ Horizontal and vertical layouts

---

## 7. File Map & Artifacts

- `/docs/logo-prompts.md` (new) → must exist
- `/design-system/logo-variants/` (new) → logo asset folder

**Artifacts required:**
- Prompt list → saved at `output/logo-prompts.md`
- Selection rubric → saved at `output/logo-rubric.md`

---

## 8. AI Agent Actions & Guardrails

**Actions:** generate style-diverse logo prompts; create selection criteria rubric; draft iteration guidance; compile prompt variations.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

---

## Links

**Related:** [01_master_idea.md](01_master_idea.md), [09_build_order.md](09_build_order.md), [08_system_design.md](08_system_design.md)

