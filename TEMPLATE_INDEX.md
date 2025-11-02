# Confer Agent Kit — Template Index

Quick reference for all 29 templates organized by category. Start here to find the right template for your task.

---

## Prep Templates (9 templates: project kickoff → build order)

- [01_master_idea.md](templates/01-prep/01_master_idea.md) – Project Master Plan with vision, metrics, roadmap, and governance
- [02_app_name.md](templates/01-prep/02_app_name.md) – Naming & Positioning with criteria, candidates, and selection rubric
- [03_ui_theme.md](templates/01-prep/03_ui_theme.md) – Design System Seed with tokens, colors, typography, and accessibility
- [04_logo_prompts.md](templates/01-prep/04_logo_prompts.md) – Logo Prompt Pack with style-diverse prompts and selection criteria
- [05_pages_and_functionality.md](templates/01-prep/05_pages_and_functionality.md) – App IA & Feature Map with sitemap, flows, and acceptance criteria
- [06_wireframes.md](templates/01-prep/06_wireframes.md) – Wireframe Planning with component breakdowns and annotation standards
- [07_data_models.md](templates/01-prep/07_data_models.md) – Domain & Schema Outline with entities, relationships, and migration principles
- [08_system_design.md](templates/01-prep/08_system_design.md) – Architecture Overview with services, data flow, caching, and scaling
- [09_build_order.md](templates/01-prep/09_build_order.md) – Phased Build Plan with milestones, dependencies, and release cut-lines

---

## Dev Templates (10 templates: daily coding workflow)

- [commands_reference.md](templates/02-dev/commands_reference.md) – Quick guide on how to invoke templates with AI agents
- [task_template_full.md](templates/02-dev/task_template_full.md) – Full task template (comprehensive)
- [task_template_quick.md](templates/02-dev/task_template_quick.md) – Quick task template (fast tasks)
- [bugfix.md](templates/02-dev/bugfix.md) – Standardized bug reproduction → fix → validation workflow
- [testing_checklist.md](templates/02-dev/testing_checklist.md) – Lightweight test plan per task
- [verification_workflow.md](templates/02-dev/verification_workflow.md) – Post-merge verification steps and rollback checklist
- [diff_review.md](templates/02-dev/diff_review.md)
- [cleanup_ts_js.md](templates/02-dev/cleanup_ts_js.md)
- [git_commit_messages.md](templates/02-dev/git_commit_messages.md)
- [pr_review_checklist.md](templates/02-dev/pr_review_checklist.md)
- [update_workflow.md](templates/02-dev/update_workflow.md)

---

## DB Templates (2 templates)

- [drizzle_down_migration.md](templates/db/drizzle_down_migration.md)
- [drizzle_rollback.md](templates/db/drizzle_rollback.md)

---

## UI Templates (3 templates)

- [improve_ui.md](templates/ui/improve_ui.md)
- [landing_page.md](templates/ui/landing_page.md)
- [diagram_mermaid.md](templates/ui/diagram_mermaid.md)

---

## Infra Templates (10 templates: infrastructure operations)

- [00_infra_conventions.md](templates/06-infra/00_infra_conventions.md) – Canonical conventions for ports, routing, DNS/TLS, secrets, and cross-platform migration
- [coolify_platform.md](templates/06-infra/coolify_platform.md) – Coolify platform runbook with Traefik, volumes, health checks, backups, and rollbacks
- [vercel_frontend.md](templates/06-infra/vercel_frontend.md) – Vercel (Next.js) frontend runbook with build settings, env mapping, ISR, and Coolify integration
- [replit_dev_env.md](templates/06-infra/replit_dev_env.md) – Replit dev workflow with tunnels, secrets, preview URLs, and env sync
- [n8n_ops.md](templates/06-infra/n8n_ops.md) – n8n on Coolify operations with webhooks, credentials, queues, backups, and rollbacks
- [flowise_ops.md](templates/06-infra/flowise_ops.md) – Flowise on Coolify operations with LLM keys, Qdrant/Neo4j connectors, caching, and rate limits
- [qdrant_ops.md](templates/06-infra/qdrant_ops.md) – Qdrant on Coolify operations with collections, snapshots, sizing, and networking
- [neo4j_ops.md](templates/06-infra/neo4j_ops.md) – Neo4j on Coolify operations with APOC, auth, backups, tuning, and connectors
- [setup_oauth_google_github.md](templates/06-infra/setup_oauth_google_github.md)
- [gcp_debugging.md](templates/06-infra/gcp_debugging.md)

