import nagisa
import re

excluded_words = []
with open('blacklist.txt',encoding='utf-8') as black_list:
    excluded_words = [line.strip() for line in black_list.readlines()]
with open('knownwords.txt',encoding='utf-8') as knownwords_list:
    excluded_words.extend([line.strip() for line in knownwords_list.readlines()])
with open('unimportantwords.txt',encoding='utf-8') as unimportantwords_list:
    excluded_words.extend([line.strip() for line in unimportantwords_list.readlines()])
with open('questionablewords.txt',encoding='utf-8') as questionablewords_list:
    excluded_words.extend([line.strip() for line in questionablewords_list.readlines()])
excluded_words.append("\u3000")
excluded_words.append("\n")

video_link = "https://www.youtube.com/watch?v=zUeAG7VcgjE"
video_id = video_link.split("=")[1]
file_name = "parsedsubtitles/"+video_id+".txt"

text = ""
with open("parsedsubtitles/"+video_id+".txt","r",encoding="utf-8") as f:
    for line in f:
        text += line.split(" ")[0]

words = nagisa.tagging(text)
word_list = words.words
word_count = {}
for word in word_list:
    word_count[word] = word_count.setdefault(word,0)+1;

word_freq_dict = dict(sorted(word_count.items(),key=lambda a: a[1],reverse=True))
for word in excluded_words:
    word_freq_dict.pop(word, "")

word_freq_list = word_freq_dict.keys()

for word in word_freq_list:
    print(word + " frequency: "+ str(word_freq_dict[word]))

# print(word_freq_list)
# print(len(word_freq_list))

r = re.compile(u'[\u30a0-\u30ff\uff00-\uff9f]*')

katakana = []
for word in word_freq_list:
    if(bool(r.fullmatch(word))):
        katakana.append(word)

with open("unimportantwords.txt","a",encoding="utf-8") as f:
    if(len(katakana)!=0):
        for word in katakana:
            f.write("\n"+word)


mined_word_count = int(input("How many of the top words would you like to choose? "))
text = ""
for index, word in enumerate(word_freq_list):
    if(index==mined_word_count-1):
        text += word
    elif(index<mined_word_count):
        text += word+", "
    else:
        break

print(text)
choice = input("Would you like to add these words to the minedcontent.txt file? (y/n): ")
if(choice == "y"):
    with open("minedcontent.txt","a",encoding="utf-8") as f:
        f.write("\n"+video_link+"\n"+text)