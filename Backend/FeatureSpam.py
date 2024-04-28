'''
This is the module to produce additional features for the sarcasm detection
The two main word baskets we need are profanity basket, and onomatopoea basket.
'''

####################################curses section######################################

from better_profanity import profanity

'''
take entire sentence (reddit post) as input
binary flag of whether there is curse word.
'''
def flagCurses(text):
    return profanity.contains_profanity(text)

'''
take entire sentence (reddit post) as input
count curses based on word
'''
def countCurses(text):
    count = 0
    for eachWord in text.split():
        if profanity.contains_profanity(eachWord):
            count += 1
    return count

##################################################################

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math

'''
Now handle embedding, start with basic term freq-inv docu freq (tf-idf)

(I know it is not gonna work well cuz the document, 
    i.e. each reddit comment, is too short, but per prof Sellie's request we do it anyways)
'''

# necessary for tokenization
import nltk
nltk.download('punkt')
nltk.download('stopwords')

#preprocessing
def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


def stemming(data):
    stemmer = PorterStemmer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data

'''
tentative test dataset dimension (1000,9) exclusing y val
features [0] and [8] do standard embedding (they are comment and parent post text)
feature [1], is username, tentatively do profanity check
'''


'''
first, need to scan all comments at features [0], [1], and [8] tp see recurrence of curse (separate)
Note we only care if docu contains, not count in each
assume data passed in is a simple column vector
'''
def crossDocOccurrence(data):
    count = 0
    for each in data:
        if flagCurses(each):
            count += 1
    return count

def idf(data):
    resArr = np.zeros((data.shape[0],))
    count = crossDocOccurrence(data)
    for i in range(resArr.shape[0]):
        if(flagCurses(data[i])):
            resArr[i] = np.log(countCurses(data[i]))/count
        else:
            resArr[i] = 0
    return resArr

def vecProcess(data):
    resArr = [None]*data.shape[0]
    for i in range(data.shape[0]):
        resArr[i] = preprocess(data[i])
    return np.array(resArr)

def vecFlagCurses(data):
    resArr = np.zeros((data.shape[0],))
    for i in range(resArr.shape[0]):
        resArr[i] += flagCurses(data[i])
    return resArr
    

    
#################################Embedding for subreddit group title###########################
'''
approach: create our own basket
'''
from collections import OrderedDict

'''
we return avector of same dim,
encode values go from 0, most freq,
to cutoff, least freq, and cutoff+1, misc others
'''
def subRedProcess(data, cutoff):
    map = OrderedDict()
    for each in data:
        if each in map:
            map[each] += 1
        else:
            map[each] = 1
    sortedItems = [item[0] for item in sorted(map.items(), key=lambda x: x[1], reverse=True)]   #rev sort of only keys
    resArr = np.zeros((data.shape[0],))
    for i in range(resArr.shape[0]):
        currRank = sortedItems.index(data[i])
        if currRank<=cutoff:
            resArr[i] = currRank
        else:
            resArr[i] = cutoff+1
    return resArr

##########################################additional processing######################################3
'''
We also realized that in the original dataset, some of the data
has wrong type/data (corruption)
'''
def weedOut(array, featureInd, goodType):
    for i in range(len(array)):
        if not isinstance(array[i][featureInd], goodType):
            array.pop(i)

#########################################3validation calculation###########################
def validate(trueY, predY, cutoff):
    return np.sum(trueY>cutoff)/np.sum(predY>cutoff)


if __name__ == "__main__":
    print("Hello world")
    print(countCurses("FUCK FUCKING  fuck ass Fuck fucking sex"))
