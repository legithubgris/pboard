import os
from pedalboard import Pedalboard, load_plugin
from pedalboard.io import AudioFile
from mido import MidiFile, Message

# Load a VST3 or Audio Unit plugin(s) from a known path on disk:
instrument1 = load_plugin("C:/Program Files/Steinberg/VstPlugins/blocks.vst3/Contents/x86_64-win/blocks.vst3")
assert instrument1.is_instrument

instrument2 = load_plugin("C:/Program Files/Steinberg/VstPlugins/blocks.vst3/Contents/x86_64-win/blocks.vst3")
assert instrument2.is_instrument

instrument3 = load_plugin("C:/Program Files/Steinberg/VstPlugins/blocks.vst3/Contents/x86_64-win/blocks.vst3")
assert instrument3.is_instrument

# Set a specific instrument within the VST plugin by loading a preset
instrument1.load_preset("C:/Users/dburbano/Documents/VST3 Presets/soonth/blocks/clappy.vstpreset")
instrument2.load_preset("C:/Users/dburbano/Documents/VST3 Presets/soonth/blocks/snare0.vstpreset")
instrument3.load_preset("C:/Users/dburbano/Documents/VST3 Presets/soonth/blocks/kicky.vstpreset")

# Make a plain old pedalboard with no effects:
board = Pedalboard()

# Read the MIDI file
midi_file_path = 'C:/pyScripts/pedalBoard/OpenSaurceVSTTest.mid'
midi = MidiFile(midi_file_path)

# Render audio for each track and combine
sample_rate = 44100
combined_audio = None

for i, track in enumerate(midi.tracks, start=0):
    midi_messages = [msg for msg in track if not msg.is_meta]
    if i == 1:
        audio = instrument1(midi_messages, duration=midi.length, sample_rate=sample_rate)
    elif i == 2:
        audio = instrument2(midi_messages, duration=midi.length, sample_rate=sample_rate)
    elif i == 3:
        audio = instrument3(midi_messages, duration=midi.length, sample_rate=sample_rate)
    else:
        continue  # Skip any additional tracks

    if combined_audio is None:
        combined_audio = audio
    else:
        combined_audio += audio

# Apply effects to this audio (if any):
effected = board(combined_audio, sample_rate)

# Define the output file path
output_file_path = 'output.wav'

# Open an audio file to write to:
with AudioFile(output_file_path, 'w', sample_rate, effected.shape[0], bit_depth=16) as o:
    o.write(effected)

print("Audio processing complete. Output saved as 'output.wav'.")

# Open the folder containing the output file in Windows Explorer
output_folder = os.path.dirname(os.path.abspath(output_file_path))
os.startfile(output_folder)
