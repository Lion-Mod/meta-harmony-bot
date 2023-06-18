from PIL import Image, ImageDraw

# Define the colors corresponding to the strings
color_mapping = {
    'p': (128, 0, 128),  # Purple
    'g': (0, 255, 0),  # Green
    'o': (255, 165, 0),  # Orange
    'r': (255, 0, 0),  # Red
    'b': (0, 0, 255),  # Blue
    'y': (255, 255, 0)  # Yellow
}


def create_image_from_dictionary(secondary_colours, extension_colours):
    """
    Creates an image of a song's chords with the appropriate meta harmony colours
    """
    image_width = 300 * 3
    image_height = 300 * len(secondary_colours)

    # Create a new image with a white background
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    # Create squares for each chord and colour it with the secondary colour appropriately
    y = 0
    section_count = 0
    for _, values in secondary_colours.items():
        x = 0
        num_of_chords = len(values)
  
        for value in values:

            # Get the chord colour (if not know then default to black)
            color = color_mapping.get(value, (0, 0, 0))
            
            x_offset = x * 50
            
            draw.rectangle((x_offset, y, x_offset + 50, y + 50), fill = color)
            
            x += 1
            
            # When reached 4 chords increase y and reset x 
            if x % 4 == 0 or x == num_of_chords:
                y += 50
                x = 0
        
        y += 100
        section_count += 1


    # Do the same thing but for extension colours
    y = 0
    section_count = 0
    for _, values in extension_colours.items():
        x = 0
        num_of_chords = len(values)

        for value in values:

            # Get the extension colour (if not know then default to black)
            color = color_mapping.get(value, (0, 0, 0))
            
            x_offset = x * 50
            
            # If no extension then don't draw a rectangle, otherwise draw one of the appropriate colour in the top left of the secondary chord colour
            # Example : orange rectangle with red rectangle is an orange chord with red extension
            if value == '':
                pass
            else:
                draw.rectangle((x_offset, y, x_offset + 12.5, y + 12.5), fill = color)
            
            x += 1
            
            if x % 4 == 0 or x == num_of_chords:
                y += 50
                x = 0
        
        y += 100
        section_count += 1

    return image

