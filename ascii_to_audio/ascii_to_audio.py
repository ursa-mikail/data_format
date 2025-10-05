#!pip install music21
from music21 import stream, note, tempo, clef
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Audio, display, FileLink

def ascii_to_audio(ascii_text, mapping_type='auto', base_note='C4', tempo=120):
    """
    Convert ASCII text/art to audio melody
    
    Parameters:
    - ascii_text: ASCII string or art
    - mapping_type: 'auto', 'height', 'binary', 'char_value'
    - base_note: Starting note ('C4')
    - tempo: Beats per minute
    
    Returns:
    - Audio player and sequence info
    """
    
    # Note frequencies (4th octave and up)
    note_frequencies = {
        'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
        'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
        'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
        'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
        'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
        'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,
        'C6': 1046.50
    }
    
    note_names = list(note_frequencies.keys())
    
    def char_to_note(char, method, base_idx):
        """Convert character to musical note"""
        if method == 'height':
            # Use character height in line (for ASCII art)
            return note_names[min(base_idx + (ord(char) % 12), len(note_names)-1)]
        
        elif method == 'binary':
            # Use character ASCII value mod number of notes
            ascii_val = ord(char)
            note_idx = (ascii_val + base_idx) % len(note_names)
            return note_names[note_idx]
        
        elif method == 'char_value':
            # Direct mapping from character frequency
            if char.isalpha():
                char_num = ord(char.upper()) - ord('A')
                note_idx = (char_num + base_idx) % len(note_names)
                return note_names[note_idx]
            elif char.isdigit():
                note_idx = (int(char) + base_idx) % len(note_names)
                return note_names[note_idx]
            else:
                # Punctuation/symbols map to base note
                return note_names[base_idx]
        
        else:  # 'auto'
            # Smart mapping based on character type
            if char.isupper():
                char_num = ord(char) - ord('A')
                return note_names[(char_num + 12) % len(note_names)]  # Higher notes
            elif char.islower():
                char_num = ord(char) - ord('a')
                return note_names[(char_num + base_idx) % len(note_names)]
            elif char.isdigit():
                return note_names[(int(char) + 7) % len(note_names)]
            else:
                # Symbols get random but consistent notes
                symbol_hash = hash(char) % 8
                return note_names[(symbol_hash + base_idx) % len(note_names)]
    
    # Find base note index
    base_idx = note_names.index(base_note) if base_note in note_names else 0
    
    # Process ASCII text
    lines = ascii_text.split('\n')
    note_sequence = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            for char in line:
                if char != ' ':  # Skip spaces
                    note = char_to_note(char, mapping_type, base_idx)
                    note_sequence.append(note)
            # Add a pause between lines
            note_sequence.append('REST')
    
    # Remove consecutive rests
    filtered_sequence = []
    for note in note_sequence:
        if note != 'REST' or (filtered_sequence and filtered_sequence[-1] != 'REST'):
            filtered_sequence.append(note)
    
    # Generate audio
    sample_rate = 44100
    note_duration = 60 / tempo  # seconds per beat
    audio_data = np.array([])
    
    for note in filtered_sequence:
        if note == 'REST':
            # Add silence
            silence = np.zeros(int(0.2 * sample_rate))  # Short rest
            audio_data = np.concatenate([audio_data, silence])
        else:
            # Generate note
            freq = note_frequencies[note]
            t = np.linspace(0, note_duration, int(sample_rate * note_duration))
            
            # Create rich tone with harmonics
            fundamental = 0.5 * np.sin(2 * np.pi * freq * t)
            harmonic1 = 0.3 * np.sin(2 * np.pi * freq * 2 * t)
            harmonic2 = 0.2 * np.sin(2 * np.pi * freq * 3 * t)
            
            note_wave = fundamental + harmonic1 + harmonic2
            
            # Apply envelope
            attack = int(0.1 * len(t))
            release = int(0.2 * len(t))
            envelope = np.ones_like(note_wave)
            envelope[:attack] = np.linspace(0, 1, attack)
            envelope[-release:] = np.linspace(1, 0, release)
            
            note_wave *= envelope
            audio_data = np.concatenate([audio_data, note_wave])
    
    # Normalize audio
    if len(audio_data) > 0:
        audio_data = audio_data / np.max(np.abs(audio_data))
    
    return audio_data, sample_rate, filtered_sequence

def advanced_ascii_to_audio(ascii_text, 
                           mapping_type='auto',
                           base_note='C4', 
                           tempo=120):
    """
    Advanced ASCII to audio converter that returns both audio and note sequence
    """
    # Convert and get both audio and sequence
    audio_data, sample_rate, note_sequence = ascii_to_audio(ascii_text, mapping_type, base_note, tempo)
    
    # Filter out REST notes for the musical sequence
    musical_sequence = [n for n in note_sequence if n != 'REST']
    
    # Display results
    print(f"📊 Conversion Results:")
    print(f"   Input: '{ascii_text}'")
    print(f"   Mapping: {mapping_type}")
    print(f"   Base Note: {base_note}")
    print(f"   Tempo: {tempo} BPM")
    print(f"   Sequence: {' → '.join(musical_sequence)}")
    
    # Return both the audio object and the note sequence
    return Audio(audio_data, rate=sample_rate, autoplay=False), musical_sequence

