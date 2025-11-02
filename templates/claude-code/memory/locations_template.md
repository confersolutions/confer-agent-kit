# Permanent Memory — Locations & Context

**Purpose:** Store locations, paths, and preferences for cross-session continuity. Claude Code uses this to resume context across devices and sessions.

**Location:** `.claude/memory/locations.md` (update this file as needed)

---

## Network Drives & Mounts

**Network drives accessible on all devices:**

```yaml
network_drives:
  - name: "SharedDocs"
    path: "\\\\server\\shared\\docs"
    mount_point: "/Volumes/SharedDocs"  # macOS mount
    notes: "Company shared documents"
  
  - name: "Archive"
    path: "\\\\archive\\files"
    mount_point: "/Volumes/Archive"
    notes: "Long-term archive storage"
  
  - name: "Projects"
    path: "smb://fileserver/projects"
    mount_point: "/Volumes/Projects"
    notes: "Active project files"
```

---

## File Locations

**Important file locations (update as needed):**

```yaml
file_locations:
  tax_documents:
    - path: "~/Documents/Taxes/2024/"
      notes: "2024 tax documents"
    - path: "~/Documents/Taxes/2023/"
      notes: "2023 tax documents"
  
  reports:
    default_output: "~/Documents/reports/"
    archive: "~/Documents/reports/archive/"
  
  desktop_files:
    default_path: "~/Desktop/"
    notes: "Desktop is primary working location"
  
  project_files:
    - path: "~/Projects/work/"
      notes: "Work projects"
    - path: "~/Projects/personal/"
      notes: "Personal projects"
```

---

## Recent Activity

**Last analyzed/scanned locations:**

```yaml
recent_activity:
  last_analyzed_path: "~/Desktop/projects/"
  last_analysis_date: "2025-01-15"
  last_analysis_report: "~/Documents/reports/analysis-20250115.md"
  
  last_updated_file: "~/Documents/reports/combined-analysis.md"
  last_update_date: "2025-01-15"
  
  last_scanned_network_drive: "/Volumes/SharedDocs/docs/"
  last_network_scan_date: "2025-01-10"
```

---

## Preferences

**Default paths and preferences:**

```yaml
preferences:
  default_report_path: "~/Documents/reports/"
  default_analysis_output: "~/Documents/reports/"
  
  excluded_directories:
    - "node_modules"
    - ".git"
    - ".DS_Store"
    - "__pycache__"
  
  file_size_threshold_mb: 100  # Flag files larger than this
  recent_file_days: 7  # Consider files modified in last N days as "recent"
  
  output_format: "markdown"  # markdown | json | csv
  include_metadata: true
```

---

## Device-Specific Context

**Device identifiers (useful for cross-device coordination):**

```yaml
devices:
  current_device:
    name: "[Device Name]"
    os: "macOS"  # macOS | Windows | Linux
    home_path: "~/"  # Resolves to full path
  
  network_mappings:
    - local_path: "/Volumes/SharedDocs"
      network_path: "\\\\server\\shared\\docs"
      available_on: ["Device1", "Device2"]
```

---

## Custom Notes

**Any other context to remember:**

```yaml
notes:
  - "Tax documents organized by year in ~/Documents/Taxes/"
  - "Reports saved to ~/Documents/reports/ with date stamps"
  - "Desktop cleanup needed monthly"
  - "Network drives mounted automatically on login"
```

---

## How to Use

**For commands/agents:**

1. Check this file for default paths before prompting user
2. Use `last_analyzed_path` if directory not specified
3. Use `default_report_path` for output if not specified
4. Reference `network_drives` for network paths

**After completing tasks:**

1. Update `recent_activity` with last path/date
2. Update `file_locations` if new important locations discovered
3. Update `preferences` if user changes defaults

**For cross-session continuity:**

- This file helps Claude Code remember where things are
- Update regularly as locations change
- Keep paths consistent (use `~` for home, absolute paths for network)

---

## Template Notes

- Copy this template to `.claude/memory/locations.md`
- Fill in your actual paths and preferences
- Update as your file structure changes
- Keep YAML format for easy parsing
- Use consistent path formats (`~/` for home, absolute paths for network)

