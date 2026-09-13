import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path.home()
    / "Library"
    / "Application Support"
    / "com.apple.shazamd"
    / "ShazamLibrary.sqlite"
)


def get_database_path() -> Path:
    """Return the macOS Music Recognition database path."""

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Shazam database not found at: {DATABASE_PATH}"
        )

    return DATABASE_PATH


def connect_database() -> sqlite3.Connection:
    """
    Open the Music Recognition database in read-only mode.

    The original SQLite database is never modified.
    """

    database_path = get_database_path()

    database_uri = f"file:{database_path}?mode=ro"

    connection = sqlite3.connect(
        database_uri,
        uri=True,
    )

    connection.row_factory = sqlite3.Row

    return connection


def get_tracks() -> list[dict]:
    """
    Retrieve all recognized tracks from the Music Recognition database.
    """

    query = """
        SELECT *
        FROM ZSHTRACKMO
        ORDER BY ZDATE DESC
    """

    with connect_database() as connection:
        rows = connection.execute(query).fetchall()

    return [dict(row) for row in rows]
