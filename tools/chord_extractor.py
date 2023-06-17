from langchain.tools import tool

@tool
def chord_extractor(uncleaned_chord_sheet_data : list) -> dict:
    """Takes the uncleaned_chord_sheet_data and extracts the chords to each part of the song and stores each part e.g. verse, chorus, bridge into a dictionary"""

    cleaned_song = {}
    key_counts = {}

    for item in uncleaned_chord_sheet_data:
        if item.startswith('['):
            # Extract the key between square brackets
            current_key = item[1:-1]

            # Check if a part of the song exists already exists
            if current_key in cleaned_song:
                # Increment the count for the key
                key_counts[current_key] += 1
                current_key = f"{current_key}_{key_counts[current_key]}"
            else:
                key_counts[current_key] = 0
                
            cleaned_song[current_key] = []

        elif current_key is not None and item:
            cleaned_song[current_key].append(item)

    return cleaned_song