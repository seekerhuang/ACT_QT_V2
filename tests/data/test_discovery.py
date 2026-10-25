from datetime import datetime
import os
from pathlib import Path

import pytest

from act_qt_v2.dataio.discovery import build_data_version


def test_empty_sources_are_rejected() -> None:
    with pytest.raises(ValueError, match="source_paths must not be empty"):
        build_data_version([])


def test_single_source_preserves_file_and_reports_timezone(tmp_path: Path) -> None:
    source = tmp_path / "daily.parquet"
    source.write_bytes(b"test source")
    os.utime(source, (1704153600, 1704153600))

    result = build_data_version([source])

    assert result["file_count"] == 1
    assert result["source_paths"] == [str(source)]
    assert result["file_size_bytes_total"] == len(b"test source")
    assert result["last_write_time"] == "2024-01-02T08:00:00+08:00"
    assert source.read_bytes() == b"test source"
    assert source.stat().st_mtime == 1704153600


def test_multiple_sources_are_deduplicated_in_input_order(tmp_path: Path) -> None:
    first = tmp_path / "first.parquet"
    second = tmp_path / "second.parquet"
    first.write_bytes(b"one")
    second.write_bytes(b"second")
    os.utime(first, (1704153600, 1704153600))
    os.utime(second, (1704240000, 1704240000))

    result = build_data_version(path for path in [second, first, second])

    assert result["file_count"] == 2
    assert result["source_paths"] == [str(second), str(first)]
    assert result["file_size_bytes_total"] == 9
    assert len(result["source_file_info"]) == 2
    assert "last_write_time" not in result
    assert datetime.fromisoformat(result["last_write_time_min"]) < datetime.fromisoformat(
        result["last_write_time_max"]
    )


def test_missing_source_is_reported(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        build_data_version([tmp_path / "missing.parquet"])


def test_directory_is_not_reported_as_a_source_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="source path must be a regular file"):
        build_data_version([tmp_path])
