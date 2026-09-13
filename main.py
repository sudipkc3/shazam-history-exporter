from shazam_exporter.database import get_tracks
from shazam_exporter.models import track_from_database_row


def main():
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

    for index, track in enumerate(tracks, start=1):
        print(f"{index}. {track.title}")
        print(f"   Artist: {track.artist}")
        print(f"   Album:  {track.album or 'Unknown album'}")
        print(f"   Date:   {track.date or 'Unknown date'}")
        print()


if __name__ == "__main__":
    main()
