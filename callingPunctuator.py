import speech_recognition as sr  
#from pydub import AudioSegment,silence
from os import path
from tkinter import *
from tkinter import font
import random
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import *
from nltk import ngrams
from nltk.corpus import wordnet as wn
from itertools import product
import itertools
import requests
import textwrap
from word2number import w2n

"""data2 = [
  ('text', 'there are three ways to do this first we can charge second we can dance third we can sing'),
]
data = {'text': "Once you have seen a pink, red and yellow ruby, you will know there is one highly preferred one, a least preferred one and a middle one."}
r = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)"""

#print(r.json())
#a = r.text
#print(a)
#print(r.status_code)

def tagPreprocess(testString):
    testStrsent = sent_tokenize(testString)
    testStrsent = [nltk.word_tokenize(sent) for sent in testStrsent]
    testStrsent = [nltk.pos_tag(sent) for sent in testStrsent]
    
    return testStrsent
    
#b = tagPreprocess(a)
#print(b)

def splitOnCommas(inpstr):
    return inpstr.split(",")
    
def posCommaSep(comArray):
    returnArray = []
    for phrase in comArray:
        #print("ph:", phrase)
        posPhrase = nltk.pos_tag(phrase.strip().split())
        #print("PT:", posPhrase)
        returnArray.append(posPhrase)
    return returnArray
    

def justPOSArray(posSubArray):
    returnArray = []
    for word, tag in posSubArray:
        returnArray.append(tag)
    return returnArray
    

def maybeASentence(posSubArray):
    
    verbTypes = {'VB', 'VBD', 'VBN', 'VBZ', 'VBP'} #no gerund right now
    subTypes = {'PRP', 'NN', 'NNS', 'NNPS', 'NNP', 'EX', 'CD'}
    
    justPOS = justPOSArray(posSubArray)
    vCount = 0
    sCount = 0
    for tag in justPOS:
        if(tag in verbTypes):
            vCount+=1
        if(tag in subTypes):
            sCount+=1
    bool1 = vCount > 0
    bool2 = sCount > 0
    bool3 = len(posSubArray) >= 3
    
    if(bool1 and bool2 and bool3):
        return True
    return False
    
def flatten(L, depth=0):
    #returns list of only elements from list of lists
    if(isinstance(L, list)==False and depth==0):
        return L
    elif(isinstance(L, list)==False):
        return [L]
    elif(L==[]):
        return []
    else:
        firstElement = L[0]
        return flatten(firstElement, depth+1) + flatten(L[1:], depth+1)
    
def find2ndIndClause(inpSent):
    indclause = ''
    posComArr = posCommaSep(splitOnCommas(inpSent))
    foundSentenceAtOnce = False
    for i in range(1,len(posComArr)):
        curindex = -i
        print("ci: ", posComArr[curindex])
        if(maybeASentence(posComArr[curindex])==False):
            continue
        else:
            remArray = posComArr[curindex:]
            indclause = flatten(remArray)
    if(indclause!=''):
        foundSentenceAtOnce = True
        return indclause
        
    if(foundSentenceAtOnce==False):
        
        for i in range(len(posComArr)):
            curindex = -i 
            cursubarr = flatten(posComArr[curindex:])
            if(maybeASentence(cursubarr)):
                return cursubarr
                
    return ''
    
#print(find2ndIndClause("Once you have seen a bad person, a good person and an okay person, you will know there is one highly preferred one, a least preferred one and a middle one."))

#print(find2ndIndClause("Although there is a lot of controversy about this issue, it is still not acted upon by the government"))
    


#"Once you have seen a bad person, a good person and an okay person, you will know there is one highly preferred one, a least preferred one and a middle one."
