import argparse
import json
import logging
from pathlib import Path
from datetime import datetime


def load_rules(rules_path: Path) -> dict:
    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")
    data = json.loads(rules_path.read_text(encoding="utf-8"))
    return {k: [e.lower() for e in v] for k, v in data.items()}


def get_target_folder(ext: str, rules: dict, default: str) -> str:
    for folder, exts in rules.items():
        if ext in exts:
            return folder
    return default


def safe_path(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while True:
        candidate = dest.with_name(f"{stem} ({i}){suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def organize_files(
    base: Path,
    rules: dict,
    default: str,
    recursive: bool,
    dry_run: bool,
    by_date: bool,
):
    files = base.rglob("*") if recursive else base.iterdir()
    moved = 0

    for item in files:
        if not item.is_file() or item.name.startswith("."):
            continue

        folder = get_target_folder(item.suffix.lower(), rules, default)

        if by_date:
            month = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m")
            dest_dir = base / folder / month
        else:
            dest_dir = base / folder

        if dest_dir in item.parents:
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        target = safe_path(dest_dir / item.name)

        logging.info("%s -> %s", item, target)
        if not dry_run:
            item.rename(target)
            moved += 1

    logging.info("Completed. %s file(s) processed.", moved)


def main():
    parser = argparse.ArgumentParser(description="Professional File Organizer")
    parser.add_argument("path", nargs="?", default=".", help="Folder to organize")
    parser.add_argument("--rules", default="rules.json", help="Rules config file")
    parser.add_argument("--default", default="Other", help="Default folder name")
    parser.add_argument("--recursive", action="store_true", help="Organize subfolders")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving")
    parser.add_argument("--by-date", action="store_true", help="Group by month")
    parser.add_argument("--log", default="info", choices=["debug", "info", "warning"])

    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log.upper()),
        format="%(levelname)s: %(message)s",
    )

    base = Path(args.path).expanduser().resolve()
    rules = load_rules(Path(args.rules))

    organize_files(
        base=base,
        rules=rules,
        default=args.default,
        recursive=args.recursive,
        dry_run=args.dry_run,
        by_date=args.by_date,
    )


if __name__ == "__main__":
    main()