---

## Advanced Templates (7 templates: Python + ADK agents + orchestration)

- [python_task_template.md](templates/05-advanced/python_task_template.md)
- [cleanup_python.md](templates/05-advanced/cleanup_python.md)
- [adk_task_template.md](templates/05-advanced/adk_task_template.md)
- [adk_bottleneck_analysis.md](templates/05-advanced/adk_bottleneck_analysis.md)
- [agent_orchestrator.md](templates/05-advanced/agent_orchestrator.md)
- [agent_design_playbook.md](templates/05-advanced/agent_design_playbook.md)
- [task_orchestrator.md](templates/05-advanced/task_orchestrator.md) – Orchestrate arbitrary tasks (seq/parallel) with loop-until-done and optional multi-agent hints

---

## Standards (Optional Guidance)

**Purpose:** Lightweight coding standards organized by domain. Use these checklists and examples as needed; they're optional guidance, not mandates.

- [README.md](standards/README.md) – How to reference standards with AI agents
- [global.md](standards/global.md) – Naming, logging, errors, docs, tokens, profile usage
- [backend.md](standards/backend.md) – API patterns, DTOs, validation, error mapping, idempotency
- [frontend.md](standards/frontend.md) – Component structure, state management, accessibility, testing

**Usage:** Reference standards files when filling templates or implementing features. Always reference `./confer-agent.profile.yml` for project constants (ports, frameworks, env).

---

## Claude Code Templates (For Claude Code Users)

**Purpose:** Templates for creating Claude Code commands, agents, and skills for everyday tasks (file analysis, MD updates, report generation). Fully optional—only for Claude Code users.

### Overview & Setup

- [README.md](templates/claude-code/README.md) – Complete guide to Claude Code integration (commands, agents, skills, memory)

### Commands

**Commands are reusable workflows you run with `/command-name` in Claude Code:**

- [command_template.md](templates/claude-code/commands/command_template.md) – Base template for creating commands
- [analyze_files.md](templates/claude-code/commands/analyze_files.md) – Example: analyze files in directory
- [update_md.md](templates/claude-code/commands/update_md.md) – Example: update markdown file with new content

### Agents

**Agents are specialized reusable specialists that commands can delegate to:**

- [agent_template.md](templates/claude-code/agents/agent_template.md) – Base template for creating agents
- [file_analyzer.md](templates/claude-code/agents/file_analyzer.md) – Example: file analysis specialist
- [report_generator.md](templates/claude-code/agents/report_generator.md) – Example: report generation specialist

### Skills

**Skills are proactive knowledge modules Claude Code uses automatically:**

- [skill_template.md](templates/claude-code/skills/skill_template.md) – Base template for creating skills
- [file_analysis_standards.md](templates/claude-code/skills/file_analysis_standards.md) – Example: file analysis standards skill

### Memory

**Memory provides cross-session continuity for locations, preferences, state:**

- [locations_template.md](templates/claude-code/memory/locations_template.md) – Template for permanent memory (network drives, file locations, tax documents, etc.)

**Usage:** Copy templates to `.claude/commands/`, `.claude/agents/`, `.claude/skills/`, `.claude/memory/` in your project root. See [claude-code/README.md](templates/claude-code/README.md) for setup guide.

---

