import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from typing import Dict

headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' }

@tool
def song_getter(url : str) -> Dict:
    """Uses the url to get the non processed chord sheet and then processes it"""
    
    # Check if url exists, if not then raise error
    response = requests.get(url, headers = headers)

    if response.status_code != 200:
        raise AssertionError("The url requested wasn't available.")
    else:
        pass


    # Get the chord sheet data
    html_chord_sheet = BeautifulSoup(response.text, 'html.parser').find("pre", class_ = "chord_sheet")

    # Pull out all chords or sections of songs e.g. verse, chorus, bridge from the html and store as a list
    # Example output : ["verse", "Cmaj", "Dmaj", "chorus", "Gmaj", ...]
    extracted_chords_and_sections = html_chord_sheet.find_all('span', class_ = lambda c: c and (c.startswith('c') or c.startswith('l ss')))

    unclean_chord_sheet_data = []
    for content in extracted_chords_and_sections:
        unclean_chord_sheet_data.append(content.text)


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

    return cleaned_song
