import requests
import re
import ast
from fastcore.foundation import *
from bs4 import BeautifulSoup

headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' }

# The corresponding secondary colour of each chord
# o = orange
# p = purple
# g = green
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
                'Bdom' : 'g'}


# The extension type for each extension
# This isn't all of them, just a start
# c = complimentary
extension2extension_type = {'add9' : 'c',
                            'b9' : 'common or syntonic?',
                            '7' : 'c',
                            'add11' : 'c',
                            'b6' : 'c'}


# The appropriate complimentary colour for each secondary colour
complimentary2colour = {'o' : 'b',
                        'g' : 'r',
                        'p' : 'y'}


def url_creator(song_name : str, artist_name : str):
    """Gets the url from chordbook to extract chords from"""
    return f'https://www.mychordbook.com/chords/{artist_name.lower().replace(" ", "-")}/{song_name.lower().replace(" ","-")}'


def get_unclean_chord_data(url : str):
    """
    Gets the unclean chord data as a list of strings
    Example : ['verse', 'Cm', 'C', 'Dmaj', 'chorus', 'D']
    """

   # Check if url exists, if not then raise error
    response = requests.get(url, headers = headers)

    if response.status_code != 200:
        raise AssertionError("The requested url wasn't available.")
    else:
        pass

    # Get the chord sheet data
    html_chord_sheet = BeautifulSoup(response.text, 'html.parser').find("pre", class_ = "chord_sheet")

    # Pull all details from the webpage
    extracted_webpage_data = L(html_chord_sheet.find_all('span', class_ = lambda c: c and (c.startswith('c') or 
                                                                                           c.startswith('l'))))

    # Remove errorneous data from the page and keep chords and chord sections
    unclean_chord_sheet_data = L()
    for content in extracted_webpage_data:
        
        part = re.sub(r'^\d+$', '', content.text)
        
        if part.startswith("[") or (len(part) < 6 and part != ""):
            unclean_chord_sheet_data.append(part)
        else:
            pass

    return unclean_chord_sheet_data


def reword_unclean_chord_name(chord : str):
    """
    Takes a string in and performs some clean up / rewording given unclean data can contain inconsistent chord naming or the chord colourer needs a better format
    Example : 'C' should be 'Cmaj', 'C7' becomes 'Cdom7', 'Bb' should be 'Bbmaj'
    """

    # If it's a song part then leave it alone
    if chord.startswith("["):
        return chord
    
    # Otherwise perform chord cleanup
    else:
        root_note = re.findall(r'[A-G][b#]?', chord)[0]
        chord_type = chord.replace(root_note, "")

        if chord_type == "":
            return root_note + "maj"
        elif chord_type in ["min7", "maj7"]:
            return chord
        elif chord_type == "m":
            return root_note + "min"
        elif chord_type == "m7":
            return root_note + "min7"
        elif chord_type == "7":
            return root_note + "dom7"
        else:
            return chord


def get_colours_of_chords_and_extensions(chord : str):
    """
    Get the colour of the chord and it's extensions
    """
    # Get root of the chord
    root = re.search(r'[A-Z][b#]?', chord).group(0)

    # Get the chord quality (if any)
    chord_quality = re.search(r'min|maj|dom', chord)

    if chord_quality is None:
        AssertionError('No chord quality detected')
    else:
        chord_quality = chord_quality.group(0)


    # Assign the appropriate colours
    # - Chord colour (secondary colour)
    chord_colour = chord2colour[root+chord_quality]

    # - Extension colour (primary colour)  
    extensions = re.search(r'(add9|7|add1|b6)', chord)

    if extensions is None: 
        extension = ""
        extension_type = ""
        extension_colour = ""

    else: 
        # Might need a loop here to go through all extensions. This currently only does one extension
        extension = extensions.group(0)
        extension_type = extension2extension_type[extension]
        
        if extension_type == 'c':
            extension_colour = complimentary2colour[chord_colour]
        else:
            extension_colour = None

    return root, chord_quality, chord_colour, extension, extension_type, extension_colour


def string_to_dictionary(llm_output):
    """
    Transform the llm output into a dictionary. This is needed as the llm output currently is a string not an actual dictionary
    """
    # Remove leading/trailing speech marks
    llm_output = llm_output.strip()

    # Convert the string to a dictionary using ast.literal_eval()
    output_dictionary = ast.literal_eval(llm_output)

    return output_dictionary