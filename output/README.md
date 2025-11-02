# Output Directory

This directory contains artifacts and outputs generated from using Confer Agent Kit templates.

## Structure

Organize outputs by category:
- `output/proof/` - Screenshots, proof-of-concept files
- `output/test-results/` - Test results, test logs
- `output/docs/` - Documentation artifacts
- `output/logs/` - Log files, deployment logs
- `output/exports/` - Data exports, CSV files
- `output/` - Other artifacts (reports, configurations, etc.)

## Gitignore

This directory is **gitignored** by default. All files in `output/` are excluded from version control.

If you need to track specific outputs, add them explicitly:
- Use `!output/specific-file.md` in `.gitignore`
- Or create a separate tracked directory for shared artifacts

## Usage

When using templates:
1. Create artifacts in this directory
2. Reference them in task files: `output/filename.md`
3. Keep organized by type (proof, logs, docs, etc.)

**Note:** Both `output/` and `refs/` directories are gitignored and will never be committed.

**vs. Refs Directory:**
- **`refs/`** = Inputs, reference materials, things to learn from (internet facts, other repos, reference docs)
- **`output/`** = Outputs, generated artifacts, results from templates (screenshots, reports, logs)
