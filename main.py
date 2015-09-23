import random
import time
from mingus.containers import Note, NoteContainer

from mingus.core import notes, chords, progressions
from mingus.midi import fluidsynth
import mingus.core.scales as scales

fluidsynth.init("example.SF2")

i = [False,
           False,
           True,
           False,
           True]


n = [False, False, False, False, False, False, False, False]
while True:
    print i
    for ind, s in enumerate(i[1:-1]):
        if ind == len(i) - 1:
            break
        if i[ind-1] and i[ind] and i[ind+1]:
            n[ind] = False
            continue
        if i[ind-1] and i[ind] and not i[ind+1]:
            n[ind] = False
            continue
        if i[ind-1] and not i[ind] and i[ind+1]:
            n[ind] = False
            continue
        if i[ind-1] and not i[ind] and not i[ind+1]:
            n[ind] = True
            continue
        if not i[ind-1] and i[ind] and i[ind+1]:
            n[ind] = True
            continue
        if not i[ind-1] and i[ind] and not i[ind+1]:
            n[ind] = True
            continue
        if not i[ind-1] and not i[ind] and i[ind+1]:
            n[ind] = True
            continue
        else:
            n[ind] = False
    i = n
    n = [False, False, False, False, False, False, False, False]
    note = NoteContainer()
    scale = scales.Ionian("C").ascending()
    for index, d in enumerate(i):
        if d:
            note.add_note(scale[index])
    print note
    fluidsynth.play_NoteContainer(note)
    time.sleep(1)
