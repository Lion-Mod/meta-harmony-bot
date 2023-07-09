from classes.ColouredChord import ColouredChord

class Part():
    def __init__(self, name, raw_chords):
        self.name = name
        self.coloured_chords = [ColouredChord(raw_chord) for raw_chord in raw_chords]

    def __repr__(self):
        return(f"""
               {self.name} chords:
               {self.coloured_chords}
                """)