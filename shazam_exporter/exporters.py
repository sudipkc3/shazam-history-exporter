import csv
import json
from pathlib import Path

from shazam_exporter.models import Track


def track_to_dict(track: Track) -> dict:
    """Convert a Track object into a dictionary."""

    return {
        "title": track.title,
        "artist": track.artist,
        "album": track.album,
        "date": track.date,
        "apple_music_id": track.apple_music_id,
        "isrc": track.isrc,
        "shazam_key": track.shazam_key,
        "shazam_url": track.shazam_url,
        "artwork_url": track.artwork_url,
    }


def export_json(
    tracks: list[Track],
    output_path: Path,
) -> None:
    """Export tracks to a JSON file."""

    data = [
        track_to_dict(track)
        for track in tracks
    ]

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def export_csv(
    tracks: list[Track],
    output_path: Path,
) -> None:
    """Export tracks to a CSV file."""

    data = [
        track_to_dict(track)
        for track in tracks
    ]

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not data:
        return

    fieldnames = list(data[0].keys())

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(data)
