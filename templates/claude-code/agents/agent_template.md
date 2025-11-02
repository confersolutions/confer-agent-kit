---
name: [agent-name]
description: [Clear, descriptive description of when Claude Code should use this agent proactively. Include multiple examples: "Use when [scenario 1], [scenario 2], [scenario 3]."]
tools: [Read, Write, Bash, Grep, WebFetch, etc.]
color: [blue|red|green|purple|yellow]
model: inherit
---

# [Agent Name]

You are a [specialist role]. Your role is to [primary responsibility].

---

## Core Responsibilities

1. **[Responsibility 1]**: [What this agent does]
2. **[Responsibility 2]**: [What this agent does]
3. **[Responsibility 3]**: [What this agent does]

---

## Workflow

### Step 1: [Step Name]

[Detailed instructions for this step]

**Actions:**
- [Action 1]
- [Action 2]
- [Action 3]

### Step 2: [Step Name]

[Detailed instructions for this step]

**Actions:**
- [Action 1]
- [Action 2]

### Step 3: [Step Name]

[Detailed instructions for this step]

**Actions:**
- [Action 1]
- [Action 2]

---

## Guidelines

- [Guideline 1 for consistent behavior]
- [Guideline 2 for quality output]
- [Guideline 3 for error handling]
- [Guideline 4 for edge cases]

---

## Memory & Context

**Check memory files when needed:**
- `.claude/memory/locations.md` for [network drives / file paths / preferences]
- `.claude/memory/[agent-name]_state.md` for [agent-specific state]

**Update memory after work:**
- Update `.claude/memory/locations.md` if paths or locations changed
- Save state in `.claude/memory/[agent-name]_state.md` if needed for next session

---

## Output Format

**Deliverables:**
- [Output 1]: [Format and location]
- [Output 2]: [Format and location]

**Format requirements:**
- [Format requirement 1]
- [Format requirement 2]

---

## Related

- **Used by commands:** `.claude/commands/[command-names].md`
- **Uses skills:** `.claude/skills/[skill-names]/SKILL.md`
- **Standards:** `standards/[relevant-standard].md` (if applicable)

