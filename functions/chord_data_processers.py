import requests
import re
import ast
from fastcore.foundation import *
from bs4 import BeautifulSoup

headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' }


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
        
        if part.startswith("[") or (len(part) < 8 and part != ""):
            unclean_chord_sheet_data.append(part)
        else:
            pass

    return unclean_chord_sheet_data


def structure_unclean_chord_data(unclean_chord_sheet_data):
    """
    Take the unclean_chord_sheet_data and structure it nicely in a dictionary ready for processing    
    
    Example output : {"Verse" : ["Cmaj", "Dmaj", "Gmaj"], "Chorus", ["Gmaj", "Amin"]}
    """
    structured_song = {}
    key_counts = {}
    current_song_section = None

    # If no first element with [] around it create the first element so the dictionary works below
    if unclean_chord_sheet_data[0].startswith('[') == False:
        unclean_chord_sheet_data.insert(0, "[song]")
    else:
        pass

    for item in unclean_chord_sheet_data:
        if item.startswith('['):
            # Extract the song section string (the string between the square brackets)
            current_song_section = item[1:-1]

            # Check if a song section already exists in the dictionary, if it does add a number after it to distinguish other sections
            # Example : chorus, chorus_1, chorus_2
            if current_song_section in structured_song:
                key_counts[current_song_section] += 1
                current_song_section = f"{current_song_section}_{key_counts[current_song_section]}"
            else:
                key_counts[current_song_section] = 0
                
            structured_song[current_song_section] = []

        elif current_song_section is not None and item:
            structured_song[current_song_section].append(item)

    structured_song = {section: [chord for chord in chords_in_section] for section, chords_in_section in structured_song.items()}

    return structured_song


def string_to_dictionary(llm_output):
    """
    Transform the llm output into a dictionary. This is needed as the llm output currently is a string not an actual dictionary
    """
    # Remove leading/trailing speech marks
    llm_output = llm_output.strip()

    # Convert the string to a dictionary using ast.literal_eval()
    output_dictionary = ast.literal_eval(llm_output)

    return output_dictionary