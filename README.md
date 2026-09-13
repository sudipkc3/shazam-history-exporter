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
[Testing](#testing)
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
* 📁 Choose a custom export directory
* 💻 Interactive command-line interface
* 🚫 No external Python dependencies
* 🔐 Process your data locally

---

## 🧭 Navigation

| Section                               | Description              |
| ------------------------------------- | ------------------------ |
| [Overview](#-overview)                | What the project does    |
| [Installation](#-installation)        | Set up the project       |
| [Usage](#-usage)                      | Run the exporter         |
| [Export Formats](#-export-formats)    | CSV and JSON output      |
| [How It Works](#-how-it-works)        | Data flow                |
| [Architecture](#-architecture)        | Project structure        |
| [Safety & Privacy](#-safety--privacy) | How your data is handled |
| [Development](#-development)          | Development setup        |
| [Testing](#testing)                  | Development setup        |
| [Roadmap](#-roadmap)                  | Planned features         |
| [Contributing](#-contributing)        | Contribution guidelines  |

---

## 💻 Installation

### Requirements

Currently supported:

* macOS
* Python 3.10+
* macOS Music Recognition / Shazam history

No third-party Python packages are required.

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

### 4. Run the application

```bash
python main.py
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

This is useful for understanding how often the same song was recognized.

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

Do **not** commit exported history files to GitHub.

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
├── main.py
│
└── shazam_exporter/
    ├── __init__.py
    ├── database.py
    ├── models.py
    ├── analysis.py
    ├── validation.py
    ├── exporters.py
    ├── service.py
    └── cli.py
```

### `main.py`

Application entry point.

```text
main.py
   ↓
cli.run()
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
* Confirmation
* Displaying results
* Friendly error messages

---

## 🧪 Development

### Create the development environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Run the application

```bash
python main.py
```

### Check the project

The project currently uses only Python's standard library, so there are no dependency installation steps.

---

## Testing

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

## 🧰 Design Principles

The project follows a few simple principles.

#
