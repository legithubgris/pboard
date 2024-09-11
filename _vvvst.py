import os
from mido import MidiFile

mid = MidiFile('C:/pyScripts/pedalBoard/OpenSaurceVSTTest.mid')

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)