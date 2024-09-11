import os
from pedalboard import Pedalboard, load_plugin
from pedalboard.io import AudioFile
from mido import Message  # not part of Pedalboard, but convenient!

# Load a VST3 or Audio Unit plugin from a known path on disk:
instrument = load_plugin("C:/Program Files/Steinberg/VstPlugins/blocks.vst3/Contents/x86_64-win/blocks.vst3")
assert instrument.is_instrument

# Set a specific instrument within the VST plugin by loading a preset
instrument.load_preset("C:/Users/dburbano/Documents/VST3 Presets/soonth/blocks/snare0.vstpreset")

# Make a plain old pedalboard with no effects:
board = Pedalboard()

# Render some audio by passing MIDI to an instrument:
sample_rate = 44100
midi_messages = [
    Message("note_on", note=60, velocity=64, time=0),
    Message("note_off", note=60, velocity=0, time=.1)
]
audio = instrument(midi_messages, duration=.2, sample_rate=sample_rate)

# Apply effects to this audio (if any):
effected = board(audio, sample_rate)

# Define the output file path
output_file_path = 'output.wav'

# Open an audio file to write to:
with AudioFile(output_file_path, 'w', sample_rate, effected.shape[0], bit_depth=16) as o:
    o.write(effected)

print("Audio processing complete. Output saved as 'output.wav'.")

# Open the folder containing the output file in Windows Explorer
output_folder = os.path.dirname(os.path.abspath(output_file_path))
os.startfile(output_folder)

