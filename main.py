from shazam_exporter.database import get_tracks


def main():
    print("🎵 Shazam History Exporter")
    print("-" * 40)

    try:
        tracks = get_tracks()
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return

    print(f"Found {len(tracks)} recognized songs.\n")

    for index, track in enumerate(tracks, start=1):
        title = track.get("ZTITLE") or "Unknown title"
        artist = track.get("ZSUBTITLE") or "Unknown artist"
        album = track.get("ZALBUMNAME") or "Unknown album"
        date = track.get("ZDATE") or "Unknown date"

        print(f"{index}. {title}")
        print(f"   Artist: {artist}")
        print(f"   Album:  {album}")
        print(f"   Date:   {date}")
        print()


if __name__ == "__main__":
    main()
