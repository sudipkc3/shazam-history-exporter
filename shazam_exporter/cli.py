from pathlib import Path

from shazam_exporter.database import get_tracks
from shazam_exporter.models import track_from_database_row
from shazam_exporter.exporters import export_csv, export_json


def run():
    """Run the Shazam history export."""

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

    output_directory = Path("exports")

    csv_path = output_directory / "shazam_history.csv"
    json_path = output_directory / "shazam_history.json"

    export_csv(tracks, csv_path)
    export_json(tracks, json_path)

    print("Export complete!")
    print(f"CSV:  {csv_path}")
    print(f"JSON: {json_path}")
