# Refs Directory (Reference Materials)

**Purpose:** Reference materials, inputs, and learning resources for AI agents.

This directory is for **reference inputs**—materials you bring in for AI agents to learn from or reference during work.

## What Goes Here

- **Reference documents** — MD files, documentation, specs
- **Internet facts** — Saved research, facts, information
- **Other repos** — Cloned repos or extracted code for learning
- **Examples** — Reference implementations, patterns, examples
- **Context materials** — Any files you want AI to reference or learn from

## Use Cases

- "Can you learn from this repo in `refs/other-project/` and help me?"
- "Reference the API docs in `refs/api-spec.md`"
- "Use the examples in `refs/examples/` as a guide"
- "Review the architecture in `refs/architecture-diagram.md`"

## vs. Output Directory

- **`refs/`** = Inputs, reference materials, things to learn from
- **`output/`** = Outputs, generated artifacts, results from templates

## Structure

Organize by purpose:
- `refs/docs/` — Documentation references
- `refs/examples/` — Code examples, patterns
- `refs/repos/` — Cloned repositories for learning
- `refs/research/` — Research, facts, information
- `refs/` — Other reference files

## Gitignore

This directory is **gitignored** by default. All files in `refs/` are excluded from version control (except this README.md).

If you need to track specific references, add them explicitly in `.gitignore`:
- Use `!refs/specific-file.md` to track a specific reference

