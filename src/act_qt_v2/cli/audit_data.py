import argparse
import json
from pathlib import Path

from act_qt_v2.dataio import build_data_version


def main() -> None:
    parser = argparse.ArgumentParser(description="Report source-file metadata as JSON.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        report = build_data_version(args.paths)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
