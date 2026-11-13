"""Print what a folder of Mavic 3M shutter groups can contribute to Fenia."""

import argparse
import sys
from pathlib import Path

from wheat_vision.capture import CaptureReadError, summarize_directory


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        summaries = summarize_directory(args.directory)
    except CaptureReadError as exc:
        print(exc, file=sys.stderr)
        return 1

    for summary in summaries:
        altitude = (
            "unknown"
            if summary.relative_altitude_m is None
            else f"{summary.relative_altitude_m:.2f} m"
        )
        print(f"{summary.capture_id}  {summary.model or 'unknown model'}  {summary.role}")
        print(f"  color {summary.rgb_width_px}x{summary.rgb_height_px}  altitude {altitude}")
        if summary.quality.flags:
            print(f"  color flags: {', '.join(summary.quality.flags)}")
        for band in summary.bands:
            print(
                f"  {band.key} {band.name or ''} {band.frequency or ''}  "
                f"{band.width_px}x{band.height_px}  "
                f"clipped {band.clipped_fraction:.1%}"
            )
        for reason in summary.reasons:
            print(f"  - {reason}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
