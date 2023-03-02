import pysubs2
import nagisa
import re

excluded_words = []
with open('blacklist.txt',encoding='utf-8') as black_list:
    excluded_words = [line.strip() for line in black_list.readlines()]
with open('knownwords.txt',encoding='utf-8') as knownwords_list:
    excluded_words.extend([line.strip() for line in knownwords_list.readlines()])
with open('unimportantwords.txt',encoding='utf-8') as unimportantwords_list:
    excluded_words.extend([line.strip() for line in unimportantwords_list.readlines()])
excluded_words.append("\u3000")
excluded_words.append("\n")

filename = "rawsubtitles\Gundam the Witch from Mercury\Mobile.Suit.Gundam.The.Witch.From.Mercury.S01E02.WEBRip.Netflix.ja[cc].srt"
subs = pysubs2.load(filename, encoding="utf-8")

text = ""
for line in subs:
    text += line.plaintext+" "

words = nagisa.tagging(text)
word_list = words.words
word_count = {}
for word in word_list:
    word_count[word] = word_count.setdefault(word,0)+1;

word_freq_dict = dict(sorted(word_count.items(),key=lambda a: a[1],reverse=True))
for word in excluded_words:
    word_freq_dict.pop(word, "")

word_freq_list = word_freq_dict.keys()

print(word_freq_list)
print(len(word_freq_list))

r = re.compile(u'[\u30a0-\u30ff\uff00-\uff9f]*')

katakana = []
for word in word_freq_list:
    if(bool(r.fullmatch(word))):
        katakana.append(word)

with open("unimportantwords.txt","a",encoding="utf-8") as f:
    if(len(katakana)!=0):
        for word in katakana:
            f.write("\n"+word)