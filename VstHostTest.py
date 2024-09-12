import os
import platform
from pedalboard import Pedalboard, load_plugin
from pedalboard.io import AudioFile
from mido import Message

# Get the path of the assets folder relative to the script
assets_folder = os.path.join(os.path.dirname(__file__), 'assets')

# Determine the correct plugin path based on the operating system
if platform.system() == "Windows":
    plugin_path = os.path.join(assets_folder, 'blocks.vst3/Contents/x86_64-win/blocks.vst3')
elif platform.system() == "Darwin":
    plugin_path = os.path.join(assets_folder, 'blocks.vst3/Contents/MacOS/blocks.vst3')
else:
    raise OSError("Unsupported operating system. This script only supports Windows and MacOS.")

# Load a VST3 or Audio Unit plugin(s) from the assets folder
try:
    instrument1 = load_plugin(plugin_path)
    assert instrument1.is_instrument
except ImportError as e:
    raise ImportError(f"Failed to load plugin: {e}")

# Set a specific instrument within the VST plugin by loading a preset from the assets folder
instrument1.load_preset(os.path.join(assets_folder, 'snare0.vstpreset'))

# Make a plain old pedalboard with no effects:
board = Pedalboard()

# Render some audio by passing MIDI to an instrument:
sample_rate = 44100
midi_messages = [
    Message("note_on", note=60, velocity=64, time=0),
    Message("note_off", note=60, velocity=0, time=.1)
]
audio = instrument1(midi_messages, duration=.2, sample_rate=sample_rate)

# Apply effects to this audio (if any):
effected = board(audio, sample_rate)

# Define the output file path
output_file_path = 'output.wav'

# Open an audio file to write to:
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
