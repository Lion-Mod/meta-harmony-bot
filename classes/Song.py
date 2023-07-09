from classes.Part import Part

class Song():
    def __init__(self, song_name, artist_name, song_structure_and_chords):
        self.song_name = song_name
        self.artist_name = artist_name
        self.parts = [Part(name = part_name, raw_chords = chords_of_part) for part_name, chords_of_part in song_structure_and_chords.items()]
