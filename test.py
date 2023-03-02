import re
print(re.sub(r"(?:(?![\n\r])(\s)\1{1,})", "", """All commands to select a specific xth word is 0 indexed
        Available commands:\n(unimplemented)anki: creates anki cards of current words\naxe x: adds xth word to blacklist.txt
        def x/all: opens xth word's jisho link or all words jisho links\nend: terminates program\nknow x: adds xth word to knownwords.txt
        sen: show sentences attached to words\nsen x: shows all sentences where xth word appears\n? x: adds xth word to questionablewords.txt
        """))
