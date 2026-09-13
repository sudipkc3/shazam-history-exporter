from pathlib import Path

from shazam_exporter.service import (
    load_tracks,
    analyze_tracks,
    export_tracks,
    get_unique_history_tracks,
)


def print_header():
    """Display the application header."""

    print()
    print("🎵 Shazam History Exporter")
    print("─" * 44)
    print()


def show_summary(analysis):
    """Display a summary of the Shazam history."""

    print(f"✓ Found {analysis['total']} recognized songs.")
    print(f"✓ {analysis['unique']} unique songs.")

    if analysis["duplicate_groups"]:
        print(
            f"ℹ {len(analysis['duplicate_groups'])} "
            "songs were recognized more than once."
        )

    print()


def show_duplicate_songs(analysis):
    """Display songs that were recognized more than once."""

    duplicates = analysis["duplicate_groups"]

    print()
    print("🔁 Duplicate songs")
    print("─" * 44)
    print()

    if not duplicates:
        print("✓ No duplicate songs found.")
        print()
        input("Press Enter to return...")
        return

    for (title, artist), count in duplicates:
        print(f"  {count}×  {title.title()}")
        print(f"      {artist.title()}")
        print()

    print("─" * 44)
    print()
    input("Press Enter to return...")


def choose_main_action():
    """Ask the user what they want to do."""

    print("What would you like to do?")
    print()
    print("  1. Export history")
    print("  2. Export unique songs")
    print("  3. View duplicate songs")
    print("  4. Exit")
    print()

    while True:
        choice = input("Select an option [1]: ").strip()

        if choice == "":
            choice = "1"

        if choice in ("1", "2", "3", "4"):
            return choice

        print("⚠️  Invalid option. Please choose 1, 2, 3, or 4.")
        print()


def choose_output_directory():
    """Ask the user where the export should be saved."""

    print("📁 Step 1 of 2 — Choose export location")
    print("─" * 44)
    print()
    print("Where do you want to save your export?")
    print()
    print("  1. Default folder")
    print("     ./exports/")
    print()
    print("  2. Custom folder")
    print("  3. Cancel")
    print()

    while True:
        choice = input("Select an option [1]: ").strip()

        if choice == "":
            choice = "1"

        if choice == "1":
            return Path("exports")

        if choice == "2":
            print()
            folder = input("Enter output folder: ").strip()

            if not folder:
                print("⚠️  Folder cannot be empty.")
                print()
                continue

            return Path(folder).expanduser()

        if choice == "3":
            return None

        print("⚠️  Invalid option. Please choose 1, 2, or 3.")
        print()


def choose_export_format():
    """Ask the user which export format they want."""

    print()
    print("📦 Step 2 of 2 — Choose export format")
    print("─" * 44)
    print()
    print("What format would you like?")
    print()
    print("  1. CSV")
    print("  2. JSON")
    print("  3. CSV + JSON")
    print("  4. Cancel")
    print()

    while True:
        choice = input("Select an option [3]: ").strip()

        if choice == "":
            choice = "3"

        if choice == "1":
            return "csv"

        if choice == "2":
            return "json"

        if choice == "3":
            return "both"

        if choice == "4":
            return None

        print("⚠️  Invalid option. Please choose 1, 2, 3, or 4.")
        print()


def confirm_export(
    track_count,
    output_directory,
    export_format,
):
    """Show export summary and ask for confirmation."""

    format_names = {
        "csv": "CSV",
        "json": "JSON",
        "both": "CSV + JSON",
    }

    print()
    print("📋 Export summary")
    print("─" * 44)
    print()
    print(f"  Songs:      {track_count}")
    print(f"  Location:   {output_directory}")
    print(f"  Format:     {format_names[export_format]}")
    print()
    print("Ready to export?")
    print()

    choice = input("Continue? [Y/n]: ").strip().lower()

    return choice in ("", "y", "yes")


def run_export(tracks, export_name="shazam_history"):
    """Run the export workflow."""

    output_directory = choose_output_directory()

    if output_directory is None:
        print()
        print("❌ Export cancelled.")
        return

    export_format = choose_export_format()

    if export_format is None:
        print()
        print("❌ Export cancelled.")
        return

    confirmed = confirm_export(
        len(tracks),
        output_directory,
        export_format,
    )

    if not confirmed:
        print()
        print("❌ Export cancelled.")
        return

    print()
    print("─" * 44)
    print()
    print(f"📤 Exporting {len(tracks)} songs...")
    print()

    exported_files = export_tracks(
        tracks,
        output_directory,
        export_format,
    )

    for file_path in exported_files:
        print(f"✓ Exported: {file_path}")

    print()
    print("─" * 44)
    print()
    print(f"🎉 Successfully exported {len(tracks)} songs!")
    print(f"📁 Location: {output_directory}")
    print()


def run():
    """Run the interactive command-line interface."""

    print_header()

    print("🔍 Reading your Music Recognition history...")
    print()

    try:
        tracks = load_tracks()
    except FileNotFoundError as error:
        print(f"❌ Error: {error}")
        return

    analysis = analyze_tracks(tracks)

    show_summary(analysis)

    while True:
        action = choose_main_action()

        if action == "1":
            run_export(tracks)
            return

        if action == "2":
            unique_tracks = get_unique_history_tracks(tracks)

            print()
            print("🎵 Unique songs")
            print("─" * 44)
            print()
            print(
                f"Found {len(unique_tracks)} unique songs "
                f"from {len(tracks)} recognitions."
            )
            print()

            run_export(
                unique_tracks,
                export_name="unique_songs",
            )
            return

        if action == "3":
            show_duplicate_songs(analysis)
            print()
            continue

        if action == "4":
            print()
            print("👋 Goodbye!")
            print()
            return


if __name__ == "__main__":
    run()
