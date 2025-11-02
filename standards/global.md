# Global Coding Standards

**Purpose:** Optional guidance for naming, logging, errors, documentation, tokens, and project profile usage. These are checklists and examples; use them as needed.

**Reference:** Always reference `./confer-agent.profile.yml` for project constants (ports, frameworks, env). Never hard-code infrastructure values.

---

## Naming Conventions

### Checklist
- ☐ Use descriptive names; avoid abbreviations
- ☐ Follow language conventions (camelCase for JS/TS, snake_case for Python)
- ☐ Prefix booleans with `is`, `has`, `should` (e.g., `isActive`, `hasPermission`)
- ☐ Use singular for classes/modules, plural for collections
- ☐ Prefix private members with underscore if language supports it

### Examples
```typescript
// Good
const userCount = 10;
const isAuthenticated = true;
function getUserById(id: string) { }

// Bad
const uc = 10;
const auth = true;
function get(id: string) { }
```

---

## Logging

### Checklist
- ☐ Use structured logging with context
- ☐ Log levels: DEBUG → INFO → WARN → ERROR
- ☐ Include request IDs or correlation IDs
- ☐ Never log secrets (tokens, passwords, API keys)
- ☐ Use appropriate log level for severity

### Examples
```typescript
// Good
logger.info('User login attempt', { userId, email, ipAddress });
logger.error('Database connection failed', { error: err.message, db: dbName });

// Bad
console.log('User logged in');  // No context
logger.info('Token: abc123');    // Logging secret
```

---

## Error Handling

### Checklist
- ☐ Always catch and handle errors explicitly
- ☐ Provide user-friendly messages for client-facing errors
- ☐ Include stack traces in server logs (not in responses)
- ☐ Use typed error classes when possible
- ☐ Handle edge cases (null, undefined, empty arrays)

### Examples
```typescript
// Good
try {
  const user = await getUserById(id);
  if (!user) throw new NotFoundError(`User ${id} not found`);
  return user;
} catch (error) {
  logger.error('Failed to get user', { id, error });
  throw new InternalServerError('Unable to retrieve user');
}

// Bad
const user = await getUserById(id);  // No error handling
return user.data;                    // May throw on undefined
```

---

## Documentation

### Checklist
- ☐ Document public APIs with JSDoc/TSDoc
- ☐ Include parameter types and return types
- ☐ Add examples for complex functions
- ☐ Document assumptions and constraints
- ☐ Keep README and inline comments up to date

### Examples
```typescript
/**
 * Fetches a user by ID from the database.
 * @param id - User UUID
 * @returns Promise resolving to User object
 * @throws NotFoundError if user doesn't exist
 * @example
 * const user = await getUserById('123e4567-e89b-12d3-a456-426614174000');
 */
async function getUserById(id: string): Promise<User> { }
```

---

## Token Placeholders & Profile Usage

### Checklist
- ☐ Use `{{ENV}}`, `{{HTTP_PORT}}`, `{{FRAMEWORKS}}` from project profile
- ☐ Never hard-code ports, environments, or framework versions
- ☐ Reference `./confer-agent.profile.yml` in Context Capsule
- ☐ Resolve date tokens: `{{AUTO:DATE}}` → `2025-01-15`
- ☐ Resolve datetime tokens: `{{AUTO:DATETIME_ISO}}` → ISO8601 string

### Examples
```yaml
# confer-agent.profile.yml
env: dev
http_port: 3000
frameworks: ["next@14", "fastapi@0.115"]

# Template usage
env: "{{ENV}}"           # → "dev"
http_port: "{{HTTP_PORT}}" # → "3000"
frameworks: ["{{FRAMEWORKS}}"]  # → ["next@14", "fastapi@0.115"]
```

**Guardrail:** Replace `{{TOKEN}}` only in YAML/TODO fields; never inject into runtime code.

---

## Project Profile Reference

**File:** `./confer-agent.profile.yml`

**Usage:**
- Copy values into Context Capsule of task templates
- Reference placeholders like `{{ENV}}`, `{{HTTP_PORT}}`
- Update profile when infrastructure changes (ports, frameworks)

**Never:**
- Hard-code profile values in templates or code
- Commit secrets to profile file
- Modify profile without updating related templates

