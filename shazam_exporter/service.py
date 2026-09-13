from pathlib import Path

from shazam_exporter.database import get_tracks
from shazam_exporter.models import track_from_database_row
from shazam_exporter.exporters import export_csv, export_json
from shazam_exporter.analysis import (
    get_unique_song_count,
    get_duplicate_groups,
    get_unique_tracks,
)
from shazam_exporter.validation import (
    validate_tracks,
    get_valid_track_count,
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


def validate_history(tracks):
    """Validate the quality and completeness of the history."""

    validation = validate_tracks(tracks)

    validation["valid"] = get_valid_track_count(tracks)

    return validation


def get_unique_history_tracks(tracks):
    """Return unique songs from the Shazam history."""

    return get_unique_tracks(tracks)


def export_tracks(
    tracks,
    output_directory: Path,
    export_format: str,
    export_name: str = "shazam_history",
):
    """Export tracks in the requested format."""

    try:
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        exported_files = []

        if export_format in ("csv", "both"):
            csv_path = output_directory / f"{export_name}.csv"

            export_csv(
                tracks,
                csv_path,
            )

            exported_files.append(csv_path)

        if export_format in ("json", "both"):
            json_path = output_directory / f"{export_name}.json"

            export_json(
                tracks,
                json_path,
            )

            exported_files.append(json_path)

        return exported_files

    except OSError as error:
        raise RuntimeError(
            f"Could not write export files: {error}"
        ) from error
