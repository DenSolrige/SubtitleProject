# Language Learning Tool
main.py runs the command line tool
test.py and test2.py are for testing certain lines in isolation

The tool pulls subtitles from a given video from YouTubeTranscriptApi and saves them locally, where it is split into individual sentences and subsequently into words, sorted by frequency. These words are then filtered by removing known and blacklisted words. 
The user is then prompted for how many of the most common words they wish to see from the video and then the words are paired with the first sentence in the video in which they appear.
The user can then perform commands allowing them to blacklist words, remove already known words, open the definition for a selected word, and look at and change the sentence for one or all words.