import itertools

# Define the chromatic scale
CHROMATIC_SCALE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Define chord intervals in semitones
CHORD_TYPES = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "augmented": [0, 4, 8],
    "major7": [0, 4, 7, 11],
    "minor7": [0, 3, 7, 10],
    "dominant7": [0, 4, 7, 10],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "add9": [0, 4, 7, 14],
    "minor9": [0, 3, 7, 10, 14],
    "major9": [0, 4, 7, 11, 14],
    "minor11": [0, 3, 7, 10, 14, 17],
    "major11": [0, 4, 7, 11, 14, 17],
    "13": [0, 4, 7, 10, 14, 21],
    "minor13": [0, 3, 7, 10, 14, 21],
    "dim7": [0, 3, 6, 9],
    "half-diminished7": [0, 3, 6, 10]
}

# Helper function to get a note from the scale
def get_note_from_scale(note, semitone_offset):
    index = (CHROMATIC_SCALE.index(note) + semitone_offset) % len(CHROMATIC_SCALE)
    return CHROMATIC_SCALE[index]

# Function to generate a chord
def generate_chord(root, chord_type):
    root = root.upper()  # Ensure root note is uppercase
    if root not in CHROMATIC_SCALE:
        raise ValueError(f"Invalid root note: {root}. Choose from {CHROMATIC_SCALE}.")
    if chord_type not in CHORD_TYPES:
        raise ValueError(f"Invalid chord type: {chord_type}. Choose from {list(CHORD_TYPES.keys())}.")

    intervals = CHORD_TYPES[chord_type]
    chord_notes = [get_note_from_scale(root, interval) for interval in intervals]
    return chord_notes

# Main program
def main():
    print("Welcome to the Chord Notes Generator!")
    print("Available notes: ", ", ".join(CHROMATIC_SCALE))
    print("Available chord types: ", ", ".join(CHORD_TYPES.keys()))

    root = input("Enter the root note of the chord (e.g., A, C#, G): ").strip()
    chord_type = input("Enter the chord type (e.g., major, minor7, sus4): ").strip()

    try:
        chord_notes = generate_chord(root, chord_type)
        print(f"The notes in the {root} {chord_type} chord are: {', '.join(chord_notes)}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
