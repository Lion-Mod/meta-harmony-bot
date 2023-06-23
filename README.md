# Meta Harmony Bot

## TLDR of what it does
1. Get some chords to a song by an artist / band
2. Colour the chords and extensions using MetaHarmony principles
3. Output coloured chords and extensions

## Uses
1. Understand if there are common types of voice leading in a song
2. See if certain artists / bands use common chord movements

## Example
```python
from tools.song_getter import *

chords = song_getter.func(song_name = 'just the way you are', artist_name = 'bruno mars')
print(chords)

{'song': [('F', 'maj', 'g', '', '', ''),
  ('D', 'min', 'g', '', '', ''),
  ('A#', 'maj', 'p', '', '', ''),
  ('F', 'maj', 'g', '', '', ''),
  ('D', 'min', 'g', '', '', ''),
  ('A#', 'maj', 'p', '', '', ''),
  ('F', 'maj', 'g', '', '', ''),
  ('F', 'maj', 'g', '', '', ''),
  ('D', 'min', 'g', '', '', ''),
  ('A#', 'maj', 'p', '', '', ''),
  ('F', 'maj', 'g', '', '', ''),
  ('F', 'maj', 'g', '', '', ''),
  ('D', 'min', 'g', '', '', ''),
  ('A#', 'maj', 'p', '', '', ''),
  ('F', 'maj', 'g', '', '', ''),
  ('F', 'maj', 'g', '', '', ''),
  ('D', 'min', 'g', '', '', ''),
  ('A#', 'maj', 'p', '', '', ''),
  ('F', 'maj', 'g', '', '', '')]}
```

## Todos
* Get data cleanup to be able to handle inversions
* More colouring - sus chords, min7b5 chords, other extensions?
* Identify most likely key of each section of the song is
* Identify most likely mode each section of the song is
* Visualise the coloured chords in an interactive web app
* Get the coloured chords to format correctly based upon chord length e.g. 1 bar, 2 bars...
