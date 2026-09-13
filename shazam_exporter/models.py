from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


def convert_apple_timestamp(timestamp) -> Optional[str]:
    """Convert Apple's Core Data timestamp to an ISO 8601 datetime."""

    if timestamp is None:
        return None

    apple_epoch = datetime(2001, 1, 1)

    converted_date = apple_epoch + timedelta(seconds=timestamp)

    return converted_date.isoformat()


@dataclass
class Track:
    """Clean representation of a recognized Shazam track."""

    title: str
    artist: str
    album: Optional[str] = None
    date: Optional[str] = None
    apple_music_id: Optional[str] = None
    isrc: Optional[str] = None
    shazam_key: Optional[str] = None
    shazam_url: Optional[str] = None
    artwork_url: Optional[str] = None

    def get_identifier(self) -> tuple[str, str]:
        """
        Return the best available stable identifier for the track.

        Priority:
        1. ISRC
        2. Apple Music ID
        3. Shazam key
        4. Title + artist fallback
        """

        if self.isrc:
            return ("isrc", self.isrc)

        if self.apple_music_id:
            return ("apple_music_id", self.apple_music_id)

        if self.shazam_key:
            return ("shazam_key", self.shazam_key)

        normalized_title = self.title.strip().lower()
        normalized_artist = self.artist.strip().lower()

        return (
            "title_artist",
            f"{normalized_title}|{normalized_artist}",
        )


def track_from_database_row(row: dict) -> Track:
    """Convert a raw SQLite row into a clean Track object."""

    return Track(
        title=row.get("ZTITLE") or "Unknown title",
        artist=row.get("ZSUBTITLE") or "Unknown artist",
        album=row.get("ZALBUMNAME"),
        date=convert_apple_timestamp(row.get("ZDATE")),
        apple_music_id=row.get("ZAPPLEMUSICID"),
        isrc=row.get("ZISRC"),
        shazam_key=row.get("ZSHAZAMKEY"),
        shazam_url=row.get("ZSHAZAMURL"),
        artwork_url=row.get("ZARTWORKURL"),
    )
