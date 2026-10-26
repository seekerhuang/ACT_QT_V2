import json
import sys

import pytest

from act_qt_v2.cli.audit_data import main


def test_cli_prints_source_metadata(tmp_path, monkeypatch, capsys):
    source = tmp_path / "data.parquet"
    source.write_bytes(b"data")
    monkeypatch.setattr(sys, "argv", ["act-qt-audit", str(source)])

    main()

    report = json.loads(capsys.readouterr().out)
    assert report["file_count"] == 1
    assert report["file_size_bytes_total"] == 4
    assert report["source_paths"] == [str(source)]


def test_cli_reports_missing_file_without_traceback(tmp_path, monkeypatch, capsys):
    source = tmp_path / "missing.parquet"
    monkeypatch.setattr(sys, "argv", ["act-qt-audit", str(source)])

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert str(source) in output.err
    assert "Traceback" not in output.err


def test_cli_version_does_not_require_source_paths(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["act-qt-audit", "--version"])

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 0
    assert capsys.readouterr().out.strip() == "act-qt-v2 0.1.0"
