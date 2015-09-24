# -*- coding: UTF-8 -*-
import random
import time

from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.midi import fluidsynth, midi_file_out
import mingus.core.scales as scales
from mingus.containers import instrument





def format(i):
    return "|" + "".join([u'▋' if n else u"  " for n in i]) + "|"


def trackgen(i, length, bars, oct, instrument):
    #what it resets to
    n = [False, False, False, False, False, False, False, False, False]
    track = Track(instrument)
    for b in range(0,(length * bars) / 4):
        bar = Bar("C", (4,4))
        for t in range(0,4):
            note = NoteContainer()
            #stop all current notes
            fluidsynth.stop_NoteContainer(note)
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
            note = NoteContainer()
            drums = NoteContainer()
            scale = scales.Ionian("C").ascending()
            scale = ["C", "D", "E", "G", "A"]


            for index, d in enumerate(i):
                # if index == 9 and d:
        #             drums.add_note(Note(26), octave=0)  #28 = snare drum, for others check https://en.wikipedia.org/wiki/General_MIDI#Percussion and subtract 10
        #             continue
        #         elif index >= 10 and d:
        #             drums.add_note(Note(24), octave=0)
        #             continue
                if d and random.randrange(0,6) == 3:
                    bar.place_rest(length)
                    break
                if d:
                    bar.place_notes(Note(list(reversed(scale))[index if index < 5 else index - 4], octave=oct if index < 5 else oct + 1),length)
                    break
            print format(i)
        track.add_bar(bar)
    return track

# initialize the soundfont
fluidsynth.init("example.SF2")

#fluidsynth.set_instrument(channel=2, bank=126, instr=0)
#initial setup
i = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False]

i[random.randrange(0,8)] = True








melody = instrument.MidiInstrument()
melody.instrument_nr = 1
track1 = trackgen(i, 8, 19, 4, melody)
#midi_file_out.write_Track("track1.mid", track)

i = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False]

i[random.randrange(0,8)] = True



bass = instrument.MidiInstrument()
bass.instrument_nr = 1
track2 = trackgen(i, 4, 19, 3, bass)

comp = Composition()

comp.add_track(track1)
comp.add_track(track2)

midi_file_out.write_Composition("comp.mid",comp)