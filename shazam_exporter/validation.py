from shazam_exporter.models import Track


def validate_tracks(tracks: list[Track]) -> dict:
    """
    Check the completeness of the Shazam track data.

    This function does not modify or remove any tracks.
    """

    return {
        "total": len(tracks),

        "missing_titles": sum(
            not track.title
            or track.title == "Unknown title"
            for track in tracks
        ),

        "missing_artists": sum(
            not track.artist
            or track.artist == "Unknown artist"
            for track in tracks
        ),

        "missing_dates": sum(
            not track.date
            for track in tracks
        ),

        "missing_apple_music_ids": sum(
            not track.apple_music_id
            for track in tracks
        ),

        "missing_isrcs": sum(
            not track.isrc
            for track in tracks
        ),

        "missing_shazam_keys": sum(
            not track.shazam_key
            for track in tracks
        ),

        "missing_shazam_urls": sum(
            not track.shazam_url
            for track in tracks
        ),
    }


def get_valid_track_count(
    tracks: list[Track],
) -> int:
    """
    Return the number of tracks with the required metadata.

    A track is considered valid when it has:
    - a title
    - an artist
    - a date
    - a stable identifier
    """

    valid_count = 0

    for track in tracks:
        has_title = bool(
            track.title
            and track.title != "Unknown title"
        )

        has_artist = bool(
            track.artist
            and track.artist != "Unknown artist"
        )

        has_date = bool(track.date)

        has_identifier = bool(
            track.isrc
            or track.apple_music_id
            or track.shazam_key
        )

        if (
            has_title
            and has_artist
            and has_date
            and has_identifier
        ):
            valid_count += 1

    return valid_count
