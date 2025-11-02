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

# Vercel (Next.js) Frontend Runbook

**Purpose:** Operational guide for deploying Next.js frontend on Vercel, including build settings, environment separation, env var mapping, Edge/Serverless limits, domain configuration, ISR cache strategy, and Coolify backend integration.

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

**Reference:** See [00_infra_conventions.md](00_infra_conventions.md) for ports, DNS, and routing conventions.

---

## 2. References & Inputs

External snippets/links cached in `output/` (gitignored):

- Project profile: `./confer-agent.profile.yml`

- Vercel env template: `output/vercel_env_template.env`
- Vercel routes examples: `output/vercel_routes_examples.md`
- Next.js config: `output/nextjs_config.md`

---

## 3. Next.js Build Settings

**Build Configuration:**

| Setting | Value | Purpose |
|---------|-------|---------|
| Framework Preset | Next.js | Auto-detected |
| Build Command | `npm run build` | Default (override if needed) |
| Output Directory | `.next` | Next.js default |
| Install Command | `npm install` | Default (override if needed) |
| Node.js Version | `20.x` | Latest LTS |

**Build Settings Checklist:**
- ☐ Framework preset set to Next.js
- ☐ Build command configured (if custom)
- ☐ Root directory set (if monorepo)
- ☐ Node.js version specified (if needed)

---

## 4. Environment Separation (Preview/Prod)

**Environment Types:**

| Environment | Trigger | Domain Pattern | Use Case |
|-------------|---------|----------------|----------|
| Production | `main` branch | `yourdomain.com` | Live production |
| Preview | `feature/*` branches | `pr-[number]-[repo].vercel.app` | PR previews |
| Development | Local dev | `localhost:3000` | Local development |

**Environment Variable Priority:**
1. Production env vars (highest priority)
2. Preview env vars (for all preview deployments)
3. Development env vars (for local dev only)

**Env Var Configuration:**
- **Production:** Set in Vercel UI → Project Settings → Environment Variables
- **Preview:** Same UI, but apply to "Preview" environment
- **Development:** Use local `.env.local` file

---

## 5. Environment Variable Mapping from Coolify

**Coolify → Vercel Integration:**

| Coolify Service | Vercel Env Var | Purpose |
|-----------------|----------------|----------|
| `api.yourdomain.com:{{HTTP_PORT}}` | `NEXT_PUBLIC_API_URL` | Backend API URL (port defined in project profile) |
| Postgres (internal) | `DATABASE_URL` | Database connection |
| n8n webhooks | `N8N_WEBHOOK_URL` | Automation webhooks |
| Flowise API | `FLOWISE_API_URL` | AI agent endpoints |

**Required Env Vars (Example):**
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
N8N_WEBHOOK_URL=https://n8n.yourdomain.com/webhook/[id]
FLOWISE_API_URL=https://flowise.yourdomain.com/api/v1
```

**Coolify → Vercel Setup:**
1. Expose backend API on port {{HTTP_PORT}} (defined in project profile) via Traefik
2. Set `NEXT_PUBLIC_API_URL` in Vercel to `https://api.yourdomain.com`
3. Configure CORS on Coolify backend (allow Vercel domains)
4. Test API calls from Vercel preview deployments

**CORS Configuration (Backend):**
```python
# FastAPI example
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 6. Edge & Serverless Limits

**Edge Runtime Limits:**

| Limit | Value | Impact |
|-------|-------|--------|
| Function timeout | 30s (Hobby), 60s (Pro) | Long-running tasks |
| Memory | 128MB (Hobby), 1024MB (Pro) | Memory-intensive operations |
| Request size | 4.5MB | Large payloads |
| Response size | 4.5MB | Large responses |

**Serverless Function Limits:**

| Limit | Value | Impact |
|-------|-------|--------|
| Function timeout | 10s (Hobby), 60s (Pro) | Long-running tasks |
| Memory | 1024MB | Memory-intensive operations |
| Request size | 4.5MB | Large payloads |
| Response size | 4.5MB | Large responses |

**Best Practices:**
- Use Edge Runtime for API routes (faster, lower latency)
- Use Serverless Functions for CPU-intensive tasks
- Offload heavy processing to Coolify backend
- Use Vercel Edge Config for global config

---

## 7. Domain & Redirects

**Domain Configuration:**

| Domain Type | Setup | Use Case |
|-------------|-------|----------|
| Custom domain | Add in Vercel UI → Domains | Production |
| Vercel domain | Auto-generated | Preview deployments |
| Subdomain | Add as alias | API endpoints (if needed) |

**Redirect Configuration (vercel.json):**
```json
{
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.yourdomain.com/:path*"
    }
  ]
}
```

**Domain Setup Checklist:**
- ☐ Add custom domain in Vercel UI
- ☐ Configure DNS records (A/CNAME)
- ☐ Wait for DNS propagation (up to 24h)
- ☐ Verify SSL certificate (auto-generated)
- ☐ Test domain redirects/rewrites

---

## 8. ISR Cache Strategy

**Incremental Static Regeneration (ISR):**

| Strategy | Revalidate | Use Case |
|----------|------------|----------|
| Static | N/A | Never-changing content |
| ISR | `revalidate: 60` | Content updates every 60s |
| ISR | `revalidate: 3600` | Content updates hourly |
| Dynamic | `revalidate: 0` | Always fetch fresh |

**ISR Example (Next.js):**
```typescript
// pages/blog/[slug].tsx
export async function getStaticProps({ params }) {
  return {
    props: {
      post: await fetchPost(params.slug),
    },
    revalidate: 60, // Revalidate every 60 seconds
  };
}
```

**Cache Strategy Guidelines:**
- **Static pages:** Use ISR with long revalidate (3600s+)
- **Dynamic content:** Use ISR with short revalidate (60s)
- **Real-time data:** Use SSR or client-side fetching
- **API routes:** Use Edge Runtime for caching

---

## 9. Preview Deployment Patterns

**PR Preview Workflow:**

| Step | Action | Result |
|------|--------|--------|
| 1. Open PR | Push to `feature/*` branch | Auto-deploy preview |
| 2. Vercel detects | Webhook from GitHub | Build starts |
| 3. Deploy preview | Deploy to `pr-[number]-[repo].vercel.app` | Preview URL generated |
| 4. Comment added | Vercel bot comments on PR | Preview link in PR |

**Preview Env Vars:**
- Use Preview environment variables
- Access Coolify backend via `api.yourdomain.com` (shared)
- Use feature flags for preview-only features

**Preview Testing Checklist:**
- ☐ Preview URL accessible
- ☐ API calls work (CORS configured)
- ☐ Environment variables loaded correctly
- ☐ Build logs show no errors
- ☐ Test critical user flows

---

## 10. File Map & Artifacts

- `/docs/vercel-runbook.md` (new) → must exist
- `/vercel.json` (update) → redirects/rewrites config
- `/next.config.js` (update) → ISR settings

**Artifacts required:**
- Vercel env template → saved at `output/vercel_env_template.env`
- Vercel routes examples → saved at `output/vercel_routes_examples.md`

---

## 11. AI Agent Actions & Guardrails

**Actions:** generate Vercel build configurations; create env var mapping from Coolify; draft ISR cache strategy; document preview deployment patterns.

**Guardrails:** do not change unrelated files; keep commits scoped; follow existing lint rules.

