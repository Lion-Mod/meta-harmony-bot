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


def create_image_from_dictionary(chord_main_colours, first_extension_colours, second_extension_colours):
    """
    Creates an image of a song's chords with the appropriate meta harmony colours
    """
    image_width = 150 * 3
    image_height = 100 * len(chord_main_colours)
    square_width = 25

    # Create a new image with a white background that the coloured chords will be drawn on
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    # Initialise y and section number to assist with correct formatting
    y = 0
    section_number = 0

    # Create squares for each section's chords and colour it with the secondary colour appropriately
    for coloured_sections in zip(chord_main_colours.items(), first_extension_colours.items(), second_extension_colours.items()):

        # Get the secondary, first extension and second extension colours
        chord_main_colours = coloured_sections[0][1]
        first_extension_colours = coloured_sections[1][1]
        second_extension_colours = coloured_sections[2][1]
  
        # The 3 variables below ensure chords are drawn correctly
        chord_number_in_section = 0
        section_number += 1
        number_of_chords_in_sections = len(chord_main_colours)

        # Output each chord's colours as a square one at a time
        for chord_main_colour, first_extension_colour, second_extension_colour in zip(chord_main_colours, first_extension_colours, second_extension_colours):

            # Set the correct x origin
            x_origin = (chord_number_in_section % 4) * square_width

            # Get the chord RGB colour (if not know then default to black) and draw the chord as a square
            chord_main_colour = color_mapping.get(chord_main_colour, (0, 0, 0))
            draw.rectangle((x_origin, y, x_origin + square_width, y + square_width), fill = chord_main_colour)
            
            # Do the same for first extension only if they exist and draw extensions as smaller squares in the chord square
            if first_extension_colour == '':
                pass
            else:
                first_extension_colour = color_mapping.get(first_extension_colour, (0, 0, 0))
                draw.rectangle((x_origin, y, x_origin + square_width / 4, y + square_width / 4), fill = first_extension_colour)

            # Same thing as the first extension but with any second extensions if they exist
            if second_extension_colour == '':
                pass
            else:
                second_extension_colour = color_mapping.get(second_extension_colour, (0, 0, 0))
                draw.rectangle((x_origin + square_width / 4, y, x_origin + square_width / 2, y + square_width / 4), fill = second_extension_colour)

            # Add one to the chord counter to ensure formatting of chords being drawn is correct
            chord_number_in_section += 1
            
            # When 4 chords have been drawn increase y (new line) and reset chord_number_in_section i.e. new line of chords
            if (chord_number_in_section % 4 == 0 and chord_number_in_section != 0) or (number_of_chords_in_sections == chord_number_in_section):
                y += square_width

        # After each section of the song reset the y to create a gap
        y += square_width

    return image

