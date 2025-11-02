# Analyze Files Command

**Purpose:** Analyze files in a directory, extract metadata, categorize by type, and generate a markdown report.

**Usage:** `/analyze-files [directory-path]`

**Example:** `/analyze-files ~/Desktop` or `/analyze-files /Volumes/NetworkDrive/docs`

---

## Overview

This command scans a directory, analyzes files, extracts metadata (size, type, modification date), categorizes by file type, and generates a structured markdown report with insights.

**Inputs:**
- Directory path: Target directory to analyze (absolute or relative path)
- Memory reference: Check `.claude/memory/locations.md` for network drives or recent paths

**Outputs:**
- Report file: `reports/analysis-[YYYYMMDD].md` (auto-generated filename with date)
- Summary: File count, total size, categories, notable files

---

## Workflow

### Phase 1: Scan Directory

Use the **file-analyzer** agent to:
- List all files in target directory (recursive scan)
- Extract metadata: path, size, modification date, file type
- Handle errors gracefully (permission denied, symlinks, etc.)

**Checklist:**
- ☐ Directory exists and is accessible
- ☐ All files enumerated
- ☐ Metadata extracted for each file

**Memory check:**
- If directory not specified, check `.claude/memory/locations.md` for `last_analyzed_path` or `default_analysis_path`

### Phase 2: Categorize & Analyze

- Group files by type (images, documents, code, etc.)
- Calculate totals per category
- Identify large files (>100MB) or unusual patterns
- Flag important files (recently modified, specific extensions)

**Checklist:**
- ☐ Files categorized by type
- ☐ Totals calculated (count, size per category)
- ☐ Notable files identified
- ☐ Anomalies flagged (if any)

### Phase 3: Generate Report

Use the **report-generator** agent to:
- Format findings as structured markdown
- Create summary table
- Include file listings per category
- Add insights and recommendations

**Output location:**
- Default: `reports/analysis-[YYYYMMDD-HHMMSS].md`
- Or: Update `.claude/memory/locations.md` for custom output path

**Checklist:**
- ☐ Markdown report created
- ☐ Summary table included
- ☐ File listings formatted
- ☐ Insights section added

---

## Memory & Context

**Update memory after completion:**
- Update `.claude/memory/locations.md`:
  - `last_analyzed_path`: [directory path]
  - `last_analysis_date`: [YYYY-MM-DD]
  - `last_analysis_report`: [report file path]

**Reference memory during execution:**
- Network drive paths (if analyzing remote directories)
- Preferred output locations
- File type preferences or filters

---

## Completion

**Success criteria:**
- ☐ Report file exists at output location
- ☐ Summary includes file counts and sizes
- ☐ Categories are clearly organized
- ☐ Notable files are highlighted

**Next steps:**
- Review report: `reports/analysis-[date].md`
- Run `/update-md` if you need to merge findings into another document

---

## Tips

- **Network drives:** Reference `.claude/memory/locations.md` for network drive mappings
- **Large directories:** Command handles large directories but may take time
- **Custom output:** Set `default_report_path` in memory file to change output location
- **Filters:** Can be extended to filter by file type, size, or date range

---

## Related

- **Agent used:** `.claude/agents/file-analyzer.md`
- **Agent used:** `.claude/agents/report-generator.md`
- **Skill used:** `.claude/skills/file-analysis/SKILL.md`
- **Memory file:** `.claude/memory/locations.md`

