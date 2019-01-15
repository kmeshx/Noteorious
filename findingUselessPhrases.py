##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


import nltk
from nltk import sent_tokenize, word_tokenize


uselessDic = {"Basically", "Essentially", "in other words", "is","say", "was", "mean", "means", "saying", "what", "you", 'could',  'that', 'I', 'to', 'as', 'should', 'also', 'um', 'uh', 'yeah', 'so', 'this', 'am', 'What', 'would', 'like'}

puncDic = {',', '.', ':', '!', '?'}

usefulTagDic = {'NN', 'NNS', 'NNPS', 'NNP', 'JJ', 'JJR', "JJS", "CD", 'LS', 'RB'}

verbCheckDic = {'VB', 'VBZ', 'VBG', 'VBP', 'VBN', 'VBD'}


def newFindUseless(wordArray):
    #wordArray = nltk.word_tokenize(inpPhrase)
    count=0
    npCount=0
    for word in wordArray:
        if(word not in puncDic): npCount+=1
        if(word not in puncDic and word in uselessDic):
            count+=1
    if(count==npCount):
        return True
    else:
        return False