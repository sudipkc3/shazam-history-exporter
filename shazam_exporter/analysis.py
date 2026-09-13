from collections import Counter

from shazam_exporter.models import Track


def normalize(value: str | None) -> str:
    """Normalize text for comparison."""

    if not value:
        return ""

    return value.strip().lower()


def get_duplicate_groups(
    tracks: list[Track],
) -> list[tuple[tuple[str, str], int]]:
    """
    Find songs that were recognized more than once.

    Songs are compared using normalized title + artist.
    """

    song_keys = [
        (
            normalize(track.title),
            normalize(track.artist),
        )
        for track in tracks
    ]

    counts = Counter(song_keys)

    duplicates = [
        (song, count)
        for song, count in counts.items()
        if count > 1
    ]

    return sorted(
        duplicates,
        key=lambda item: item[1],
        reverse=True,
    )


def get_unique_song_count(tracks: list[Track]) -> int:
    """Return the number of unique title + artist combinations."""

    song_keys = {
        (
            normalize(track.title),
            normalize(track.artist),
        )
        for track in tracks
    }

    return len(song_keys)


def get_unique_tracks(tracks: list[Track]) -> list[Track]:
    """
    Return unique songs from the recognition history.

    Stable identifiers are preferred when available.
    The first occurrence of each song is preserved.
    """

    unique_tracks = []
    seen_identifiers = set()

    for track in tracks:
        identifier = track.get_identifier()

        if identifier in seen_identifiers:
            continue

        seen_identifiers.add(identifier)
        unique_tracks.append(track)

    return unique_tracks
