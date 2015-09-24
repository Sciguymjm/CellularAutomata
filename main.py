# -*- coding: UTF-8 -*-
import random
import time

from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.midi import fluidsynth, midi_file_out
import mingus.core.scales as scales
from mingus.containers import instrument


def format_block(i):
    return "|" + "".join([u'▋' if n else u"  " for n in i]) + "|"


def trackgen(i, length, bars, octave, inst):
    # what it resets to
    n = [False, False, False, False, False, False, False, False, False]
    track = Track(inst)
    for b in range(0, (length * bars) / 4):
        bar = Bar("C", (4, 4))
        for t in range(0, 4):
            for ind, s in enumerate(i):
                x = ind - 1
                y = ind
                z = ind + 1
                if ind == 0:
                    x = len(i) - 1
                else:
                    z = 0
                if i[x] and i[y] and i[z]:
                    n[y] = False
                    continue
                if i[x] and i[y] and not i[z]:
                    n[y] = True
                    continue
                if i[x] and not i[y] and i[z]:
                    n[y] = False
                    continue
                if i[x] and not i[y] and not i[z]:
                    n[y] = True
                    continue
                if not i[x] and i[y] and i[z]:
                    n[y] = True
                    continue
                if not i[x] and i[y] and not i[z]:
                    n[y] = False
                    continue
                if not i[x] and not i[y] and i[z]:
                    n[y] = True
                    continue
                else:
                    n[y] = False
            i = n
            n = [False, False, False, False, False, False, False, False, False]
            scale = ["C", "D", "E", "G", "A"]

            for index, d in enumerate(i):
                if d and random.randrange(0, 6) == 3:
                    bar.place_rest(length)
                    break
                if d:
                    # strip off the top note for the melody
                    bar.place_notes(Note(list(reversed(scale))[index if index < 5 else index - 4],
                                         octave=octave if index < 5 else octave + 1), length)
                    break
            print format_block(i)
        track.add_bar(bar)
    return track

# initial setup
ini = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False]

ini[random.randrange(0, 8)] = True

melody = instrument.MidiInstrument()
melody.instrument_nr = 1
track1 = trackgen(ini, 8, 19, 4, melody)

ini = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False]

ini[random.randrange(0, 8)] = True

bass = instrument.MidiInstrument()
bass.instrument_nr = 1
track2 = trackgen(ini, 4, 19, 3, bass)

comp = Composition()

comp.add_track(track1)
comp.add_track(track2)

midi_file_out.write_Composition("comp.mid", comp)
print "Wrote to file..."