from classes.Part import Part
from PIL import Image, ImageDraw


# Define the colors corresponding to the strings
color_mapping = {
    'p': (128, 0, 128),  # Purple
    'g': (0, 255, 0),    # Green
    'o': (255, 165, 0),  # Orange
    'r': (255, 0, 0),    # Red
    'b': (0, 0, 255),    # Blue
    'y': (255, 255, 0)   # Yellow
}


class Song():
    def __init__(self, song_name, artist_name, song_structure_and_chords):
        self.song_name = song_name
        self.artist_name = artist_name
        self.parts = [Part(name = part_name, raw_chords = chords_of_part) for part_name, chords_of_part in song_structure_and_chords.items()]        

    def get_chord_colours(self):
        """
        Get all the chord colours (and any extension colours) for each part e.g. ['o', 'o', 'o', 'o'] is a part of a song with 4 orange chords
        """
        song_chord_colours = []

        for p in self.parts:
        
            part_chord_colours = []
            
            for c in p.coloured_chords:
                part_chord_colours.append([c.chord_colour, c.extension_one_colour, c.extension_two_colour, c.extension_three_colour])
            
            song_chord_colours.append(part_chord_colours)
        
        return song_chord_colours

    def create_coloured_chords_image(self):
        """
        Creates an image of a song's chords with the appropriate meta harmony colours
        """
        song_chord_colours = self.get_chord_colours()

        image_width = 150 * 3
        image_height = 50 * max(len(part_chord_colours) for part_chord_colours in song_chord_colours)
        square_width = 25

        # Create a new image with a white background that the coloured chords will be drawn on
        image = Image.new('RGB', (image_width, image_height), 'white')
        draw = ImageDraw.Draw(image)

        # Initialise y and section number to assist with correct formatting
        y = 0
        section_number = 0

        # Create squares for each section's chords and colour it with the secondary colour appropriately
        for coloured_section in song_chord_colours:

            # Get the main chord colour and the extension colours
            chord_main_colours = [chord[0] for chord in coloured_section]
            first_extension_colours = [chord[1] for chord in coloured_section]
            second_extension_colours = [chord[2] for chord in coloured_section]
            third_extension_colours = [chord[3] for chord in coloured_section]
    
            # The 3 variables below ensure chords are drawn correctly
            chord_number_in_section = 0
            section_number += 1
            number_of_chords_in_sections = len(coloured_section)

            # Output each chord's colours as a square one at a time
            for (chord_main_colour, first_extension_colour, 
                second_extension_colour, third_extension_colour) in zip(chord_main_colours, first_extension_colours, 
                                                                        second_extension_colours, third_extension_colours):

                # Set the correct x origin
                x_origin = (chord_number_in_section % 4) * square_width

                # Get the chord RGB colour (if not know then default to black) and draw the chord as a square
                chord_main_colour = color_mapping.get(chord_main_colour, (0, 0, 0))
                draw.rectangle((x_origin, y, x_origin + square_width, y + square_width), fill = chord_main_colour)
                
                # Add the colours of the extensions (if applicable) as a smaller rectangle within the main chord's square
                for i, extension_colour in enumerate([first_extension_colour, second_extension_colour, third_extension_colour], start = 1):
                    if extension_colour != '':
                        extension_colour = color_mapping.get(extension_colour, (0, 0, 0))
                        draw.rectangle((x_origin + square_width * (i - 1) / 3, y,
                                        x_origin + square_width * i / 3, y + square_width / 4), fill = extension_colour)
                    else:
                        AssertionError(f'Colouring extensions failed on extension number {i}')

                # Add one to the chord counter to ensure formatting of chords being drawn is correct
                chord_number_in_section += 1
                
                # When 4 chords have been drawn increase y (new line) and reset chord_number_in_section i.e. new line of chords
                if (chord_number_in_section % 4 == 0 and chord_number_in_section != 0) or (number_of_chords_in_sections == chord_number_in_section):
                    y += square_width

            # After each section of the song reset the y to create a gap
            y += square_width

        return image