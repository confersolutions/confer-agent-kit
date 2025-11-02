# Claude Code Integration Guide

**Purpose:** Guide to using Confer Agent Kit with Claude Code for everyday tasks (file analysis, MD updates, report generation). Leverages Claude Code's native Commands, Agents, and Skills features.

---

## Overview

Claude Code has three native features that unlock powerful workflows:

1. **Commands** (`.claude/commands/`) — Reusable workflows you run with `/command-name`
2. **Agents** (`.claude/agents/`) — Specialized reusable specialists
3. **Skills** (`.claude/skills/`) — Proactive knowledge that Claude Code uses automatically

---

## Directory Structure

When using Claude Code, create these directories in your project root:

```
.claude/
├── commands/              # Commands you run with /command-name
│   └── analyze-files.md
├── agents/                 # Reusable specialized agents
│   └── file-analyzer.md
├── skills/                 # Proactive knowledge modules
│   └── file-analysis/
│       └── SKILL.md
└── memory/                 # Cross-session continuity (network drives, file locations)
    └── locations.md
```

**Note:** `.claude/` is typically gitignored. These are your personal Claude Code configurations.

---

## 1. Commands

**What:** Reusable workflows you run with `/command-name` in Claude Code chat.

**Location:** `.claude/commands/[command-name].md`

**Use when:** You have a repetitive workflow you want to run consistently.

**Example:** `/analyze-files ~/Desktop` analyzes files on your desktop.

**Templates:**
- `templates/claude-code/commands/command_template.md` — Base template
- `templates/claude-code/commands/analyze_files.md` — Example: analyze files
- `templates/claude-code/commands/update_md.md` — Example: update MD file

---

## 2. Agents

**What:** Specialized reusable agents with front matter metadata.

**Location:** `.claude/agents/[agent-name].md`

**Use when:** You need a specialist that can be invoked by commands or Claude Code.

**Example:** Create a `file-analyzer` agent that commands delegate to.

**Templates:**
- `templates/claude-code/agents/agent_template.md` — Base template
- `templates/claude-code/agents/file_analyzer.md` — Example: file analysis agent
- `templates/claude-code/agents/report_generator.md` — Example: report generator

**Delegation pattern:** Commands can invoke agents: "Use the **file-analyzer** agent to..."

---

## 3. Skills

**What:** Discoverable knowledge modules Claude Code uses proactively.

**Location:** `.claude/skills/[skill-name]/SKILL.md`

**Use when:** You want Claude Code to automatically use certain knowledge when relevant.

**Example:** When analyzing files, Claude Code uses your file analysis standards.

**Templates:**
- `templates/claude-code/skills/skill_template.md` — Base template
- `templates/claude-code/skills/file_analysis_standards.md` — Example skill

**Key:** Write descriptive `description` in front matter—this triggers Claude Code.

---

## 4. Permanent Memory

**What:** Cross-session continuity for locations, preferences, state.

**Location:** `.claude/memory/locations.md` (and other memory files)

**Use for:** Network drives, file locations, last-used paths, tax document locations, preferences.

**Why:** Claude Code works across devices/sessions. Memory helps it resume context.

**Template:** `templates/claude-code/memory/locations_template.md`

**Example entries:**
- Network drives: `\\server\shared\docs`
- Tax documents: `~/Documents/Taxes/2024/`
- Last analyzed: `~/Desktop/projects/`
- Preferred output: `~/Documents/reports/`

---

## Quick Start

1. **Create `.claude/` structure:**
   ```bash
   mkdir -p .claude/{commands,agents,skills,memory}
   ```

2. **Copy templates:**
   - Copy command template → `.claude/commands/my-command.md`
   - Copy agent template → `.claude/agents/my-agent.md`
   - Copy skill template → `.claude/skills/my-skill/SKILL.md`

3. **Set up memory:**
   - Copy `locations_template.md` → `.claude/memory/locations.md`
   - Fill in your network drives, file locations, preferences

4. **Use in Claude Code:**
   - Run commands: `/my-command`
   - Agents are invoked automatically or by name
   - Skills are used proactively when relevant

---

## Best Practices

**Commands:**
- Keep focused (one workflow per command)
- Use phases for multi-step work
- Delegate to agents when appropriate

**Agents:**
- Name clearly (e.g., `file-analyzer`, not `agent1`)
- Write clear descriptions in front matter
- Specify tools needed (Read, Bash, Grep, etc.)

**Skills:**
- Write descriptive `description` field (triggers Claude Code)
- Link to full standards files when relevant
- Add "When to use this skill" section

**Memory:**
- Update regularly as locations change
- Use clear, consistent naming
- Reference memory in commands/agents when needed

---

## Integration with Confer Agent Kit

**Standards:** Skills can wrap your `standards/` files for proactive use.

**Templates:** Commands/agents can reference task templates from `templates/02-dev/`.

**Profile:** Reference `./confer-agent.profile.yml` for project constants.

---

## Examples

**Everyday task:** Analyze files on desktop and update report

1. Create command: `.claude/commands/analyze-desktop.md`
2. Command delegates to agent: `.claude/agents/file-analyzer.md`
3. Agent uses skill: `.claude/skills/file-analysis/SKILL.md`
4. Memory tracks: `.claude/memory/locations.md` (last analyzed path)

Run: `/analyze-desktop` in Claude Code.

---

**Related:**
- [Command Template](commands/command_template.md)
- [Agent Template](agents/agent_template.md)
- [Skill Template](skills/skill_template.md)
- [Memory Template](memory/locations_template.md)

