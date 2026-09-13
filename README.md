# 🎵 Shazam History Exporter

Export your **macOS Music Recognition / Shazam history** to CSV and JSON — safely, locally, and without modifying your original database.

<p align="center">

**Read-only • Local • Privacy-friendly • No dependencies**

</p>

<p align="center">

[Overview](#-overview) ·
[Installation](#-installation) ·
[Usage](#-usage) ·
[Exports](#-export-formats) ·
[Architecture](#-architecture) ·
[Development](#-development) ·
[Testing](#testing) ·
[Roadmap](#-roadmap)

</p>

---

## 📌 Overview

**Shazam History Exporter** is a lightweight Python CLI that reads the local database used by macOS Music Recognition and turns your recognized-song history into portable files.

It is designed for people who have accumulated years of Shazam/Music Recognition history but want an easy way to access, analyze, back up, or reuse that data.

### ✨ Features

* 🎵 Read macOS Music Recognition history
* 🔒 Open the database in **read-only mode**
* 📄 Export history to **CSV**
* 🧾 Export history to **JSON**
* 🔁 Detect duplicate recognitions
* 🎯 Extract unique songs
* 🔍 Validate metadata quality
* 🆔 Use stable identifiers such as ISRC and Shazam keys
* 💻 Interactive command-line interface
* ⚡ Direct command-line export
* 📦 Installable as a Python package
* 🚫 No external Python dependencies
* 🔐 Process your data locally

---

## 🧭 Navigation

| Section                                  | Description              |
| ---------------------------------------- | ------------------------ |
| [Overview](#-overview)                   | What the project does    |
| [Installation](#-installation)           | Set up the project       |
| [Usage](#-usage)                         | Run the exporter         |
| [Export Formats](#-export-formats)       | CSV and JSON output      |
| [How It Works](#-how-it-works)           | Data flow                |
| [Architecture](#-architecture)           | Project structure        |
| [Safety & Privacy](#-safety--privacy)    | How your data is handled |
| [Development](#-development)             | Development setup        |
| [Testing](#testing)                      | Run the test suite       |
| [Design Principles](#-design-principles) | Project philosophy       |
| [Roadmap](#-roadmap)                     | Planned features         |
| [Contributing](#-contributing)           | Contribution guidelines  |

---

## 💻 Installation

### Requirements

Currently supported:

* macOS
* Python 3.10+
* macOS Music Recognition / Shazam history

The project uses only Python's standard library and does not require third-party runtime dependencies.

### 1. Clone the repository

```bash
git clone https://github.com/sudipkc3/shazam-history-exporter.git
cd shazam-history-exporter
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install the project

```bash
python -m pip install -e .
```

After installation, the `shazam-history-exporter` command becomes available:

```bash
shazam-history-exporter --version
```

You should see:

```text
Shazam History Exporter 1.0.0
```

---

## 🚀 Usage

When the application starts, it automatically looks for your macOS Music Recognition database.

The application displays a summary similar to:

```text
🎵 Shazam History Exporter
────────────────────────────

🔍 Reading your Music Recognition history...

✓ Found 160 recognized songs.
✓ 153 unique songs.
ℹ 7 songs were recognized more than once.
```

You will then see the main menu:

```text
What would you like to do?

  1. Export history
  2. Export unique songs
  3. View duplicate songs
  4. View data quality
  5. Exit
```

### 1. Export history

Exports **every recognition event**.

For example, if you recognized the same song three times, all three records remain in the history export.

This preserves your original recognition history.

Output:

```text
exports/shazam_history.csv
exports/shazam_history.json
```

### 2. Export unique songs

Creates a deduplicated collection of songs.

For example:

```text
160 recognitions
        ↓
153 unique songs
```

Stable identifiers are preferred when determining whether two records represent the same track.

Output:

```text
exports/unique_songs.csv
exports/unique_songs.json
```

### 3. View duplicate songs

Displays songs that appeared multiple times in your recognition history.

Example:

```text
🔁 Duplicate songs
────────────────────────────

  2×  Example Song
      Example Artist
```

This is useful for understanding repeated recognition events.

### 4. View data quality

Displays the completeness of the extracted metadata.

The application checks fields such as:

* Title
* Artist
* Date
* Shazam key
* Shazam URL
* ISRC
* Apple Music ID

It also determines whether every track has a usable stable identifier.

### 5. Exit

Closes the application without modifying your Music Recognition database.

---

### Command-line options

The exporter supports both an interactive mode and a simple command-line mode.

#### Interactive mode

For the easiest experience, run:

```bash
shazam-history-exporter
```

This opens the interactive menu where you can:

* Export your complete Shazam history
* Export unique songs
* View duplicate songs
* View data quality
* Exit the application

For development, you can also run:

```bash
python main.py
```

#### Direct export

Export the complete recognition history:

```bash
shazam-history-exporter export
```

Export as CSV:

```bash
shazam-history-exporter export --format csv
```

Export as JSON:

```bash
shazam-history-exporter export --format json
```

Export both CSV and JSON:

```bash
shazam-history-exporter export --format both
```

Export only unique songs:

```bash
shazam-history-exporter export --unique
```

Combine unique songs with a specific format:

```bash
shazam-history-exporter export --format csv --unique
```

#### Help and version

View available commands:

```bash
shazam-history-exporter --help
```

View the application version:

```bash
shazam-history-exporter --version
```

The CLI intentionally keeps the number of options small so that common tasks remain simple and approachable.

---

## 📦 Export Formats

### CSV

CSV is useful for:

* Spreadsheets
* Data analysis
* Importing into other applications
* Manual inspection

Example:

```csv
title,artist,album,date,apple_music_id,isrc,shazam_key,shazam_url,artwork_url
Example Song,Example Artist,Example Album,2026-09-13T16:51:25,123456,ABC123,987654,...
```

### JSON

JSON is useful for:

* Programming
* APIs
* Future integrations
* Data processing
* Backups

Example:

```json
[
  {
    "title": "Example Song",
    "artist": "Example Artist",
    "album": "Example Album",
    "date": "2026-09-13T16:51:25",
    "apple_music_id": "123456",
    "isrc": "ABC123",
    "shazam_key": "987654",
    "shazam_url": "https://...",
    "artwork_url": "https://..."
  }
]
```

---

## 🔍 How It Works

The application follows a simple pipeline:

```text
┌──────────────────────────────┐
│ macOS Music Recognition      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ ShazamLibrary.sqlite         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Python database layer        │
│ Read-only SQLite connection  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Track model                  │
│ Clean structured data        │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│ Analysis     │  │ Validation   │
│              │  │              │
│ Duplicates   │  │ Data quality │
│ Unique songs │  │ Identifiers  │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Exporters       │
       │                 │
       │ CSV / JSON      │
       └─────────────────┘
```

---

## 🗄️ macOS Database

The current macOS Music Recognition database is located at:

```text
~/Library/Application Support/com.apple.shazamd/ShazamLibrary.sqlite
```

The database may also have associated SQLite WAL and SHM files:

```text
ShazamLibrary.sqlite
ShazamLibrary.sqlite-wal
ShazamLibrary.sqlite-shm
```

The exporter reads the SQLite database directly.

### Important

The database is opened using SQLite's read-only mode:

```python
database_uri = f"file:{database_path}?mode=ro"
```

The application does **not** write to the original database.

---

## 🆔 Track Identification

The exporter uses stable identifiers whenever available.

Priority:

```text
1. ISRC
2. Apple Music ID
3. Shazam key
4. Title + artist fallback
```

This is important because title and artist strings alone are not always reliable identifiers.

For example, capitalization, whitespace, remix names, or additional metadata can cause two records to look different even when they refer to the same track.

---

## 🔁 Duplicate Analysis

Duplicate analysis currently compares normalized:

```text
title + artist
```

Normalization removes leading/trailing whitespace and makes comparison case-insensitive.

For example:

```text
"Song Name"
"song name"
" SONG NAME "
```

can be treated as the same title for duplicate analysis.

The original recognition records are never deleted.

---

## 🛡️ Safety & Privacy

Privacy and data safety are important design goals of this project.

### Read-only database access

The original Music Recognition database is never intentionally modified.

The database is opened with:

```text
mode=ro
```

### Local processing

Your Shazam history is processed locally by the Python application.

There is currently no:

* Cloud database
* Analytics service
* Tracking
* Login system
* External API requirement
* Automatic upload

### Personal data

Your exported files contain your personal Music Recognition history.

**Do not commit exported history files to GitHub.**

The repository includes:

```gitignore
exports/
```

so generated exports are ignored by Git.

### Never commit your personal history

Before pushing the project:

```bash
git status
```

Make sure files such as these are not being committed:

```text
exports/shazam_history.csv
exports/shazam_history.json
exports/unique_songs.csv
exports/unique_songs.json
```

---

## 🏗️ Architecture

The project intentionally uses small modules instead of putting everything into one large Python file.

```text
shazam-history-exporter/
│
├── .gitignore
├── README.md
├── LICENSE
├── pyproject.toml
├── main.py
│
├── shazam_exporter/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── analysis.py
│   ├── validation.py
│   ├── exporters.py
│   ├── service.py
│   └── cli.py
│
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_analysis.py
    ├── test_validation.py
    └── test_exporters.py
```

### `main.py`

Development entry point.

```text
main.py
   ↓
cli.run()
```

### `pyproject.toml`

Defines the Python package, project metadata, version, build configuration, and installed console command.

```text
pyproject.toml
      ↓
shazam-history-exporter
```

### `database.py`

Responsible for:

* Finding the macOS database
* Opening SQLite
* Read-only access
* Retrieving raw records
* Database error handling

### `models.py`

Responsible for:

* `Track`
* Apple timestamp conversion
* Stable identifiers
* Converting database rows into clean objects

### `analysis.py`

Responsible for:

* Duplicate detection
* Unique song counting
* Unique track extraction

### `validation.py`

Responsible for:

* Metadata completeness
* Missing fields
* Stable identifier validation

### `exporters.py`

Responsible for:

* CSV export
* JSON export
* Converting `Track` objects into serializable dictionaries

### `service.py`

Responsible for coordinating:

```text
Database
    ↓
Models
    ↓
Analysis
    ↓
Validation
    ↓
Export
```

### `cli.py`

Responsible for:

* Terminal interface
* Menus
* User input
* Displaying results
* Friendly error messages
* Command-line arguments

---

## 🧪 Development

### Create the development environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the project

```bash
python -m pip install -e .
```

### Run the application

```bash
python main.py
```

Or use the installed command:

```bash
shazam-history-exporter
```

### Check the version

```bash
shazam-history-exporter --version
```

The project currently uses only Python's standard library, so there are no additional runtime dependencies.

---

## 🧪 Testing

The project includes an automated test suite using Python's built-in `unittest` framework.

### Run all tests

```bash
python -m unittest discover -v
```

### Current test coverage

The test suite currently includes **15 tests** across four modules:

| Test module          |  Tests | Coverage                                       |
| -------------------- | -----: | ---------------------------------------------- |
| `test_models.py`     |      6 | Apple timestamps, Track identifiers, fallbacks |
| `test_analysis.py`   |      3 | Duplicate detection, unique song extraction    |
| `test_validation.py` |      4 | Metadata validation and valid track detection  |
| `test_exporters.py`  |      2 | CSV and JSON export                            |
| **Total**            | **15** | **All passing**                                |

The exporter tests use temporary directories, so running the test suite does not modify the project's real `exports/` directory or the user's Music Recognition history.

### Test structure

```text
tests/
├── __init__.py
├── test_models.py
├── test_analysis.py
├── test_validation.py
└── test_exporters.py
```

The tests use only Python's standard library and require no additional dependencies.

---

## 🧰 Design Principles

The project follows a few simple principles.

### 🔒 Safety First

The original macOS Music Recognition database is **never modified**.

The database is opened in read-only mode, and all exports are written to separate files.

### 🧩 Small, Focused Modules

Functionality is separated into small modules instead of putting everything into one large file.

```text
database.py     → Database access
models.py       → Track data model
analysis.py     → Duplicate and uniqueness analysis
validation.py   → Data quality checks
exporters.py    → CSV and JSON export
service.py      → Application logic
cli.py          → User interface
```

### 📦 Standard Library First

The project currently uses Python's standard library wherever possible, keeping installation simple and avoiding unnecessary dependencies.

### 🧪 Testable Code

Core functionality is covered by automated tests using Python's built-in `unittest` framework.

The test suite currently contains **15 tests** covering models, analysis, validation, and exports.

### 🔐 Privacy by Design

Shazam history is personal data.

Processing happens locally on the user's Mac, and personal history files are excluded from Git using `.gitignore`.

### 🧹 Preserve Original Data

The exporter does not silently remove duplicate recognition events from the history export.

Users can choose between:

* **Full history** — every recognition event
* **Unique songs** — one entry per identified song

### 🛠️ Keep It Simple

The project aims to solve one problem well:

> Safely extracting and exporting macOS Music Recognition history.

Additional features, such as Spotify integration, are kept separate from the core database and export functionality.

---

## 🗺️ Roadmap

### Completed

* [x] SQLite database reader
* [x] Track data model
* [x] Stable track identifiers
* [x] Duplicate analysis
* [x] Unique-song extraction
* [x] CSV export
* [x] JSON export
* [x] Data validation
* [x] Error handling and safety
* [x] README documentation
* [x] GitHub repository cleanup
* [x] Automated test suite
* [x] Improve CLI options
* [x] Add `pyproject.toml` packaging
* [x] Add installable console command

### Planned

* [ ] Improve macOS compatibility
* [ ] Add richer history statistics
* [ ] Spotify integration
* [ ] Spotify track matching
* [ ] Spotify playlist creation
* [ ] GitHub release

---

## 🎧 Future Spotify Integration

Spotify integration is planned as a separate feature rather than being part of the core exporter.

The intended architecture is:

```text
Shazam History
      ↓
Unique Tracks
      ↓
Spotify Matcher
      ↓
Spotify Track IDs
      ↓
Spotify Playlist
```

Potential future functionality:

* Match Shazam tracks with Spotify
* Handle tracks that cannot be found
* Create a Spotify playlist
* Add matched songs automatically
* Report unmatched songs

Spotify integration is **not currently implemented**.

---

## 🤝 Contributing

Contributions are welcome.

Before submitting a pull request:

1. Create a fork of the repository.
2. Create a feature branch.
3. Make your changes.
4. Run the test suite.
5. Make sure personal Shazam exports are not included.
6. Submit a pull request.

Run the tests with:

```bash
python -m unittest discover -v
```

Please keep contributions focused, modular, and consistent with the project's privacy-first design.

---

## ⚠️ Disclaimer

This project is an independent open-source utility and is **not affiliated with, endorsed by, or sponsored by Apple or Shazam**.

The application relies on the local macOS Music Recognition database. Apple may change the database structure, location, or behavior in future macOS versions.

As a result, compatibility may change over time.

---

## 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

## ⭐ Support the Project

If this project helps you export or recover your Music Recognition history, consider:

⭐ Starring the repository
🐛 Reporting issues
💡 Suggesting improvements
🔧 Contributing code

Every contribution helps improve the project for other macOS users.
