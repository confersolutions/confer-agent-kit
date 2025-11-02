---
task_id: "uuid-here"
created_by: "yatin.karnik"
created_at: "{{AUTO:DATE:America/Chicago}}"      # resolve to YYYY-MM-DD
updated_at: "{{AUTO:DATETIME_ISO:America/Chicago}}"  # resolve to ISO8601 with offset
status: "draft"        # draft | in_progress | review | done
priority: "high"       # critical | high | normal | low
type: "testing"        # feature | enhancement | bugfix | research | refactor | testing
labels: ["ai","testing"]
version: "1.0.0"
project_profile:       # optional - standardize project constants
  env: "{{ENV}}"           # dev | staging | prod
  http_port: "{{HTTP_PORT}}"     # do NOT set numeric default
  frameworks: ["{{FRAMEWORKS}}"]
  db: "{{DB}}"
  auth: "{{AUTH_SYSTEM}}"
  infra: "{{INFRA}}"
---

# Testing Checklist Template

**Purpose:** Lightweight test plan per task. Use this to define what tests are needed, how to verify functionality, and document test results. Produces concrete artifacts under `refs/`.

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
- Task being tested: `tasks/NNN_feature_name.md`
- API docs: `refs/api-spec.md`
- Test examples: `refs/test-examples.md`

**Standards reference:**
- Frontend testing: `standards/frontend.md`
- Backend testing: `standards/backend.md`
- Global conventions: `standards/global.md`

---

## 3. Test Scope & Strategy

**Feature/Change Being Tested:**
- Brief description of what needs testing (1-2 sentences)

**Test Types Needed:**
- ☐ Unit tests (functions, components, utilities)
- ☐ Integration tests (API endpoints, database queries)
- ☐ E2E tests (user flows, critical paths)
- ☐ Manual QA (edge cases, visual verification)

**Priority Areas:**
- Critical paths (must work)
- Edge cases (error handling, null values)
- Performance (if applicable)

---

## 4. Test Plan

### Unit Tests

**Functions/Components to Test:**
- [Function/component name]: [what to verify]
  - Input: [test input]
  - Expected output: [expected result]
  - Edge cases: [null, empty, invalid inputs]

**Example:**
```typescript
// Test: validateEmail function
test('validates email correctly', () => {
  expect(validateEmail('user@example.com')).toBe(true);
  expect(validateEmail('invalid')).toBe(false);
});
```

**Test Files:**
- `/src/lib/utils/validation.test.ts` (new/update)
- `/src/components/Button.test.tsx` (new/update)

**Artifacts:**
- Test results: `refs/test-results/unit-YYYYMMDD.json`

### Integration Tests

**Endpoints/Flows to Test:**
- [Endpoint/flow name]: [what to verify]
  - Request: [method, path, body]
  - Expected response: [status, body]
  - Database state: [what should change]

**Example:**
```typescript
// Test: POST /api/users
test('creates user successfully', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({ email: 'test@example.com', name: 'Test User' });
  
  expect(response.status).toBe(201);
  expect(response.body.data.email).toBe('test@example.com');
});
```

**Test Files:**
- `/tests/api/users.test.ts` (new/update)
- `/tests/integration/auth-flow.test.ts` (new/update)

**Artifacts:**
- Test results: `refs/test-results/integration-YYYYMMDD.json`
- Test logs: `refs/test-results/integration-logs-YYYYMMDD.txt`

### E2E Tests

**User Flows to Test:**
- [Flow name]: [user scenario]
  - Steps: 1) ... 2) ... 3) ...
  - Expected result: [what should happen]
  - Screenshots: [when to capture]

**Example:**
```typescript
// Test: User registration flow
test('user can register and login', async ({ page }) => {
  await page.goto('/register');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
  await page.screenshot({ path: 'refs/proof/registration-success.png' });
});
```

**Test Files:**
- `/tests/e2e/registration-flow.spec.ts` (new/update)
- `/tests/e2e/payment-flow.spec.ts` (new/update)

**Artifacts:**
- Screenshots: `refs/proof/e2e-YYYYMMDD/*.png`
- Test results: `refs/test-results/e2e-YYYYMMDD.json`
- Video recordings: `refs/proof/e2e-videos/` (if enabled)

### Manual QA Checklist

**Scenarios:**
- ☐ Happy path: [steps and expected result]
- ☐ Error handling: [error case and expected behavior]
- ☐ Edge cases: [edge case and expected behavior]
- ☐ Accessibility: [keyboard nav, screen reader, contrast]
- ☐ Performance: [load time, response time, if applicable]

**Test Environment:**
- URL: `http://localhost:{{HTTP_PORT}}` (from profile)
- Credentials: (use secrets, not in template)
- Browser: Chrome, Firefox, Safari (list applicable)

**Artifacts:**
- Screenshots: `refs/proof/manual-qa-YYYYMMDD/*.png`
- Notes: `refs/proof/manual-qa-notes-YYYYMMDD.md`

---

## 5. Test Execution & Results

**Test Results:**
- ☐ Unit tests: [pass/fail count]
- ☐ Integration tests: [pass/fail count]
- ☐ E2E tests: [pass/fail count]
- ☐ Manual QA: [scenarios completed]

**Failures (if any):**
- [Test name]: [failure reason, link to artifact]

**Artifacts Produced:**
- `refs/test-results/unit-YYYYMMDD.json`
- `refs/test-results/integration-YYYYMMDD.json`
- `refs/test-results/e2e-YYYYMMDD.json`
- `refs/proof/manual-qa-YYYYMMDD/*.png` (screenshots)

**Coverage:**
- Unit test coverage: [X%] (if measured)
- Integration test coverage: [Y%] (if measured)

---

## 6. AI Agent Actions & Guardrails

**Actions:**
- Review test requirements in task being tested
- Create/update test files based on Test Plan
- Run tests and capture results
- Document failures and fixes
- Generate test artifacts under `refs/`
- Update test results checkboxes

**Guardrails:**
- Resolve all {{TOKEN}} placeholders at instantiation time; leave none unresolved.
- Set `created_at` = {{AUTO:DATE:America/Chicago}}, `updated_at` = {{AUTO:DATETIME_ISO:America/Chicago}}.
- Replace only in YAML/TODO fields; never inject {{TOKEN}} into runtime code.
- Never hard-code ports, frameworks, or environment values; use `{{HTTP_PORT}}`, `{{FRAMEWORKS}}`, `{{ENV}}` from profile.
- Store test artifacts under `refs/test-results/` or `refs/proof/`.
- Follow testing standards in `standards/frontend.md`, `standards/backend.md`.
- Use project profile (`./confer-agent.profile.yml`) for test environment values.

---

## Links

**Related:** [task_template_quick.md](task_template_quick.md), [task_template_full.md](task_template_full.md), [verification_workflow.md](verification_workflow.md)

**Standards:** [standards/frontend.md](../../standards/frontend.md), [standards/backend.md](../../standards/backend.md), [standards/global.md](../../standards/global.md)

