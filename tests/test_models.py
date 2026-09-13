import unittest

from shazam_exporter.models import (
    Track,
    convert_apple_timestamp,
)


class TestConvertAppleTimestamp(unittest.TestCase):

    def test_convert_apple_timestamp(self):
        result = convert_apple_timestamp(0)

        self.assertEqual(
            result,
            "2001-01-01T00:00:00",
        )

    def test_convert_none_timestamp(self):
        result = convert_apple_timestamp(None)

        self.assertIsNone(result)


class TestTrackIdentifier(unittest.TestCase):

    def test_isrc_has_highest_priority(self):
        track = Track(
            title="Test Song",
            artist="Test Artist",
            isrc="TEST123",
            apple_music_id="12345",
            shazam_key="67890",
        )

        self.assertEqual(
            track.get_identifier(),
            ("isrc", "TEST123"),
        )

    def test_apple_music_id_used_when_no_isrc(self):
        track = Track(
            title="Test Song",
            artist="Test Artist",
            apple_music_id="12345",
            shazam_key="67890",
        )

        self.assertEqual(
            track.get_identifier(),
            ("apple_music_id", "12345"),
        )

    def test_shazam_key_used_when_no_isrc_or_apple_music_id(self):
        track = Track(
            title="Test Song",
            artist="Test Artist",
            shazam_key="67890",
        )

        self.assertEqual(
            track.get_identifier(),
            ("shazam_key", "67890"),
        )

    def test_title_artist_used_as_fallback(self):
        track = Track(
            title="  Test Song  ",
            artist="  Test Artist  ",
        )

        self.assertEqual(
            track.get_identifier(),
            ("title_artist", "test song|test artist"),
        )


if __name__ == "__main__":
    unittest.main()
