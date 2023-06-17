import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' }

@tool
def chord_sheet_getter(url : str) -> list:
    """Uses the url to get the unclean chord sheet data"""
    response = requests.get(url, headers = headers)

    # Create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the chord sheet data
    chord_sheet = soup.find("pre", class_ = "chord_sheet")

    # Pull out all chords or parts of songs e.g. verse, chorus, bridge from the html
    extracted_chords_and_parts = chord_sheet.find_all('span', class_=lambda c: c and (c.startswith('c') or c.startswith('l ss')))

    unclean_chord_sheet_data = []
    for content in extracted_chords_and_parts:
        unclean_chord_sheet_data.append(content.text)

    return unclean_chord_sheet_data
