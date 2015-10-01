import unittest

from SongStructureGen import SongStructure


class TestSongStructure(unittest.TestCase):

    def test_create_new(self):
        """tests create new song structure"""
        song = SongStructure()

        print song.get_sections_string()
        # TODO:
        # self.assertTrue(SOMETHING...)
