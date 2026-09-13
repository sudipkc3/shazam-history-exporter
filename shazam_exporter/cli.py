import argparse
from pathlib import Path

from shazam_exporter.database import get_tracks
from shazam_exporter.models import track_from_database_row
from shazam_exporter.exporters import export_csv, export_json


def create_parser():
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="Export your macOS Shazam history."
    )

    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="both",
        help="Export format. Default: both",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("exports"),
        help="Output directory. Default: exports",
    )

    return parser


def run():
    """Run the Shazam history export."""

    parser = create_parser()
    args = parser.parse_args()

    print("🎵 Shazam History Exporter")
    print("-" * 40)

    try:
        raw_tracks = get_tracks()
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return

    tracks = [
        track_from_database_row(row)
        for row in raw_tracks
    ]

    print(f"Found {len(tracks)} recognized songs.\n")

    output_directory = args.output

    if args.format in ("csv", "both"):
        csv_path = output_directory / "shazam_history.csv"

        export_csv(tracks, csv_path)

        print(f"CSV:  {csv_path}")

    if args.format in ("json", "both"):
        json_path = output_directory / "shazam_history.json"

        export_json(tracks, json_path)

        print(f"JSON: {json_path}")

    print("\nExport complete!")


if __name__ == "__main__":
    run()
