from youtube_transcript_api import YouTubeTranscriptApi
import os
import nagisa
import re
import webbrowser

video_link = "https://www.youtube.com/watch?v=p_hC2CApcf0"
video_id = video_link.split("=")[1]
file_name = "parsedsubtitles/"+video_id+".txt"

# Take subtitles from the video and put them into a local txt (only if it doesn't already exist)
if(not os.path.isfile(file_name)):
    print("Subtitles not found for video, retrieving them now...")
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript(['ja']).fetch()

    text = ""

    with open("parsedsubtitles/"+video_id+".txt","w",encoding="utf-8") as f:
        for line in transcript:
            f.write(line['text']+" "+str(line['start'])+" "+str(line['duration'])+"\n") 
    print("Subtitles retrieved")

# Pull all excluded words from the different sources
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


# Collect subtitles from the file
sentences = []
with open(file_name,"r",encoding="utf-8") as f:
    for line in f:
        sentence = line.split(" ")[0]
        sentences.append(sentence)

# Split sentences into individual words and then add them to a map, keeping track of how many times the word appears
words = []
for sen in sentences:
    words.extend([word for word in nagisa.tagging(sen).words])
word_count = {}
for word in words:
    word_count[word] = word_count.setdefault(word,0)+1

# Sort words by most frequent first
word_freq_dict = dict(sorted(word_count.items(),key=lambda a: a[1],reverse=True))

# Remove excluded words from the list
for word in excluded_words:
    word_freq_dict.pop(word, "")

# Add katakana-words to unimportantwords.txt and also remove them from the list of words
r = re.compile(u'[\u30a0-\u30ff\uff00-\uff9f]*')
katakana = []
for word in word_freq_dict.keys():
    if(bool(r.fullmatch(word))):
        katakana.append(word)
with open("unimportantwords.txt","a",encoding="utf-8") as f:
    if(len(katakana)!=0):
        for word in katakana:
            f.write("\n"+word)
            word_freq_dict.pop(word, "")

# List of the words, no duplicates, in order by frequency, subscriptable
word_freq_list = []
for word in word_freq_dict.keys():
    word_freq_list.append(word)

# Collects a number of the top words as chosen by the user
mined_word_count = int(input("How many of the top words would you like to choose? "))
chosen_words = []
for index, word in enumerate(word_freq_list):
    if(index==mined_word_count-1):
        chosen_words.append(word)
    elif(index<mined_word_count):
        chosen_words.append(word)
    else:
        break

# collect first sentence where the word occurs
chosen_words_sentences = []
for word in chosen_words:
    for sen in sentences:
        if re.search(word,sen):
            chosen_words_sentences.append(sen)
            break



print("Beginning user prompting, type help to list available commands")
endProgram = False
# ------- Begining of loop --------------
while(not endProgram):

    text = ""
    for index, word in enumerate(chosen_words):
        if(index==len(chosen_words)-1):
            text += "["+str(index)+"]"+word
        else:
            text += "["+str(index)+"]"+word+", "
    print("\nCurrent words: "+text)

    choice = input("What would you like to do? ").split(" ")
    action = choice[0]

    # Adds xth word to blacklist.txt
    if(action == "axe"):
        word_index = int(choice[1])
        word = chosen_words[word_index]
        with open("blacklist.txt","a",encoding="utf-8") as f:
            f.write("\n"+word)
        chosen_words.pop(word_index)
        new_word = word_freq_list[mined_word_count]
        mined_word_count +=1
        chosen_words.append(new_word)

    # Adds xth word to knownwords.txt
    elif(action == "know"):
        word_index = int(choice[1])
        word = chosen_words[word_index]
        with open("knownwords.txt","a",encoding="utf-8") as f:
            f.write("\n"+word)
        chosen_words.pop(word_index)
        new_word = word_freq_list[mined_word_count]
        mined_word_count +=1
        chosen_words.append(new_word)

    # Lists available commands and other information that is relevant to using the program
    elif(action == "help"):
        print("All commands to select a specific xth word is 0 indexed")
        print("Available commands:\n(unimplemented)anki: creates anki cards of current words\naxe x: adds xth word to blacklist.txt")
        print("def x/all: opens xth word's jisho link or all words jisho links\nend: terminates program\nknow x: adds xth word to knownwords.txt")
        print("sen: show sentences attached to words\nsen x: shows all sentences where xth word appears\n? x: adds xth word to questionablewords.txt")
    
    # If no selected words, opens jisho link for all words, otherwise opens only jisho link for xth word
    elif(action == "def"):
        if(len(choice)==1):
            for word in chosen_words:
                webbrowser.open("https://jisho.org/search/"+word)
        else:
            word_index = int(choice[1])
            word = chosen_words[word_index]
            webbrowser.open("https://jisho.org/search/"+word)
    
    # If no selected word, lists current sentences for each word, otherwise lists all sentences for xth word allowing user to pick desired sentence for the word
    elif(action == "sen"):
        # Lists current sentences for each word
        if(len(choice)==1):
            for index, sen in enumerate(chosen_words_sentences):
                print("\n"+chosen_words[index]+": "+sen)
        # Lists all sentences for xth word
        else:
            word_index = int(choice[1])
            word = chosen_words[word_index]
            specific_word_sen = []
            print("\n"+word+":")
            for index,sen in enumerate(sentences):
                if re.search(word,sen):
                    specific_word_sen.append(sen)
            for index,sen in enumerate(specific_word_sen):
                if(sen==chosen_words_sentences[word_index]):
                    print("["+str(index)+"]"+sen+" (Current Sentence)")
                else:
                    print("["+str(index)+"]"+sen)
            choice2 = input("Would you like to change the selected sentence for "+word+" to xth sentence above? (y x/n): ").split(" ")
            if(choice2[0]=="y"):
                index = int(choice2[1])
                selected_sen = specific_word_sen[index]
                chosen_words_sentences[word_index] = selected_sen
                print("Sentence for "+word+" changed to: "+selected_sen)
    
    # Adds xth word to questionablewords.txt
    elif(action == "?"):
        word_index = int(choice[1])
        word = chosen_words[word_index]
        with open("questionablewords.txt","a",encoding="utf-8") as f:
            f.write("\n"+word)
        chosen_words.pop(word_index)
        new_word = word_freq_list[mined_word_count]
        mined_word_count +=1
        chosen_words.append(new_word)
    
    # Terminates the program
    elif(action == "end"):
        endProgram = True
    
    # Catchall if the user mistypes a command or types a command that doesn't exist
    else:
        print("Sorry check that you didn't mispell the command and try again")

# ------------- End of loop --------------------