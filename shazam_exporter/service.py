from pathlib import Path

from shazam_exporter.database import get_tracks
from shazam_exporter.models import track_from_database_row
from shazam_exporter.exporters import export_csv, export_json
from shazam_exporter.analysis import (
    get_unique_song_count,
    get_duplicate_groups,
)


def load_tracks():
    """Load and convert all Shazam history records."""

    raw_tracks = get_tracks()

    return [
        track_from_database_row(row)
        for row in raw_tracks
    ]


def analyze_tracks(tracks):
    """Analyze the loaded Shazam history."""

    total_count = len(tracks)
    unique_count = get_unique_song_count(tracks)
    duplicate_groups = get_duplicate_groups(tracks)

    return {
        "total": total_count,
        "unique": unique_count,
        "duplicate_groups": duplicate_groups,
    }


def export_tracks(
    tracks,
    output_directory: Path,
    export_format: str,
):
    """Export tracks in the requested format."""

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    exported_files = []

    if export_format in ("csv", "both"):
        csv_path = output_directory / "shazam_history.csv"

        export_csv(tracks, csv_path)

        exported_files.append(csv_path)

    if export_format in ("json", "both"):
        json_path = output_directory / "shazam_history.json"

        export_json(tracks, json_path)

        exported_files.append(json_path)

    return exported_files
