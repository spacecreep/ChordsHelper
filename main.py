import customtkinter as ctk
from chords import generate_chord, CHROMATIC_SCALE, CHORD_TYPES
import pygame  # For sound playback
import random
import time

class ChordApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load note sounds
        self.note_sounds = self.load_note_sounds()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set window size as a percentage of the screen size
        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.3)
        self.geometry(f"{window_width}x{window_height}")
        self.title("Chord Notes Generator")
        self.resizable(False, False)

        # Title label
        self.title_label = ctk.CTkLabel(
            self, text="Chord Notes Generator", font=("Arial", int(window_height * 0.05))
        )
        self.title_label.pack(pady=int(window_height * 0.02))

        # Randomize button (top-right)
        self.randomize_button = ctk.CTkButton(
            self, text="Randomize", command=self.randomize_chord, font=("Arial", int(window_height * 0.03))
        )
        self.randomize_button.place(x=window_width - 110, y=10)  # Position the button at top-right

        # Dropdown for root notes
        self.root_label = ctk.CTkLabel(
            self, text="Select Root Note:", font=("Arial", int(window_height * 0.03))
        )
        self.root_label.pack(pady=(int(window_height * 0.01), 0))

        self.root_var = ctk.StringVar()
        self.root_dropdown = ctk.CTkOptionMenu(
            self, values=CHROMATIC_SCALE, variable=self.root_var, command=self.update_chord
        )
        self.root_dropdown.pack(pady=int(window_height * 0.01))

        # Dropdown for chord types
        self.type_label = ctk.CTkLabel(
            self, text="Select Chord Variation:", font=("Arial", int(window_height * 0.03))
        )
        self.type_label.pack(pady=(int(window_height * 0.01), 0))

        self.type_var = ctk.StringVar()
        self.type_dropdown = ctk.CTkOptionMenu(
            self, values=list(CHORD_TYPES.keys()), variable=self.type_var, command=self.update_chord
        )
        self.type_dropdown.pack(pady=int(window_height * 0.01))

        # Result label
        self.result_label = ctk.CTkLabel(
            self, text="", font=("Arial", int(window_height * 0.03))
        )
        self.result_label.pack(pady=int(window_height * 0.02))

        # Piano frame
        self.piano_frame_width = int(window_width * 0.5)
        self.piano_frame_height = int(window_height * 0.2)
        self.piano_frame = ctk.CTkFrame(
            self, width=self.piano_frame_width, height=self.piano_frame_height
        )
        self.piano_frame.pack(pady=int(window_height * 0.03))

        self.create_piano()

        # Volume slider
        self.volume_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=1,
            orientation="vertical",
            number_of_steps=100,
            command=self.change_volume,
            height=int(window_height * 0.2),  # Set slider height
        )
        self.volume_slider.set(0.5)  # Default volume
        self.volume_slider.place(x=self.piano_frame.winfo_rootx() + 10, y=self.piano_frame.winfo_rooty())  # Position slider next to piano

        # Play chord button
        self.play_chord_button = ctk.CTkButton(
            self,
            text="Play Chord",
            command=self.play_all_notes,
            font=("Arial", int(window_height * 0.03)),
        )
        self.play_chord_button.pack(pady=int(window_height * 0.02))

        # To store current chord notes
        self.current_chord_notes = []

    def load_note_sounds(self):
        """Load sounds for each note and return a dictionary."""
        notes = [
            "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
        ]
        note_sounds = {}
        for note in notes:
            try:
                note_sounds[note] = pygame.mixer.Sound(f"Sounds/Chords/Piano/{note}.wav")  # Replace 'sounds/' with your directory
            except pygame.error:
                print(f"Warning: Could not load sound for {note}.")
        return note_sounds

    def play_note_sound(self, note):
        """Play the sound corresponding to the given note."""
        if note in self.note_sounds:
            self.note_sounds[note].play()

    def play_all_notes(self):
        """Play all the notes of the current chord simultaneously."""
        # Disable the "Play Chord" button to prevent playing while sounds are playing
        self.play_chord_button.configure(state="disabled")

        # Play all notes in the chord
        for note in self.current_chord_notes:
            self.play_note_sound(note)

        # Wait for all sounds to finish before enabling the button again
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event when music finishes
        while pygame.mixer.get_busy():  # Wait until sound is playing
            self.update_idletasks()  # Ensure the GUI is still responsive
            time.sleep(0.1)  # Prevent locking up the interface

        # Enable the "Play Chord" button again
        self.play_chord_button.configure(state="normal")

    def create_piano(self):
        # Create keys dynamically based on frame dimensions
        self.keys = {}
        white_keys = ["C", "D", "E", "F", "G", "A", "B"]
        black_keys = {"C": "C#", "D": "D#", "F": "F#", "G": "G#", "A": "A#"}

        white_key_width = self.piano_frame_width // len(white_keys)
        white_key_height = self.piano_frame_height

        black_key_width = int(white_key_width * 0.6)
        black_key_height = int(white_key_height * 0.6)

        # Create white keys
        for i, note in enumerate(white_keys):
            key = ctk.CTkButton(
                self.piano_frame,
                width=white_key_width,
                height=white_key_height,
                text=note,
                corner_radius=0,
                fg_color="white",
                text_color="black",
                command=lambda n=note: self.play_note_sound(n),  # Play sound on click
            )
            key.place(x=i * white_key_width, y=0)
            self.keys[note] = key

        # Create black keys
        for i, (white_note, black_note) in enumerate(black_keys.items()):
            if white_note in white_keys[:-1]:
                key = ctk.CTkButton(
                    self.piano_frame,
                    width=black_key_width,
                    height=black_key_height,
                    text=black_note,
                    corner_radius=0,
                    fg_color="black",
                    text_color="white",
                    command=lambda n=black_note: self.play_note_sound(n),  # Play sound on click
                )
                key.place(
                    x=int((white_keys.index(white_note) + 0.7) * white_key_width),
                    y=0,
                )
                self.keys[black_note] = key

    def update_chord(self, _=None):
        root = self.root_var.get()
        chord_type = self.type_var.get()

        # Reset key colors
        for key, button in self.keys.items():
            if key in ["C", "D", "E", "F", "G", "A", "B"]:  # White keys
                button.configure(fg_color="white", text_color="black")
            else:  # Black keys
                button.configure(fg_color="black", text_color="white")

        if not root or not chord_type:
            self.result_label.configure(text="Please select both a root note and a chord type.")
            return

        try:
            notes = generate_chord(root, chord_type)
            self.current_chord_notes = notes  # Save the current chord notes
            self.result_label.configure(text=f"Notes: {', '.join(notes)}")

            # Highlight notes on the piano
            for note in notes:
                if note in self.keys:
                    self.keys[note].configure(fg_color="yellow", text_color="black")
        except ValueError as e:
            self.result_label.configure(text=str(e))

    def randomize_chord(self):
        """Randomly select a root note and chord type."""
        root = random.choice(CHROMATIC_SCALE)
        chord_type = random.choice(list(CHORD_TYPES.keys()))

        # Update the dropdowns to reflect the random values
        self.root_var.set(root)
        self.type_var.set(chord_type)

        # Trigger the chord update
        self.update_chord()

    def change_volume(self, value):
        """Change the volume based on the slider position."""
        volume = float(value)
        pygame.mixer.music.set_volume(volume)  # Adjust master volume
        for sound in self.note_sounds.values():
            sound.set_volume(volume)  # Set volume for each note sound



# Run the application
if __name__ == "__main__":
    app = ChordApp()
    app.mainloop()

