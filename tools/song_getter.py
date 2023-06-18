import requests
import re
from fastcore.foundation import *
from bs4 import BeautifulSoup
from langchain.tools import tool
from typing import Dict

headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' }

# The corresponding secondary colour of each chord
# o = orange
# p = purple
# g = green
chord2colour = {'Cmaj' : 'o',
                'C#maj' : 'p',
                'Dmaj' : 'g',
                'D#maj' : 'o',
                'Emaj' : 'p',
                'Fmaj' : 'g',
                'F#maj' : 'o',
                'Gmaj' : 'p',
                'G#maj' : 'g',
                'Amaj' : 'o',
                'A#maj' : 'p',
                'Bmaj' : 'g',
                'Cmin' : 'o',
                'C#min' : 'p',
                'Dmin' : 'g',
                'D#min' : 'o',
                'Emin' : 'p',
                'Fmin' : 'g',
                'F#min' : 'o',
                'Gmin' : 'p',
                'G#min' : 'g',
                'Amin' : 'o',
                'A#min' : 'p',
                'Bmin' : 'g',
                'Cdom' : 'o',
                'C#dom' : 'p',
                'Ddom' : 'g',
                'D#dom' : 'o',
                'Edom' : 'p',
                'Fdom' : 'g',
                'F#dom' : 'o',
                'Gdom' : 'p',
                'G#dom' : 'g',
                'Adom' : 'o',
                'A#dom' : 'p',
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

    # Pull out all chords or sections of songs e.g. verse, chorus, bridge from the html and store as a list
    # Example output : ["verse", "Cmaj", "Dmaj", "chorus", "Gmaj", ...]
    extracted_chords_and_sections = L(html_chord_sheet.find_all('span', class_ = lambda c: c and (c.startswith('c') or c.startswith('l ss'))))

    unclean_chord_sheet_data = L()
    for content in extracted_chords_and_sections:
        unclean_chord_sheet_data.append(content.text)

    return unclean_chord_sheet_data


def reword_unclean_chord_name(chord : str):
    """
    Takes a string in and performs some clean up / rewording given unclean data can contain inconsistent chord naming or the chord colourer needs a better format
    Example : 'C' should be 'Cmaj', 'C7' becomes 'Cdom7'
    """
    if len(chord) == 1 and chord.isupper():
        chord = chord + "maj"
    elif len(chord) >= 2 and chord[0].isupper():
        if chord[1:] == "m" or chord[1:] == "m7":
            chord = chord.replace("m", "min")
        elif chord[1] == "7":
            chord = chord[0] + "dom7"
    return chord


def get_colours_of_chords_and_extensions(chord : str):
  """
  Get the colour of the chord and it's extensions
  """
  # Get info about the chord
  root = re.search(r'[A-Z]#?', chord).group(0)
  chord_quality = re.search(r'min|maj|dom', chord).group(0)
  extensions = re.search(r'(add9|7|add1|b6)', chord)

  # Assign the appropriate colours
  # - Chord colour (secondary colour)
  chord_colour = chord2colour[root+chord_quality]
  
  # - Extension colour (primary colour)
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


@tool
def song_getter(song_name : str, artist_name : str) -> Dict:
    """Creates a url using the song_name and artist_name to get the non processed chord sheet and then processes it and colours it"""
    url = url_creator(song_name = song_name, artist_name = artist_name)

    unclean_chord_sheet_data = get_unclean_chord_data(url)
    
    # Reword unclean chord names
    unclean_chord_sheet_data = unclean_chord_sheet_data.map(reword_unclean_chord_name)
        
    # Below reformats the data into a dictionary
    # Example output : {"Verse" : ["Cmaj", "Dmaj", "Gmaj"], "Chorus", ["Gmaj", "Amin"]}
    cleaned_song = {}
    key_counts = {}

    for item in unclean_chord_sheet_data:
        if item.startswith('['):
            # Extract the song section string (the string between the square brackets)
            current_song_section = item[1:-1]

            # Check if a song section already exists in the dictionary, if it does add a number after it to distinguish other sections
            # Example : chorus, chorus_1, chorus_2
            if current_song_section in cleaned_song:
                key_counts[current_song_section] += 1
                current_song_section = f"{current_song_section}_{key_counts[current_song_section]}"
            else:
                key_counts[current_song_section] = 0
                
            cleaned_song[current_song_section] = []

        elif current_song_section is not None and item:
            cleaned_song[current_song_section].append(item)

    cleaned_song = {section: [get_colours_of_chords_and_extensions(chord) for chord in chords_in_section] for section, chords_in_section in cleaned_song.items()}

    return cleaned_song