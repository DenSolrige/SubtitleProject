from ankisync2 import AnkiDesktop

filepath = r"1.0.0-collection.anki2"
# AnkiDesktop.backup(filepath)
anki = AnkiDesktop(filepath)
words = []
for row in anki.db.database.execute_sql("select notes.flds,cards.ivl from cards inner join notes on cards.nid = notes.id where ivl > 0 and cards.did = 1674942306548 order by cards.id"):
    word = row[0].split("\x1f")[1] + (" M" if row[1]>=21 else " L")
    words.append(word)
with open("./vocab/core2k.txt","w",encoding="utf-8") as f:
    f.write("\n".join(words))   
# AnkiDesktop.restore(filepath)