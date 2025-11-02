# Backend Coding Standards

**Purpose:** Optional guidance for API patterns, DTOs, validation, error mapping, and idempotency. Use these checklists as needed.

**Reference:** Always reference `./confer-agent.profile.yml` for backend framework, DB, auth system. Never hard-code infrastructure values.

---

## API Patterns

### Checklist
- ☐ Use RESTful conventions (GET, POST, PUT, PATCH, DELETE)
- ☐ Version APIs when breaking changes (e.g., `/api/v1/users`)
- ☐ Return consistent response formats
- ☐ Use HTTP status codes correctly (200, 201, 400, 404, 500)
- ☐ Include request/response examples in API docs

### Examples
```typescript
// Good: RESTful endpoint
GET /api/v1/users/:id       → 200 OK with user object
POST /api/v1/users          → 201 Created with user object
PUT /api/v1/users/:id       → 200 OK with updated user
DELETE /api/v1/users/:id    → 204 No Content

// Good: Consistent response format
{
  "success": true,
  "data": { ... },
  "error": null
}
```

---

## DTOs (Data Transfer Objects)

### Checklist
- ☐ Define DTOs for API request/response bodies
- ☐ Use validation libraries (Zod, Joi, Pydantic)
- ☐ Separate DTOs from database models
- ☐ Document DTO fields with types and constraints
- ☐ Transform database models to DTOs before sending

### Examples
```typescript
// Good: DTO with validation
import { z } from 'zod';

const CreateUserDTO = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional()
});

type CreateUserDTO = z.infer<typeof CreateUserDTO>;

// Usage
const validated = CreateUserDTO.parse(request.body);
```

---

## Validation

### Checklist
- ☐ Validate all inputs (query params, body, headers)
- ☐ Use schema-based validation (Zod, Joi, Pydantic)
- ☐ Return 400 Bad Request for validation errors
- ☐ Provide clear error messages for validation failures
- ☐ Sanitize inputs to prevent injection attacks

### Examples
```typescript
// Good: Validation with clear errors
try {
  const data = CreateUserDTO.parse(req.body);
  // Process data
} catch (error) {
  if (error instanceof z.ZodError) {
    return res.status(400).json({
      success: false,
      error: 'Validation failed',
      details: error.errors
    });
  }
}

// Bad: No validation
const user = await createUser(req.body);  // Trusts input
```

---

## Error Mapping

### Checklist
- ☐ Map exceptions to HTTP status codes consistently
- ☐ Never expose internal errors to clients
- ☐ Log full error details server-side
- ☐ Return user-friendly error messages
- ☐ Include error codes for client-side handling

### Examples
```typescript
// Good: Error mapping
try {
  const user = await getUserById(id);
} catch (error) {
  if (error instanceof NotFoundError) {
    return res.status(404).json({
      success: false,
      error: 'User not found',
      code: 'USER_NOT_FOUND'
    });
  }
  logger.error('Unexpected error', { error, id });
  return res.status(500).json({
    success: false,
    error: 'Internal server error',
    code: 'INTERNAL_ERROR'
  });
}

// Bad: Exposing internal errors
return res.status(500).json({ error: err.stack });  // Exposes stack trace
```

---

## Idempotency

### Checklist
- ☐ Make GET requests idempotent (safe to retry)
- ☐ Use idempotency keys for POST/PUT requests
- ☐ Check idempotency key before processing
- ☐ Return same response for duplicate requests
- ☐ Store idempotency results temporarily (Redis, DB)

### Examples
```typescript
// Good: Idempotent POST with key
POST /api/v1/users
Headers: { 'Idempotency-Key': 'abc123' }

// Server checks key
const existing = await getIdempotencyResult('abc123');
if (existing) {
  return res.status(200).json(existing);  // Return cached result
}

// Process and cache result
const user = await createUser(data);
await cacheIdempotencyResult('abc123', user);
return res.status(201).json(user);
```

---

## Data Access Patterns

**Reference:** Follow data access pattern rules:
- Mutations (create/update/delete) → `src/lib/actions/` or equivalent
- Queries (read) → `src/lib/queries/` or equivalent
- API Routes → `src/app/api/` or equivalent

**Never:** Put mutations directly in route handlers or API endpoints.

---

## Profile Usage

**Reference:** `./confer-agent.profile.yml` for:
- Backend framework: `{{FRAMEWORKS}}`
- Database: `{{DB}}`
- Auth system: `{{AUTH_SYSTEM}}`
- Environment: `{{ENV}}`
- HTTP port: `{{HTTP_PORT}}`

**Never:** Hard-code framework versions, ports, or database names.

