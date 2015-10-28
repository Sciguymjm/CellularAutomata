import random
import math

from mingus import containers

from mingus.containers import Bar, Note, MidiInstrument

from cellular_musician.ElementaryCAEngine import Engine
from cellular_musician.ElementaryCAEngine import EdgeType


class Track(object):
    """
        A track generating class.
        Future goal is to wrap all mingus needed so user can easily modify songs.
    """
    initial = []
    instrument_nr = 0
    track = None

    def __init__(self, initial=[]):
        self.initial = initial
        self.track = containers.Track()

    def set_instrument(self, number):
        self.instrument_nr = number

    def generate(self, length, bars, octave, scale=["C", "D", "E", "G", "A"], rand_length=False):
        # create the instrument for the main track
        instr = MidiInstrument()
        instr.instrument_nr = 1  # MIDI instrument number: http://www.midi.org/techspecs/gm1sound.php
        track = containers.Track(instr)
        if not self.initial:
            self.initial = [False] * 9
            print "Error: initial set empty. Defaulting..."
        rule_number = 30
        if rand_length:
            length = 4
        automata = Engine(rule_number, init_row=self.initial, edge_type=EdgeType.LOOP)
        for b in range(0, (length * bars) / 4):
            bar = Bar("C", (4, 4))
            while bar.space_left() != 0:

                automata.step()

                i = automata.rows[-1]
                if rand_length:
                    length = int(math.pow(2, random.randrange(2, 5)))
                for index, d in enumerate(i):
                    if rand_length:
                        left = bar.space_left()
                        space = ((left - (left % 0.25)) * 16) if left > 0.25 else left * 16
                        if space < 16 / length:
                            length = int(16.0 / space)
                    if d and random.randrange(0, 6) == 1:
                        bar.place_rest(length)
                        break
                    if index > 0 and d:
                        # strip off the top note for the melody
                        bar.place_notes(Note(list(reversed(scale))[index if index < 5 else index - 4],
                                             octave=octave if index < 5 else octave + 1), length)
                        break
                print Track.format_block(i)
            track.add_bar(bar)
        self.track = track
        return self

    def random_generate(self, bars, octave):
        # Generates track in random key with random note lengths
        scale = Util().major_penta(Util().notes[random.randrange(0, len(Util().notes))])
        length = 8
        # create the instrument for the main track
        instr = MidiInstrument()
        instr.instrument_nr = random.randrange(1,
                                               104)  # MIDI instrument number: http://www.midi.org/techspecs/gm1sound.php
        track = containers.Track(instr)
        self.initial = [False] * 9
        self.initial[random.randrange(0, 8)] = True
        rule_number = 30
        automata = Engine(rule_number, init_row=self.initial, edge_type=EdgeType.LOOP)
        for b in range(0, bars):
            bar = Bar("C", (4, 4))
            previous = 0
            while bar.space_left() != 0:
                automata.step()

                i = automata.rows[-1]
                length = int(math.pow(2, random.randrange(2, 5)))
                if length > 16:
                    print length
                for index, d in enumerate(i):
                    left = bar.space_left()
                    space = ((left - (left % 0.25)) * 16) if left > 0.25 else left * 16
                    if space < 16 / length:
                        length = int(16.0 / space)
                    if d and random.randrange(0, 20) == 1:
                        bar.place_rest(length)
                        break
                    if index > 0 and d:
                        # strip off the top note for the melody
                        bar.place_notes(Note(list(reversed(scale))[index if index < 5 else index - 4],
                                             octave=octave if index < 5 else octave + 1), length)
                        previous = length
                        break
                print Track.format_block(i)

            track.add_bar(bar)
        self.track = track
        return self

    @staticmethod
    def format_block(i1):
        return "|" + "".join([u'?' if n1 else u"  " for n1 in i1]) + "|"


class Util(object):
    notes = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'] * 2
    notes = [note.upper() for note in notes]

    def chroma(self, x):
        return [i for i in self.notes[self.notes.index(x):] + self.notes[:self.notes.index(x)]] + [x]

    def major(self, x):
        return (self.chroma(x)[:5] + [self.chroma(x)[5]] + self.chroma(x)[5:12])[::2] + [x]

    def major_penta(self, x):
        return [i for idx, i in enumerate(self.major(x)) if idx not in (3, 6)]

    def minor_penta(self, x):
        return (self.major_penta(self.notes[self.notes.index(x) + 3])[:-1] * 2)[-6:]
