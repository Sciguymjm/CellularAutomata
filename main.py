# -*- coding: UTF-8 -*-
import os
import random
import subprocess

from mingus import containers
from mingus.containers import Note, Bar, Composition, MidiInstrument, NoteContainer

from mingus.containers.instrument import MidiPercussionInstrument

from mingus.midi import midi_file_out

from cellular_musician import SongGen
from cellular_musician.TrackGen import Track, Util

BAR_NUMBER = 4
time_sig = (4, 4)
util = Util()
scale1 = util.major_penta('C')
scale2 = util.major_penta('A')
# BEGIN MELODY #
# setup verse
ini = [False] * 9
ini[random.randint(0, 8)] = True
# instr = random.randint(1, 104)
instr = 0
vel = [70, 100]
# instrument in this function does not matter if you are combining generated tracks
verse = Track(ini).generate(16, BAR_NUMBER, 4, scale=scale1, rand_length=True, time_signature=time_sig,
                            velocity=vel)

# setup bridge
ini = [False] * 9
ini[random.randint(0, 8)] = True
bridge = Track(ini).generate(8, BAR_NUMBER, 4, scale=scale2, rand_length=True, time_signature=time_sig,
                             velocity=vel)

# setup chorus
ini = [False] * 9
ini[random.randint(0, 8)] = True
chorus = Track(ini).generate(8, BAR_NUMBER, 4, scale=scale1, rand_length=True, time_signature=time_sig,
                             velocity=vel)

song = Composition()

trackmain = Track()
# here is where you set the actual instrument

print "Melody instrument: " + trackmain.set_instrument(instr).names[instr] + " ({})".format(instr)

s = SongGen.Song()
trackmain = s.generate(chorus, verse, bridge, trackmain.track)

# LAST BAR
b = Bar()
n = Note('C', 4)
n.set_channel(1)
b.place_notes(n, 4)

trackmain.add_bar(b)
song.add_track(trackmain)

# END MELODY #


# BEGIN HARMONY #

# setup verse
ini = [False] * 5
ini[random.randint(0, 4)] = True
# instr = random.randint(1, 104)
instr = 33
vel = [32, 48]
channel = 2

# instrument in this function does not matter if you are combining generated tracks
verse = Track(ini).generate(2, BAR_NUMBER * 2, 2, scale=scale1, time_signature=time_sig, velocity=vel,
                            channel=channel, rests=False)

# setup bridge
ini = [False] * 5
ini[random.randint(0, 4)] = True
bridge = Track(ini).generate(2, BAR_NUMBER * 2, 2, scale=scale2, time_signature=time_sig, velocity=vel,
                             channel=channel, rests=False)

# setup chorus
ini = [False] * 5
ini[random.randint(0, 4)] = True
chorus = Track(ini).generate(2, BAR_NUMBER * 2, 2, scale=scale1, time_signature=time_sig, velocity=vel,
                             channel=channel, rests=False)

track2 = Track()
# here is where you set the actual instrument

print "Harmony instrument: " + track2.set_instrument(instr).names[instr] + " ({})".format(instr)
track2 = s.generate(chorus, verse, bridge, track2.track)
b = Bar()
n = Note('C', 2)
n.set_channel(2)
b.place_notes(n, 4)

track2.add_bar(b)
song.add_track(track2)





# END HARMONY #

if False:
    bass = MidiInstrument()
    bass.instrument_nr = random.randint(1, 104)
    basstrack = containers.Track(bass)

    print "Bass instrument: " + bass.names[bass.instrument_nr]

    for i in range(0, len(s.song_structure.sections) * BAR_NUMBER):
        b = Bar()
        for i2 in range(0, time_sig[0] / (time_sig[1] / 4)):
            n = Note("C" if s.song_structure.sections[i // BAR_NUMBER] != bridge else "A", 3)
            n.set_channel(2)
            b.place_notes(n, 4)
            # b.place_rest(8)
        basstrack.add_bar(b)

    song.add_track(basstrack)

# set up example drums (basic beat) TODO: generate beat + fills
drumtrack = containers.Track(MidiPercussionInstrument())

vel = 40

bd = MidiPercussionInstrument().bass_drum_1()  # parses name to "note" value (drum sound representation)
bd.set_channel(9)  # required for drums
bd.set_velocity(vel)

sd = MidiPercussionInstrument().acoustic_snare()
sd.set_channel(9)
sd.set_velocity(vel * 1.5)  # snare is too soft normally

hh = MidiPercussionInstrument().closed_hi_hat()
hh.set_channel(9)
hh.set_velocity(vel)

cc = MidiPercussionInstrument().crash_cymbal_1()
cc.set_channel(9)
cc.set_velocity(vel)

# eighth note fills, read each sublist as an eighth beat
possible_fills = [
    [[sd], [sd], [sd], [sd]],
    [[hh, bd], [hh, sd], [hh, bd], [hh, sd]],
    [[bd], [sd], [bd], [sd]],
    [[bd, sd], [bd, sd], [bd, sd], [bd, sd]],
    [[hh], [hh], [hh, bd], [hh, sd]]
]

for i in range(0, len(s.song_structure.sections)):
    notes = [[cc, bd], [hh], [hh, sd], [hh]] + \
            [[hh, bd], [hh, bd], [hh, sd], [hh], [hh, bd], [hh], [hh, sd], [hh]] * 3 + \
            possible_fills[random.randint(0, len(possible_fills) - 1)]
    for num in range(0, BAR_NUMBER):
        b = Bar()
        for i2 in range(0, 8):
            n = NoteContainer()
            n.add_notes(notes[num * 8 + i2])
            b.place_notes(n, 8)
        drumtrack.add_bar(b)

b = Bar()
b.place_notes([cc, bd], 4)

drumtrack.add_bar(b)
song.add_track(drumtrack)

midi_file_out.write_Composition("song.mid", song, bpm=random.randint(8, 14) * 10)
print "Wrote to file..."

MUSESCORE_PATH = 'D:\\Program Files (x86)\\MuseScore 2\\bin\\MuseScore.exe'  # Bad environment detection
if os.path.isfile(MUSESCORE_PATH):
    subprocess.Popen("taskkill /F /IM WWAHost.exe").communicate()  # Kill music app, wait until done
    subprocess.Popen("taskkill /F /IM MuseScore.exe").communicate()  # Kill musescore
    call = '"' + MUSESCORE_PATH + '" ' + '-o "song.mp3" song.mid'  # Convert midi to mp3 using musescore
    subprocess.Popen(call).communicate()
    print "Outputted mp3... opening."
    os.startfile('song.mp3') # open both files
    os.startfile('song.mid')



# midi_file_out.write_Track("random.mid", Track().random_generate(16, 4).track)
