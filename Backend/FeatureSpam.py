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

'''
Now handle embedding, start with basic term freq-inv docu freq (tf-idf)

(I know it is not gonna work well cuz the document, 
    i.e. each reddit comment, is too short, but per prof Sellie's request we do it anyways)
'''

# necessary for tokenization
import nltk
nltk.download('punkt')




if __name__ == "__main__":
    print("Starting Feature Spam")
    print(countCurses("Lol lets first try clean sentence see what happenes"))
    print(countCurses("Now lets be nasty for a bit: damn."))
    print(countCurses("Ok, clearly works on a single word, what about..."))
    print(countCurses(" 'Maybe I never saw a camel, but I know a camel's cunt when I smell one' --Arya Stark"))
    print(countCurses("Once I've seen pranks on BG3: Arsetarion, Shadowfart, pokemon muk backward is cum, etc..."))
    print(countCurses("ok I guess this ass algo is not as fucking good as I freagging hoped for, son of a bitch."))