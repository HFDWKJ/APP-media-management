"""Single CSV report per reorganize run (timestamped filename)."""

from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from utils.paths import log_dir

CSV_PREFIX = "reorganize_"
CSV_COLUMNS = [
    "sequence_no",
    "original_relative_path",
    "original_filename",
    "original_absolute_path",
    "new_filename",
    "new_absolute_path",
    "new_relative_path",
    "original_folder_name",
    "original_folder_path",
    "file_hash",
    "media_id",
    "processed_at",
]


def report_filename(processed_at: datetime | None = None) -> str:
    ts = processed_at or datetime.now(timezone.utc)
    if ts.tzinfo is None or ts.utcoffset() is None:
        raise ValueError("processed_at must include a timezone")
    return ts.astimezone(timezone.utc).strftime("%Y%m%d%H") + "-reorganize.csv"


def write_reorganize_csv(
    folder: Path,
    rows: list[dict[str, Any]],
    *,
    processed_at: datetime | None = None,
) -> Path:
    """Write a run receipt under .log; folder identifies its source, not its destination."""
    folder = folder.resolve()
    processed_at = processed_at or datetime.now(timezone.utc)
    source_id = hashlib.sha256(str(folder).encode("utf-8")).hexdigest()[:12]
    basename = Path(report_filename(processed_at)).stem + "-" + source_id
    root = log_dir()
    when = (processed_at or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    sequence = 1
    while True:
        suffix = "" if sequence == 1 else f"-{sequence}"
        path = root / f"{basename}{suffix}.csv"
        try:
            handle = path.open("x", encoding="utf-8-sig", newline="")
            break
        except FileExistsError:
            sequence += 1
    with handle as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out.setdefault("processed_at", when)
            writer.writerow(out)
    return path


def find_latest_reorganize_csv(folder: Path) -> Path | None:
    folder = folder.resolve()
    source_id = hashlib.sha256(str(folder).encode("utf-8")).hexdigest()[:12]
    current = list(log_dir().glob(f"[0-9]?????????-reorganize-{source_id}*.csv"))
    legacy = list(folder.glob(f"{CSV_PREFIX}*.csv"))
    candidates = sorted(current + legacy, key=lambda path: path.stat().st_mtime_ns, reverse=True)
    return candidates[0] if candidates else None
