# -*- coding: UTF-8 -*-
import random

from mingus.containers import Note, Bar, Track, Composition
from mingus.midi import midi_file_out
from mingus.containers import instrument
from ElementaryCAEngine import Engine, EdgeType
from SongStructureGen import SongStructure, SongSection


def format_block(i):
    return "|" + "".join([u'▋' if n else u"  " for n in i]) + "|"


def trackgen(i, length, bars, octave, inst, scale = ["C", "D", "E", "G", "A"]):
    track = Track(inst)

    rule_number = 30
    automata = Engine(rule_number, init_row=i, edge_type=EdgeType.LOOP)

    for b in range(0, (length * bars) / 4):
        bar = Bar("C", (4, 4))
        for t in range(0, 4):

            automata.step()

            i = automata.rows[-1]


            for index, d in enumerate(i):
                if d and random.randrange(0, 6) == 1:
                    bar.place_rest(length)
                    break
                if index > 0 and d:
                    # strip off the top note for the melody
                    bar.place_notes(Note(list(reversed(scale))[index if index < 5 else index - 4],
                                         octave=octave if index < 5 else octave + 1), length)
                    break
            print format_block(i)
        track.add_bar(bar)
    return track

notes       = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'] * 2
notes = [note.upper() for note in notes]
chroma      = lambda x: [ i for i in notes[ notes.index(x): ] + notes[ :notes.index(x) ] ] + [x]
major       = lambda x: ( chroma(x)[:5] + [chroma(x)[5]] + chroma(x)[5:12] )[::2] + [x]
major_penta = lambda x: [ i for idx, i in enumerate(major(x)) if idx not in (3, 6) ]
minor_penta = lambda x: ( major_penta( notes[ notes.index(x) + 3 ])[:-1] * 2)[-6:]

# setup verse
ini = [False]*9
ini[random.randrange(0, 8)] = True
melody = instrument.MidiInstrument()
melody.instrument_nr = 1
verse = trackgen(ini, 8, 8, 4, melody, scale=major_penta('C'))

# setup bridge
ini = [False]*9
ini[random.randrange(0, 8)] = True
melody = instrument.MidiInstrument()
melody.instrument_nr = 1
bridge = trackgen(ini, 8, 8, 4, melody, scale=major_penta('A'))

# setup chorus
ini = [False]*9
ini[random.randrange(0, 8)] = True
melody = instrument.MidiInstrument()
melody.instrument_nr = 1
chorus = trackgen(ini, 8, 8, 4, melody, scale=major_penta('C'))

song = Composition()
trackmain = Track()

song_sections = {
    SongSection.CHORUS: chorus,
    SongSection.VERSE: verse,
    SongSection.BRIDGE: bridge,
}
song_structure = SongStructure(min_len=5)

all_bars = []
for section in song_structure.sections:
    all_bars += song_sections[section]
[trackmain.add_bar(bar) for bar in all_bars]

song.add_track(trackmain)


midi_file_out.write_Composition("song.mid", song)




# initial setup
ini = [False]*9

ini[random.randrange(0, 8)] = True

melody = instrument.MidiInstrument()
melody.instrument_nr = 1
track1 = trackgen(ini, 8, 19, 4, melody)

ini = [False]*9

ini[random.randrange(0, 8)] = True

bass = instrument.MidiInstrument()
bass.instrument_nr = 1
track2 = trackgen(ini, 4, 19, 3, bass)

comp = Composition()

comp.add_track(track1)
comp.add_track(track2)

print 'generated song structure: ', song_structure.get_sections_string()

midi_file_out.write_Composition("comp.mid", comp)
print "Wrote to file..."