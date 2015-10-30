import unittest

from TrackGen import Track, NoteChooser

from cellular_musician.TrackGen import Track, Util

util = Util()

def get_init_state():
    ini = [False] * 9
    ini[4] = True
    return ini

def generationTest(verse):
    BAR_NUMBER = 4
    time_sig = (4, 4)
    vel = [70, 100]
    verse.generate(16, BAR_NUMBER, 4, scale=util.major_penta('C'), rand_length=True, time_signature=time_sig,
                            velocity=vel)

class TestTrackGen(unittest.TestCase):

    def test_generate_new_old_avg_track(self):
        """tests create & generate new track using NEW_OLD_AVG"""
        generationTest( Track(get_init_state(), NoteChooser.NEW_OLD_AVG) )
        
    def test_generate_new_track_top(self):
        """tests create & generate new track using TOP"""
        generationTest( Track(get_init_state(), NoteChooser.TOP) )

    def test_generate_new_track_bottom(self):
        """tests create & generate new track using BOTTOM"""
        generationTest( Track(get_init_state(), NoteChooser.BOTTOM) )

    def test_generate_new_track_median(self):
        """tests create & generate new track using MEDIAN"""
        generationTest( Track(get_init_state(), NoteChooser.MEDIAN) )

    def test_generate_new_track_min_interval(self):
        """tests create & generate new track using MIN_INTERVAL"""
        generationTest( Track(get_init_state(), NoteChooser.MIN_INTERVAL) )


