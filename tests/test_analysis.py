import unittest

from shazam_exporter.analysis import (
    get_duplicate_groups,
    get_unique_song_count,
    get_unique_tracks,
)
from shazam_exporter.models import Track


class TestAnalysis(unittest.TestCase):

    def setUp(self):
        self.tracks = [
            Track(
                title="Song A",
                artist="Artist A",
                isrc="ISRC001",
            ),
            Track(
                title="Song B",
                artist="Artist B",
                isrc="ISRC002",
            ),
            Track(
                title="Song A",
                artist="Artist A",
                isrc="ISRC001",
            ),
            Track(
                title="Song C",
                artist="Artist C",
                shazam_key="SHAZAM003",
            ),
        ]

    def test_unique_song_count(self):
        result = get_unique_song_count(self.tracks)

        self.assertEqual(result, 3)

    def test_duplicate_groups(self):
        result = get_duplicate_groups(self.tracks)

        self.assertEqual(
            result,
            [
                (("song a", "artist a"), 2),
            ],
        )

    def test_get_unique_tracks(self):
        result = get_unique_tracks(self.tracks)

        self.assertEqual(len(result), 3)

        self.assertEqual(
            result[0].title,
            "Song A",
        )

        self.assertEqual(
            result[1].title,
            "Song B",
        )

        self.assertEqual(
            result[2].title,
            "Song C",
        )


if __name__ == "__main__":
    unittest.main()
