import random


class SongSection(object): # Enum
    # NOTE: be sure to modify _get_next_section probabilities if modifying this list
    CHORUS = 0
    VERSE = 1
    BRIDGE = 2
    END = 3

    enum_to_str_map = {
        CHORUS: "C",
        VERSE: "V",
        BRIDGE: "B"
    }

    @staticmethod
    def list_all():
        return [SongSection.CHORUS, SongSection.VERSE, SongSection.BRIDGE, SongSection.END]

    @staticmethod
    def to_string(section_type):
        return SongSection.enum_to_str_map[section_type]


class SongStructure(object):

    def __init__(self, min_len=1, max_len=99):
        self.sections = []
        self.generate(min_len, max_len)

    def get_sections_string(self):
        str = "|"
        for section in self.sections:
            str += SongSection.to_string(section)
            str += "|"
        return str

    def generate(self, min_len, max_len, starts_with=[]):
        # generates song with length between min_len & max_len distinct parts
        # use starts_with to start off the song with a particular part,
        #     ie starts_with=[SongSection.VERSE, SongSection.CHORUS]
        if len(starts_with) < 1:
            starting_choices = SongSection.list_all()
            starting_choices.remove(SongSection.END)
            self.sections = [SongSection.VERSE]  # start w/ verse, why not?
        else:
            self.sections = starts_with

        while len(self.sections) < max_len and self.sections[-1] != SongSection.END :
            self.sections.append(self._get_next_section(self.sections))

            # check that song isn't ending too soon
            if self.sections[-1] == SongSection.END and len(self.sections) <= min_len:
                self.sections.pop()

        # remove END songSection
        self.sections.pop()

    @staticmethod
    def _get_next_section(prev_sections):
        # most popular (for modern popular music) should be:
        #   Verse - Chorus - Verse - Chorus - Bridge - Chorus
        # other popular ones:
        #   verse/chorus/verse/chorus/solo/chorus
        #   verse/lift/chorus/verse/lift/chorus/solo/lift/chorus
        #   verse/verse/bridge/verse
        #   verse/verse/verse

        section_weights = [
        #x=  CH   V  B
            [ 1, 40, 10],  # P(CH | x)
            [40, 40, 10],  # P( V | x)
            [10, 10,  1],  # P( B | x)
            [30, 20,  1],  # P( E | x)
        ]

        p_sections = {
            SongSection.CHORUS: 0,
            SongSection.VERSE: 0,
            SongSection.BRIDGE: 0,
            SongSection.END: 0
        }

        for section_type in SongSection.list_all():
            p_sections[section_type] += section_weights[section_type][prev_sections[-1]]

        my_list = [SongSection.CHORUS] * p_sections[SongSection.CHORUS]\
                + [SongSection.VERSE]  * p_sections[SongSection.VERSE] \
                + [SongSection.BRIDGE] * p_sections[SongSection.BRIDGE] \
                + [SongSection.END]    * p_sections[SongSection.END]

        return random.choice(my_list)