# -*- coding: UTF-8 -*-
import random
from mingus import containers

from mingus.containers import Note, Bar, Composition, MidiInstrument, NoteContainer
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.midi import midi_file_out
from mingus.containers import instrument
from cellular_musician import SongGen

from cellular_musician.SongStructureGen import SongStructure, SongSection
from cellular_musician.TrackGen import Track, Util

BAR_NUMBER = 4


util = Util()
# setup verse
ini = [False] * 9
ini[random.randrange(0, 8)] = True

# instrument in this function does not matter if you are combining generated tracks
verse = Track(ini).generate(16, BAR_NUMBER, 4, scale=util.major_penta('C'), rand_length=True)

# setup bridge
ini = [False] * 9
ini[random.randrange(0, 8)] = True
bridge = Track(ini).generate(8, BAR_NUMBER, 4, scale=util.major_penta('A'), rand_length=True)

# setup chorus
ini = [False] * 9
ini[random.randrange(0, 8)] = True
chorus = Track(ini).generate(8, BAR_NUMBER, 4, scale=util.major_penta('C'), rand_length=True)

song = Composition()

trackmain = Track()
# here is where you set the actual instrument

trackmain.set_instrument(1)

s = SongGen.Song()
trackmain = s.generate(chorus, verse, bridge, trackmain.track)

song.add_track(trackmain)

bass = MidiInstrument()
bass.instrument_nr = 38
basstrack = containers.Track(bass)

for i in range(0, len(s.song_structure.sections) * BAR_NUMBER):
    b = Bar()
    for i2 in range(0, 4):
        n = Note("C", 2)
        n.set_channel(2)
        b.place_notes(n, 4)
    basstrack.add_bar(b)

song.add_track(basstrack)

# set up example drums (basic beat) TODO: generate beat + fills
drumtrack = containers.Track(MidiPercussionInstrument())

bd = MidiPercussionInstrument().bass_drum_1()  # parses name to "note" value (drum sound representation)
bd.set_channel(9)  # required for drums
sd = MidiPercussionInstrument().acoustic_snare()
sd.set_channel(9)
hh = MidiPercussionInstrument().closed_hi_hat()
hh.set_channel(9)

notes = [[hh, bd], [hh], [hh, sd], [hh]] * 2
for i in range(0, len(s.song_structure.sections) * BAR_NUMBER):
    b = Bar()
    for i2 in range(0, 8):
        n = NoteContainer()
        n.add_notes(notes[i2])
        b.place_notes(n, 8)
    drumtrack.add_bar(b)
song.add_track(drumtrack)

midi_file_out.write_Composition("song.mid", song)
print "Wrote to file..."


midi_file_out.write_Track("random.mid", Track().random_generate(16, 4).track)





