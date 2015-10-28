from cellular_musician.SongStructureGen import SongSection, SongStructure


class Song(object):
    song_structure = []

    def __init__(self):
        pass

    def generate(self, chorus, verse, bridge, track):
        song_sections = {
            SongSection.CHORUS: chorus.track,
            SongSection.VERSE: verse.track,
            SongSection.BRIDGE: bridge.track,
        }
        self.song_structure = SongStructure(min_len=5)

        all_bars = []
        for section in self.song_structure.sections:
            all_bars += song_sections[section]
        [track.add_bar(bar) for bar in all_bars]
        return track