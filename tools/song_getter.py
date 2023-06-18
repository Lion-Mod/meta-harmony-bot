from functions.chord_data_processers import *
from langchain.tools import tool
from typing import Dict


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