# Test the advanced version
print("🎛️ Advanced ASCII to Audio")
print("=" * 50)

test_text = 'neurai-AI'
# Get both audio and sequence
audio_obj, note_sequence = advanced_ascii_to_audio(test_text, mapping_type='vowel', tempo=100)

# Display the audio
print("\n🔊 Playing audio:")
display(audio_obj)

# Now create music21 stream with the actual note sequence
print("\n🎵 Creating music21 stream...")
s = stream.Stream()
s.append(clef.TrebleClef())

# Add notes to the stream (using the actual note sequence, not the audio object)
for n in note_sequence:
    s.append(note.Note(n, quarterLength=1))

# Set the tempo
s.insert(0, tempo.MetronomeMark(number=120))

# Save as MIDI
s.write('midi', 'neurai.mid')
print("✅ MIDI file saved as 'neurai.mid'")

# Create a piano roll visualization
def create_piano_roll_visualization(sequence):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Note to position mapping
    note_order = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    note_height = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
    
    x_positions = range(len(sequence))
    
    for i, note_str in enumerate(sequence):
        # Handle sharp notes (like C#4)
        if '#' in note_str:
            pitch_class = note_str[:2]  # e.g., 'C#'
            octave = int(note_str[2])   # e.g., 4
        else:
            pitch_class = note_str[0]   # e.g., 'C'
            octave = int(note_str[1])   # e.g., 4
        
        # Calculate vertical position
        base_height = note_height.get(pitch_class[0], 0)  # Get base height for letter
        total_height = base_height + (octave - 4) * 7
        
        # Plot the note
        color = plt.cm.Set3(i / len(sequence))  # Different colors for each note
        ax.bar(i, 1, bottom=total_height, width=0.8, 
               color=color, edgecolor='black', alpha=0.8)
        
        # Add note label
        ax.text(i, total_height + 0.5, note_str, 
                ha='center', va='center', fontweight='bold', fontsize=10)
    
    ax.set_xlabel('Note Position')
    ax.set_ylabel('Pitch Height')
    ax.set_title(f'Neurai Melody: {" → ".join(sequence)}')
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f'Pos {i+1}' for i in x_positions])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Create visualization
print("\n📊 Creating piano roll visualization...")
create_piano_roll_visualization(note_sequence)

# Also print the sequence
print(f"\n🎼 Musical Sequence: {' → '.join(note_sequence)}")

# Create download link
print("\n📥 Download links:")
display(FileLink('neurai.mid', result_html_prefix="Download MIDI file: "))

print("\n🎵 Trying to convert MIDI to WAV for direct playback...")

# Try to play using different methods
try:
    # Convert MIDI to WAV using fluidsynth
    print("Installing fluidsynth...")
    !apt-get install -y fluidsynth fluid-soundfont-gm > /dev/null 2>&1
    print("Converting MIDI to WAV...")
    !fluidsynth -F neurai.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 neurai.mid > /dev/null 2>&1
    
    print("✅ Playing converted WAV audio:")
    display(Audio('neurai.wav'))
    
except Exception as e:
    print(f"❌ Couldn't convert MIDI to WAV: {e}")
    print("But the MIDI file was created successfully! Download and play it locally.")

print("\n" + "="*50)
print("🎹 Summary:")
print(f"   Input text: '{test_text}'")
print(f"   Generated melody: {' → '.join(note_sequence)}")
print(f"   MIDI file: 'neurai.mid'")
print(f"   Audio length: {len(note_sequence)} notes")
print("="*50)

"""
🎛️ Advanced ASCII to Audio
==================================================
📊 Conversion Results:
   Input: 'neurai-AI'
   Mapping: vowel
   Base Note: C4
   Tempo: 100 BPM
   Sequence: C#5 → E4 → G#5 → F5 → C4 → G#4 → C4 → C5 → G#5

🔊 Playing audio:

🎵 Creating music21 stream...
✅ MIDI file saved as 'neurai.mid'

📊 Creating piano roll visualization...


🎼 Musical Sequence: C#5 → E4 → G#5 → F5 → C4 → G#4 → C4 → C5 → G#5

📥 Download links:
Download MIDI file: neurai.mid

🎵 Trying to convert MIDI to WAV for direct playback...
Installing fluidsynth...
Converting MIDI to WAV...
✅ Playing converted WAV audio:

==================================================
🎹 Summary:
   Input text: 'neurai-AI'
   Generated melody: C#5 → E4 → G#5 → F5 → C4 → G#4 → C4 → C5 → G#5
   MIDI file: 'neurai.mid'
   Audio length: 9 notes
==================================================
"""