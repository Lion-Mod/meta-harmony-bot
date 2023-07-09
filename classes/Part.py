from classes.ColouredChord import ColouredChord

class Part():
    """
    Represents a musical part consisting of ColouredChords.

    It creates a list of ColouredChord objects based on the provided raw chords and stores the name of the part e.g. 'intro'.

    Attributes:
        name (str): The name of the musical part e.g. 'intro'
        raw_chords (list): A list of raw chord names for the part.

    Properties:
        coloured_chords (list): A list of ColouredChord objects created from the raw chord names.
    """
    def __init__(self, name, raw_chords):
        self.name = name
        self.coloured_chords = [ColouredChord(raw_chord) for raw_chord in raw_chords]


    def __repr__(self):
        return(f"""
               {self.name} chords:
               {self.coloured_chords}
                """)