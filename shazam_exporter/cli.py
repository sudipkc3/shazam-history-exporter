from shazam_exporter.service import (
    load_tracks,
    analyze_tracks,
    export_tracks,
)


def print_header():
    """Display the application header."""

    print()
    print("🎵 Shazam History Exporter")
    print("─" * 44)
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
            from pathlib import Path
            return Path("exports")

        if choice == "2":
            from pathlib import Path

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

    print(f"✓ Found {analysis['total']} recognized songs.")
    print(f"✓ {analysis['unique']} unique songs.")

    if analysis["duplicate_groups"]:
        print(
            f"ℹ {len(analysis['duplicate_groups'])} "
            "songs were recognized more than once."
        )

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


if __name__ == "__main__":
    run()
