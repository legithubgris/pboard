import os
import platform
from pedalboard import Pedalboard, load_plugin
from pedalboard.io import AudioFile
from mido import MidiFile, Message

# Get the path of the assets folder relative to the script
assets_folder = os.path.join(os.path.dirname(__file__), 'assets')

# Load a VST3 or Audio Unit plugin(s) from the assets folder
instrument1 = load_plugin(os.path.join(assets_folder, 'blocks.vst3/Contents/x86_64-win/blocks.vst3'))
assert instrument1.is_instrument

instrument2 = load_plugin(os.path.join(assets_folder, 'blocks.vst3/Contents/x86_64-win/blocks.vst3'))
assert instrument2.is_instrument

instrument3 = load_plugin(os.path.join(assets_folder, 'blocks.vst3/Contents/x86_64-win/blocks.vst3'))
assert instrument3.is_instrument

# Set a specific instrument within the VST plugin by loading a preset from the assets folder
instrument1.load_preset(os.path.join(assets_folder, 'clappy.vstpreset'))
instrument2.load_preset(os.path.join(assets_folder, 'snare0.vstpreset'))
instrument3.load_preset(os.path.join(assets_folder, 'kicky.vstpreset'))

# Rest of the code remains unchanged
board = Pedalboard()
midi_file_path = os.path.join(assets_folder, 'OpenSaurceVSTTest.mid')
midi = MidiFile(midi_file_path)
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
        continue

    if combined_audio is None:
        combined_audio = audio
    else:
        combined_audio += audio

effected = board(combined_audio, sample_rate)
output_file_path = 'output.wav'

with AudioFile(output_file_path, 'w', sample_rate, effected.shape[0], bit_depth=16) as o:
    o.write(effected)

print("Audio processing complete. Output saved as 'output.wav'.")

output_folder = os.path.dirname(os.path.abspath(output_file_path))

if platform.system() == "Windows":
    os.startfile(output_folder)
elif platform.system() == "Darwin":
    os.system(f"open {output_folder}")
else:
    print("Unsupported operating system. Cannot open file explorer.")

input("Press Enter to close the window")
