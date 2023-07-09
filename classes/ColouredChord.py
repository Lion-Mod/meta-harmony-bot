import re

# The corresponding secondary colour of each chord
# o = orange
# p = purple
# g = green
# y = yellow
# r = red
# b = blue
chord2colour = {'Cmaj' : 'o',
                'C#maj' : 'p',
                'Dbmaj' : 'p',
                'Dmaj' : 'g',
                'D#maj' : 'o',
                'Ebmaj' : 'o',
                'Emaj' : 'p',
                'Fmaj' : 'g',
                'F#maj' : 'o',
                'Gbmaj' : 'o',
                'Gmaj' : 'p',
                'G#maj' : 'g',
                'Abmaj' : 'g',
                'Amaj' : 'o',
                'A#maj' : 'p',
                'Bbmaj' : 'p',
                'Bmaj' : 'g',
                
                'Cmin' : 'o',
                'C#min' : 'p',
                'Dbmin' : 'p',
                'Dmin' : 'g',
                'D#min' : 'o',
                'Ebmin' : 'o',
                'Emin' : 'p',
                'Fmin' : 'g',
                'F#min' : 'o',
                'Gbmin' : 'o',
                'Gmin' : 'p',
                'G#min' : 'g',
                'Abmin' : 'g',
                'Amin' : 'o',
                'A#min' : 'p',
                'Bbmin' : 'p',
                'Bmin' : 'g',

                'Cmaj7' : 'o',
                'C#maj7' : 'p',
                'Dbmaj7' : 'p',
                'Dmaj7' : 'g',
                'D#maj7' : 'o',
                'Ebmaj7' : 'o',
                'Emaj7' : 'p',
                'Fmaj7' : 'g',
                'F#maj7' : 'o',
                'Gbmaj7' : 'o',
                'Gmaj7' : 'p',
                'G#maj7' : 'g',
                'Abmaj7' : 'g',
                'Amaj7' : 'o',
                'A#maj7' : 'p',
                'Bbmaj7' : 'p',
                'Bmaj7' : 'g',
                
                'Cmin7' : 'o',
                'C#min7' : 'p',
                'Dbmin7' : 'p',
                'Dmin7' : 'g',
                'D#min7' : 'o',
                'Ebmin7' : 'o',
                'Emin7' : 'p',
                'Fmin7' : 'g',
                'F#min7' : 'o',
                'Gbmin7' : 'o',
                'Gmin7' : 'p',
                'G#min7' : 'g',
                'Abmin7' : 'g',
                'Amin7' : 'o',
                'A#min7' : 'p',
                'Bbmin7' : 'p',
                'Bmin7' : 'g',

                'Csus' : 'o',
                'C#sus' : 'p',
                'Dbsus' : 'p',
                'Dsus' : 'g',
                'D#sus' : 'o',
                'Ebsus' : 'o',
                'Esus' : 'p',
                'Fsus' : 'g',
                'F#sus' : 'o',
                'Gbsus' : 'o',
                'Gsus' : 'p',
                'G#sus' : 'g',
                'Absus' : 'g',
                'Asus' : 'o',
                'A#sus' : 'p',
                'Bbsus' : 'p',
                'Bsus' : 'g',

                'Cdom' : 'o',
                'C#dom' : 'p',
                'Dbdom' : 'p',
                'Ddom' : 'g',
                'D#dom' : 'o',
                'Ebdom' : 'o',
                'Edom' : 'p',
                'Fdom' : 'g',
                'F#dom' : 'o',
                'Gbdom' : 'o',
                'Gdom' : 'p',
                'G#dom' : 'g',
                'Abdom' : 'g',
                'Adom' : 'o',
                'A#dom' : 'p',
                'Bbdom' : 'p',
                'Bdom' : 'g',
                
                'Cdim' : 'y',
                'C#dim' : 'r',
                'Dbdim' : 'r',
                'Ddim' : 'b',
                'D#dim' : 'y',
                'Ebdim' : 'y',
                'Edim' : 'r',
                'Fdim' : 'b',
                'F#dim' : 'y',
                'Gbdim' : 'y',
                'Gdim' : 'r',
                'G#dim' : 'b',
                'Abdim' : 'b',
                'Adim' : 'y',
                'A#dim' : 'r',
                'Bbdim' : 'r',
                'Bdim' : 'b'}


# The extension type for each extension
# Some chords e.g. Fdom11 are considered their own 
extension2extension_type = {'b5' : 'syntonic',
                            'b6' : 'complimentary',
                            '9' : 'complimentary',
                            'b9' : 'syntonic',
                            '#9' : 'common',
                            'b11' : 'syntonic',
                            '11' : 'complimentary',
                            '#11' : 'common',
                            'b13' : 'syntonic',
                            '13' : 'complimentary',
                            'min6' : 'common',
                            'dom' : 'syntonic',
                            'min7b5' : 'common',
                            'sus2' : 'complimentary',
                            'sus4' : 'complimentary'}


# The appropriate complimentary colour for each secondary colour
# b = blue
# r = red
# y = yellow
complimentary2colour = {'o' : 'b',
                        'g' : 'r',
                        'p' : 'y'}


# The appropriate syntonic colour for each secondary colour
syntonic2colour = {'o' : 'r',
                   'g' : 'y',
                   'p' : 'b'}


# The appropriate common cadence colour for each secondary colour
common2colour = {'o' : 'y',
                 'g' : 'b',
                 'p' : 'r'}


