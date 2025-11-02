# Update MD File Command

**Purpose:** Update an existing markdown file with new findings, merge content, or append sections.

**Usage:** `/update-md [target-file] [source-content]`

**Example:** `/update-md ~/Documents/reports/analysis.md "New findings from file scan"`

---

## Overview

This command safely updates markdown files by:
- Merging new content into existing sections
- Appending new sections at the end
- Preserving existing structure and formatting
- Creating backups before modifications

**Inputs:**
- Target file: Markdown file to update (must exist or will be created)
- Source content: New content to merge/append (file path or direct content)
- Update mode: `merge` (update sections) or `append` (add new sections)

**Outputs:**
- Updated markdown file
- Backup file: `[target-file].backup-[timestamp]`

---

## Workflow

### Phase 1: Prepare Update

**Checklist:**
- ☐ Target file exists (or create new)
- ☐ Read target file structure
- ☐ Identify existing sections
- ☐ Read source content (file or provided text)
- ☐ Create backup: `[target-file].backup-[timestamp]]`

**Memory check:**
- If target file not specified, check `.claude/memory/locations.md` for `default_report_file` or `last_updated_file`

### Phase 2: Merge or Append

**Merge mode** (update existing sections):
- Match section headers in source with target
- Update matching sections with new content
- Preserve unmatched sections
- Maintain formatting and structure

**Append mode** (add new sections):
- Append new sections at end of file
- Avoid duplicate section headers
- Add date stamp to new sections

**Checklist:**
- ☐ Backup created
- ☐ Content merged/appended correctly
- ☐ Formatting preserved
- ☐ No duplicate sections (append mode)

### Phase 3: Validate & Save

- Validate markdown syntax
- Ensure file structure is intact
- Write updated content
- Verify file saved successfully

**Checklist:**
- ☐ Markdown syntax valid
- ☐ File structure intact
- ☐ Changes saved
- ☐ Backup preserved

---

## Memory & Context

**Update memory after completion:**
- Update `.claude/memory/locations.md`:
  - `last_updated_file`: [target file path]
  - `last_update_date`: [YYYY-MM-DD]
  - `backup_location`: [backup file path]

**Reference memory during execution:**
- Default target files for common reports
- Backup preferences (location, retention)
- Formatting preferences

---

## Completion

**Success criteria:**
- ☐ Target file updated with new content
- ☐ Backup file created
- ☐ Original formatting preserved
- ☐ Changes verified

**Next steps:**
- Review updated file
- Commit changes if using version control
- Run `/analyze-files` again if needed

---

## Tips

- **Backups:** Always creates backup before modifications
- **Merge vs Append:** Use merge for updating existing sections, append for adding new info
- **Large files:** Command handles large markdown files efficiently
- **Formatting:** Preserves existing markdown formatting and structure

---

## Related

- **Agent used:** `.claude/agents/md-updater.md` (if created)
- **Memory file:** `.claude/memory/locations.md`

