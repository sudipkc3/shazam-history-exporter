import unittest

from shazam_exporter.models import Track
from shazam_exporter.validation import (
    validate_tracks,
    get_valid_track_count,
)


class TestValidation(unittest.TestCase):

    def test_all_required_data_is_present(self):
        tracks = [
            Track(
                title="Test Song",
                artist="Test Artist",
                date="2026-09-13T16:51:25",
                isrc="TEST123",
                shazam_key="123456",
                apple_music_id="789",
                shazam_url="https://example.com",
            )
        ]

        result = validate_tracks(tracks)

        self.assertEqual(result["total"], 1)
        self.assertEqual(result["missing_titles"], 0)
        self.assertEqual(result["missing_artists"], 0)
        self.assertEqual(result["missing_dates"], 0)
        self.assertEqual(result["missing_apple_music_ids"], 0)
        self.assertEqual(result["missing_isrcs"], 0)
        self.assertEqual(result["missing_shazam_keys"], 0)
        self.assertEqual(result["missing_shazam_urls"], 0)

    def test_missing_metadata_is_detected(self):
        tracks = [
            Track(
                title="Test Song",
                artist="Test Artist",
            )
        ]

        result = validate_tracks(tracks)

        self.assertEqual(result["total"], 1)
        self.assertEqual(result["missing_dates"], 1)
        self.assertEqual(result["missing_apple_music_ids"], 1)
        self.assertEqual(result["missing_isrcs"], 1)
        self.assertEqual(result["missing_shazam_keys"], 1)
        self.assertEqual(result["missing_shazam_urls"], 1)

    def test_valid_track_count(self):
        tracks = [
            Track(
                title="Valid Song",
                artist="Valid Artist",
                date="2026-09-13T16:51:25",
                isrc="TEST123",
            ),
            Track(
                title="Invalid Song",
                artist="Valid Artist",
            ),
        ]

        result = get_valid_track_count(tracks)

        self.assertEqual(result, 1)

    def test_shazam_key_is_valid_identifier(self):
        tracks = [
            Track(
                title="Song Without ISRC",
                artist="Artist",
                date="2026-09-13T16:51:25",
                shazam_key="123456",
            )
        ]

        result = get_valid_track_count(tracks)

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
