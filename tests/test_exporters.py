import json
import tempfile
import unittest
from pathlib import Path

from shazam_exporter.exporters import (
    export_csv,
    export_json,
)
from shazam_exporter.models import Track


class TestExporters(unittest.TestCase):

    def setUp(self):
        self.tracks = [
            Track(
                title="Test Song",
                artist="Test Artist",
                album="Test Album",
                date="2026-09-13T16:51:25",
                apple_music_id="12345",
                isrc="TEST123",
                shazam_key="67890",
                shazam_url="https://example.com/shazam",
                artwork_url="https://example.com/artwork.jpg",
            )
        ]

    def test_json_export(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            output_path = Path(temp_directory) / "test.json"

            export_json(
                self.tracks,
                output_path,
            )

            self.assertTrue(output_path.exists())

            with output_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            self.assertEqual(len(data), 1)
            self.assertEqual(
                data[0]["title"],
                "Test Song",
            )
            self.assertEqual(
                data[0]["artist"],
                "Test Artist",
            )
            self.assertEqual(
                data[0]["isrc"],
                "TEST123",
            )

    def test_csv_export(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            output_path = Path(temp_directory) / "test.csv"

            export_csv(
                self.tracks,
                output_path,
            )

            self.assertTrue(output_path.exists())

            content = output_path.read_text(
                encoding="utf-8",
            )

            self.assertIn("title", content)
            self.assertIn("artist", content)
            self.assertIn("Test Song", content)
            self.assertIn("Test Artist", content)
            self.assertIn("TEST123", content)


if __name__ == "__main__":
    unittest.main()
