import argparse
import json
from pathlib import Path

from act_qt_v2 import __version__
from act_qt_v2.dataio import build_data_version


def main() -> None:
    parser = argparse.ArgumentParser(description="Report source-file metadata as JSON.")
    parser.add_argument("--version", action="version", version=f"act-qt-v2 {__version__}")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--compact", action="store_true", help="Print JSON on one line.")
    args = parser.parse_args()
    try:
        report = build_data_version(args.paths)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=None if args.compact else 2))


if __name__ == "__main__":
    main()
