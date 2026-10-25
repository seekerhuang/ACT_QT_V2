"""Source-file metadata auditing ported from ACT_QT_V3."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from stat import S_ISREG
from typing import Iterable
from zoneinfo import ZoneInfo

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


def build_data_version(source_paths: Iterable[Path]) -> dict[str, object]:
    source_paths = list(dict.fromkeys(Path(path) for path in source_paths))
    if not source_paths:
        raise ValueError("source_paths must not be empty")

    source_file_info = []
    for path in source_paths:
        stat = path.stat()
        if not S_ISREG(stat.st_mode):
            raise ValueError(f"source path must be a regular file: {path}")
        source_file_info.append(
            {
                "path": str(path),
                "size_bytes": int(stat.st_size),
                "last_write_time": datetime.fromtimestamp(stat.st_mtime, tz=SHANGHAI_TZ).isoformat(),
            }
        )

    timestamps = [item["last_write_time"] for item in source_file_info]
    payload: dict[str, object] = {
        "file_count": len(source_paths),
        "source_paths": [str(path) for path in source_paths],
        "file_size_bytes_total": int(sum(item["size_bytes"] for item in source_file_info)),
        "source_file_info": source_file_info,
        "last_write_time_min": min(timestamps),
        "last_write_time_max": max(timestamps),
    }
    if len(source_paths) == 1:
        payload["last_write_time"] = timestamps[0]
    return payload
