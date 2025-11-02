---
name: File Analysis Standards
description: Use when analyzing files, extracting file metadata, generating file reports, scanning directories, categorizing files, or working with file collections. Apply these standards for consistent file analysis, metadata extraction, and report generation.
---

# File Analysis Standards

This skill provides standards and best practices for analyzing files, extracting metadata, and generating file reports. Use this when working with file collections, directory scans, or file analysis tasks.

---

## When to use this skill

- When analyzing files in directories (desktop, network drives, project folders)
- When extracting file metadata (size, dates, types, permissions)
- When generating file reports or summaries
- When categorizing files by type or purpose
- When identifying file patterns or anomalies
- When organizing file information for documentation

---

## Guidelines

### Metadata Extraction

- Always use absolute file paths (not relative) for clarity
- Include file size in both bytes and human-readable format (KB, MB, GB)
- Use ISO 8601 format for dates: `YYYY-MM-DDTHH:MM:SSZ`
- Extract file type from extension, not content analysis
- Include modification date, not just creation date
- Note permissions/attributes if accessible and relevant

### File Categorization

**Categories:**
- **Images**: .jpg, .jpeg, .png, .gif, .svg, .webp, .bmp, .tiff
- **Documents**: .pdf, .doc, .docx, .txt, .md, .rtf, .odt
- **Code**: .js, .ts, .py, .java, .cpp, .c, .rb, .go, .rs, .php
- **Archives**: .zip, .tar, .gz, .rar, .7z, .bz2
- **Media**: .mp4, .mp3, .wav, .avi, .mov, .mkv, .flac
- **Data**: .json, .csv, .xlsx, .db, .sqlite, .xml
- **Other**: All extensions not in above categories

**Rules:**
- Be consistent—assign category based on extension only
- If extension missing, categorize as "Other" with note
- Group similar types together (e.g., .doc and .docx both in Documents)

### Report Formatting

**Structure:**
- Summary section at top (file counts, total size, overview)
- Category breakdown with tables
- File listings organized by category
- Insights section for patterns/anomalies

**Tables:**
- Use markdown tables for structured data
- Include: path, size, modified date, type
- Sort by size (descending) or date (descending) as appropriate

**Lists:**
- Use unordered lists for file listings
- Use ordered lists for sequences
- Use checklists for items to review

---

## Standards Reference

For detailed documentation standards, see:
- **Global standards**: `standards/global.md`
- **Backend standards**: `standards/backend.md` (if analyzing code files)

---

## Examples

**Example 1: File List Entry**

```markdown
| Path | Size | Modified | Type |
|------|------|----------|------|
| ~/Desktop/report.pdf | 2.3 MB | 2025-01-15T10:30:00Z | Document |
```

**Example 2: Category Summary**

```markdown
## Documents
- Total files: 15
- Total size: 45.2 MB
- Largest: report.pdf (12.3 MB)
```

---

## Related

- **Used by agents:** `.claude/agents/file-analyzer.md`
- **Used by commands:** `.claude/commands/analyze-files.md`
- **Full standards:** `standards/global.md`

