##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import *
from nltk import ngrams
from nltk.corpus import wordnet as wn
from itertools import product
import itertools

puncDic = {',', '.', ':', '!', '?'}


##converting array to text

def changeToText(sentArray):
    
    returnStr = ""
    
    for aTuple in sentArray:
        word, type = aTuple[0], aTuple[1]
        if(word not in puncDic):
            returnStr= returnStr + " " + word
        else:
            returnStr= returnStr + word
            
    return returnStr
    
##specialized tokens 

def tokenizedOnKeyword(inpstr, keyword):
    wordArray = inpstr.split(" ")
    keyArray = []
    prevKeyInd = 0
    
    for index in range(len(wordArray)):
        aWord = wordArray[index]
        
        if(aWord == keyword):
            keyArray.append(wordArray[prevKeyInd+1:index])
            prevKeyInd = index
            
    return keyArray
    
def replaceTokenWithPeriod(inpstr, keyword):
    return inpstr.replace(" "+keyword, ".")
    
def capitalizePostKeyword(inpstr, keyword):
#account for indexError last bingo
    wordArray = inpstr.split(" ")
    
    for index in range(len(wordArray)-1):
        aWord = wordArray[index]
        
        if(aWord == keyword):
            toCaps = wordArray[index+1] 
            newWord = toCaps[0].upper() + toCaps[1:]
            wordArray[index+1] = newWord

    return " ".join(wordArray)
    

##semantic similarity measure    
def sentenceSimilarity(sent1, sent2):
    #custom made :)
    
    simScore = 0
    dScore = 10 #change this!
    
    posS1 = tagPreprocess(sent1)
    posS2 = tagPreprocess(sent2)
    
    for w1 in posS1[0]:
        curtag = w1[1]
        if(curtag in setRemoveTags):
            posS1[0].remove(w1)
    
    for w2 in posS2[0]:
        curtag = w2[1]
        if(curtag in setRemoveTags):
            posS2[0].remove(w2)
    
    count = 0        
    for w1 in posS1[0]:
        for w2 in posS2[0]:
            count+=1
            word1 = w1[0]
            word2 = w2[0]
            #if(areSimilar(word1, word2)):
            simScore+=areSimilar(word1, word2)
    
    return simScore   #/min(len(posS1[0]), len(posS2[0]))
    
def areSimilar(word1, word2):
    #Cite: https://stackoverflow.com/questions/18871706/check-if-two-words-are-related-to-each-other
    
    thresholdWordSim = 0.65
    syn1 = wn.synsets(word1)
    syn2 = wn.synsets(word2)
    
    maxSimScore = 0
    
    for i, j in list(product(*[syn1, syn2])):
        simS = i.wup_similarity(j)
        if(simS is None): return 0
        if(simS > maxSimScore):
            maxSimScore = simS
        
            
    return maxSimScore #>=thresholdWordSim    