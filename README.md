#  Meta Harmony Crayon Box 🟨🟥🟦🟧🟩🟪

## TLDR of what it does
1. Input chords to a piece of music OR get some chords to a song by an artist / band (if they're available)
2. The crayon box colours the chords and extensions using Meta Harmony
3. The newly coloured chords and extensions (where applicable) are outputted

## What is Meta Harmony?
[This video has a good high level run through of it](https://www.youtube.com/watch?v=qjR13Jz7YYw)

Come to the [Discord](https://discord.gg/nwHRsgbx) to find out more!

## Uses of the crayon box
1. Understand if there are common types of voice leading in a song
2. See if certain artists, bands or genres use common chord movements


## Todos
* ~~Get data cleanup to be able to handle inversions~~
* ~~More colouring - sus chords, min7b5 chords, other extensions?~~
* ~~Handle dominant 9th, 11ths etc~~
* ~~Handle chords w/ 3 extensions e.g. Fdom9/#11 (this has dominant extension, 9th and #11 i.e. yellow, red and blue extensions)~~
* ~~Make ColouredChords objects~~
* ~~Make Part objects (each part consists of ColouredChords)~~
* ~~Make Song object (each Song is made up of Parts, each Part is make up of ColouredChords)~~
* ~~Rework coloured image generator into Song~~
* ~~Identify most likely major key of each section of the song is~~
* ~~Make basic app~~

* Identify most likely key of each section of the song is
* Identify most likely mode each section of the song is

* Basic reharm, you enter key cube you're in (this determines alphacube and chord functions) and state to reharm to a mode e.g C lydian (shift SD up)
* Do the above but for an entire section e.g. change the intro to be xxx
(Don't affect chords not in the key e.g. Cmajor key, there's a Bb chord, leave it)

* Get the coloured chords to format correctly based upon chord length e.g. 1 bar, 2 bars...
* Feedbacker? Rates your composition? WTF would this be?! Maybe an analyser? Detects common trends?
