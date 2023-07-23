import streamlit as st
import ast
from classes.Song import Song
from annotated_text import annotated_text, annotation


# A colour mapping to get colours working in Streamlit annotated text
colour_mapping = {'o' : 'orange',
                 'p' : 'purple',
                 'g' : 'green',
                 'r' : 'red',
                 'y' : 'yellow',
                 'b' : 'blue'}

def process_user_input_to_dictionary(user_input):
    """
    Takes the user's input over multiple lines and creates the appropriate format ready for processing and chord colouring

    Example
    Cmaj7 Dmin7 Emin7
    Amaj9/#11

    Example output
    {'Section 1' : ['Cmaj7', 'Dmin7', 'Emin7'],
     'Section 2' : ['Amaj9/#11']}
    """
    # Split the users input into each line
    user_input_split_per_line = user_input.splitlines()
    
    # Convert each line into a list of chords
    lists_of_chords = [chords_in_line.split() for chords_in_line in user_input_split_per_line]

    # Take each list of chords and store them in a dictionary, each key is a section for the song
    processed_input_as_dictionary = {
        'Section ' + str(section_number + 1): collection_of_bars 
        for section_number, collection_of_bars in enumerate(lists_of_chords)
    }

    return processed_input_as_dictionary


def get_top_border_colour(chord_colour, first_extension_colour):
    """
    Get the correct top border colour. If there is no first extension colour then default to the chord's colour
    """
    if first_extension_colour == '':
        return f'6px solid {colour_mapping[chord_colour]}'
    else:
        return f'6px solid {colour_mapping[first_extension_colour]}'


def get_bottom_border_colour(chord_colour, second_extension_colour):
    """
    Get the correct bottom border colour. If there is no second extension colour then default to the chord's colour
    """
    if second_extension_colour == '':
        return f'6px solid {colour_mapping[chord_colour]}'
    else:
        return f'6px solid {colour_mapping[second_extension_colour]}'


def get_right_border_colour(chord_colour, third_extension_colour):
    """
    Get the correct right border colour. If there is no third extension colour then default to the chord's colour
    """
    if third_extension_colour == '':
        return f'6px solid {colour_mapping[chord_colour]}'
    else:
        return f'6px solid {colour_mapping[third_extension_colour]}'


# App header
st.title('Meta Harmony Crayon Box 🖍️')

# Example input
st.subheader("Here's an example input")
st.code("""
        Cmaj7 Emin Dmin Ddom7
        Cmaj7 Dmin Gdom7/#9
        Amin Gmin7 Dmin9
        """, language = 'python')


# Get the user input 
st.subheader('Input the composition of the track and hit "Ctrl+Enter or Cmd+Enter" to colour the chords')
song = st.text_area("user input", label_visibility = 'hidden')


# Once the input is done and Enter is hit, output the song with Meta Harmony colours
if song is not None:
    
    try:
        # Take the user's input and perform clean up on it
        s = Song(song_name = '', 
                 artist_name = '', 
                 song_structure_and_chords = process_user_input_to_dictionary(song))
    except ValueError:
        st.error("The chord format isn't correct or the input isn't appropriate. It must match the above example.")

    # Get the part names of the song
    part_names = [part.name for part in s.parts]

    # For each part show the chords using Meta Harmony colours
    for part_name, chords, colours_of_chords in zip(part_names, s.get_chords(), s.get_chord_colours()):
        
        # Output part name
        f"## {part_name}"
        
        # Get the colours of the chord
        chord_main_colours = [chord[0] for chord in colours_of_chords]
        first_extension_colours = [chord[1] for chord in colours_of_chords]
        second_extension_colours = [chord[2] for chord in colours_of_chords]
        third_extension_colours = [chord[3] for chord in colours_of_chords]

        # Create a block of text to represent the chords in the part
        chords_as_text = []
        
        # Loop through each chord in the part and it's colours and display them appropriately
        for (chord, chord_colour, first_extension_colour, 
             second_extension_colour, third_extension_colour) in zip(chords, chord_main_colours, 
                                                                     first_extension_colours, second_extension_colours, third_extension_colours):
            chords_as_text.append(annotation(chord, 
                                             '', 
                                             font_family = 'Arial', 
                                             background = colour_mapping[chord_colour], 
                                             border_top = get_top_border_colour(chord_colour, first_extension_colour),
                                             border_bottom = get_bottom_border_colour(chord_colour, second_extension_colour),
                                             border_right = get_right_border_colour(chord_colour, third_extension_colour),
                                             color = 'white'))
        
        annotated_text(chords_as_text)