# 📂 Professional File Organizer (Python)

A production-style Python automation tool that organizes files into folders based on file type using configurable rules.

## 🚀 Features
- Configurable rules via `rules.json`
- Safe file renaming (prevents overwrite)
- Dry-run mode (preview changes)
- Recursive organization
- Optional grouping by date (YYYY-MM)
- CLI arguments & logging

## ▶️ Usage

### Preview changes (recommended)
```bash
python organize.py ~/Downloads --dry-run
