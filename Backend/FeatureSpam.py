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



if __name__ == "__main__":
    print("Starting Feature Spam")