class ColouredChord():
    def __init__(self, raw_chord):  
        self.raw_chord = raw_chord; assert type(self.raw_chord) == str
        self.chord = self.reword_unclean_chord_name()
        self.root_note = self.get_root_note()
        self.bass_note = self.get_bass_note()
        self.chord_quality = self.get_chord_quality()
        self.chord_colour = self.get_chord_colour()
        (self.extension_one, self.extension_one_type, self.extension_one_colour, 
         self.extension_two, self.extension_two_type, self.extension_two_colour,
         self.extension_three, self.extension_three_type, self.extension_three_colour) = self.get_extensions()

    def __repr__(self):
        return (f"""
                Raw chord = {self.raw_chord}
                Chord = {self.chord}
                Root note = {self.root_note}
                Bass note = {self.bass_note}
                Chord quality = {self.chord_quality}
                Chord colour = {self.chord_colour}
                Chord extension 1 = {self.extension_one}, {self.extension_one_type}, {self.extension_one_colour}
                Chord extension 2 = {self.extension_two}, {self.extension_two_type}, {self.extension_two_colour}
                Chord extension 3 = {self.extension_three}, {self.extension_three_type}, {self.extension_three_colour}
                """)

    def reword_unclean_chord_name(self):
        """
        Takes a string in and performs some clean up / rewording given unclean data can contain inconsistent chord naming or the chord colourer needs a better format
        Example : 'C' should be 'Cmaj', 'C7' becomes 'Cdom7', 'Bb' should be 'Bbmaj'
        """        
        # Pull out the root note and chord type from the raw chord
        root_note = re.findall(r'[A-G][b#]?', self.raw_chord)[0]
        chord_type = self.raw_chord.replace(root_note, "")
        

        # Handle any inversions
        if "/" in chord_type:
            chord_parts = chord_type.split("/")
            chord_type = chord_parts[0]
            bass_note = chord_parts[1]

            # Adjust chord and bass note if necessary
            if chord_type == "":
                chord_type += "maj"
            elif chord_type in ["min7", "maj7", "min", "maj"]:
                pass
            elif chord_type == "m":
                chord_type = 'min'
            elif chord_type == "m7":
                chord_type = 'min7'
            elif chord_type == "m7b5":
                chord_type = 'min7b5'
            elif chord_type == "7":
                chord_type = 'dom7'

            return root_note + chord_type + "/" + bass_note


        # Handle standard chords (no inversions)
        if chord_type == "":
            return root_note + "maj"
        elif chord_type in ["min7", "maj7", "min", "maj"]:
            return root_note + chord_type
        elif chord_type == "m":
            return root_note + "min"
        elif chord_type == "m7":
            return root_note + "min7"
        elif chord_type == "m7b5":
            return root_note + 'min7b5'
        elif chord_type == "7":
            return root_note + "dom7"

        else:
            return self.raw_chord

    def get_root_note(self):
        """
        Get root note of the chord
        """
        root_note = re.search(r'[A-G][b#]?', self.chord)
        
        if root_note is None:
            AssertionError('No root note detected')
        else:
            root_note = root_note.group(0)

        return root_note

    def get_bass_note(self):  
        """
        Get bass note if the chord is an inversion
        """
        bass_note = re.search(r'/[A-G][b#]?', self.chord)

        if bass_note is None:
            bass_note = "No bass note"
        else:
            bass_note = bass_note.group(0)

        return bass_note

    def get_chord_quality(self):
        """
        Get the chord quality (if it matches the below chord qualities)
        """
        chord_quality = re.search(r'min[7]?|maj[7]?|sus|dom|dim', self.chord)

        if chord_quality is None:
            AssertionError('No chord quality detected')
        else:
            chord_quality = chord_quality.group(0)

        return chord_quality

    def get_chord_colour(self):
        """
        Get the appropriate chord colour (secondary colour unless it's a diminished chord)
        """
        return chord2colour[self.root_note + self.chord_quality]

    def get_extensions(self):
        """
        Get the extensions, their type and their colour (if extensions are there), the max expected is 3
        """
        # Regex out the extensions (if they're there)
        extension_pattern = "(b5|b6|min6|min7b5|dom|sus[2|4]+|[b#]?9|[b#]?11|[b]?13)"
        extensions = re.findall(extension_pattern, self.chord)

        extension_info = []

        # Get the colour of each extension
        for extension in extensions:
            extension_type = extension2extension_type.get(extension)
            if extension_type is not None:
                if extension_type == 'complimentary':
                    extension_colour = complimentary2colour.get(self.chord_colour)
                elif extension_type == 'syntonic':
                    extension_colour = syntonic2colour.get(self.chord_colour)
                elif extension_type == 'common':
                    extension_colour = common2colour.get(self.chord_colour)
                else:
                    extension_colour = None

                extension_info.append((extension, extension_type, extension_colour))

        # Pull out each extensions information (what the extension is, the "type" of extension, the colour of it)
        extension_one, extension_one_type, extension_one_colour = extension_info[0] if extension_info else ("", "", "")
        extension_two, extension_two_type, extension_two_colour = extension_info[1] if len(extension_info) > 1 else ("", "", "")
        extension_three, extension_three_type, extension_three_colour = extension_info[2] if len(extension_info) > 2 else ("", "", "")

        return (extension_one, extension_one_type, extension_one_colour, 
                extension_two, extension_two_type, extension_two_colour,
                extension_three, extension_three_type, extension_three_colour)

    def get_colours(self):
        """
        Pulls only the chord, the chord colour and the extension colours
        """
        return (self.chord, self.chord_colour, self.extension_one_colour, self.extension_two_colour, self.extension_three_colour)