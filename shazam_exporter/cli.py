import argparse
from pathlib import Path

from shazam_exporter.service import load_tracks, export_tracks


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
    """Run the command-line interface."""

    parser = create_parser()
    args = parser.parse_args()

    print("🎵 Shazam History Exporter")
    print("-" * 40)

    try:
        tracks = load_tracks()
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return

    print(f"Found {len(tracks)} recognized songs.\n")

    exported_files = export_tracks(
        tracks,
        args.output,
        args.format,
    )

    for file_path in exported_files:
        print(f"Exported: {file_path}")

    print("\nExport complete!")


if __name__ == "__main__":
    run()
