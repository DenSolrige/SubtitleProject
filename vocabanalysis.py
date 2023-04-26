import colorama
from colorama import Fore, init

init()

with open('./vocab/core2k.txt',encoding='utf-8') as file:
    core2k = [line.strip().split(" ") for line in file.readlines()]

def compareToCurrentVocab(str):
    with open(f'./vocab/{str}.txt',encoding='utf-8') as file:
        vocab = [line.strip().split(" ")[0] for line in file.readlines()]
    mature = 0
    learning = 0
    wordcount = len(vocab)
    name = str
    for word1 in vocab:
        for word2 in core2k:
            if word1 == word2[0]:
                if word2[1] == 'M':
                    mature += 1
                else:
                    learning += 1
    return {'mature':mature, 'learning':learning, 'wordcount':wordcount, 'name':name}

def compare2Vocabs(str1,str2):
    with open(f'./vocab/{str1}.txt',encoding='utf-8') as file:
        vocab1 = [line.strip().split(" ")[0] for line in file.readlines()]
    with open(f'./vocab/{str2}.txt',encoding='utf-8') as file:
        vocab2 = [line.strip().split(" ")[0] for line in file.readlines()]

    sharedwords = 0
    name1 = str1
    name2 = str2
    for word1 in vocab1:
        for word2 in vocab2:
            if word1 == word2:
                sharedwords += 1
    vocab1words = len(vocab1)-sharedwords
    vocab2words = len(vocab2)-sharedwords
    wordcount = vocab1words+vocab2words+sharedwords
    return {'vocab1words':vocab1words, 'sharedwords':sharedwords,'vocab2words':vocab2words, 'wordcount':wordcount, 'name1':name1, 'name2':name2}

def printLearningProgress(comparison):
    total = 180
    barChar = '█'
    matureratio = round(comparison['mature']/comparison['wordcount']*total)
    learningratio = round(comparison['learning']/comparison['wordcount']*total)
    unknownratio = total-matureratio-learningratio
    print(Fore.WHITE + comparison['name']+":")
    print(Fore.GREEN + matureratio*barChar + Fore.YELLOW + learningratio*barChar + Fore.RED + unknownratio*barChar)

def printVocabComparison(comparison):
    total = 180
    barChar = '█'
    vocab1ratio = round(comparison['vocab1words']/comparison['wordcount']*total)
    sharedratio = round(comparison['sharedwords']/comparison['wordcount']*total)
    vocab2ratio = total-vocab1ratio-sharedratio
    print(Fore.WHITE + comparison['name1']+" vs "+comparison['name2']+":")
    print(Fore.BLUE + vocab1ratio*barChar + Fore.CYAN + sharedratio*barChar + Fore.GREEN + vocab2ratio*barChar)

# printLearningProgress(compareToCurrentVocab('N5'))
# printLearningProgress(compareToCurrentVocab('N4'))
# printLearningProgress(compareToCurrentVocab('N3'))
# printLearningProgress(compareToCurrentVocab('N2'))
# printLearningProgress(compareToCurrentVocab('N1'))

# printLearningProgress(compareToCurrentVocab('U1'))
# printLearningProgress(compareToCurrentVocab('U2'))
# printLearningProgress(compareToCurrentVocab('U3'))
# printLearningProgress(compareToCurrentVocab('U4'))
# printLearningProgress(compareToCurrentVocab('U5'))

printVocabComparison(compare2Vocabs('core2k','iKnow'))