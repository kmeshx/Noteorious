##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


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
    
def objectCount(posSubArray):
    
    subTypesH = {'PRP', 'NN', 'NNS', 'NNPS', 'NNP'}
    count = 0
    #justPOSH = justPOSArray(posSubArray)
    for tag in posSubArray:
        if(tag in subTypesH):
            count+=1
    return count
            
    

def maybeASentence(posSubArray):
    
    verbTypes = {'VB', 'VBD', 'VBN', 'VBZ', 'VBP'} #no gerund right now
    subTypes = {'PRP', 'NN', 'NNS', 'NNPS', 'NNP', 'EX', 'CD'}
    
    
    justPOS = justPOSArray(posSubArray)
    if(justPOS[0] in verbTypes):
        return False
    vCount = 0
    sCount = 0
    for i in range(len(justPOS)):
        
        tag = justPOS[i]
        if(tag in {'IN', 'WDT', 'WP$', 'WP'} and objectCount(justPOS[i+1])==0):
            return 'Xtype'
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
        
def joinList(charac, L):
    
    retlist = []
    for i in range(len(L)):
        L[i].append(charac)
        retlist.extend(L[i])
    retlist.pop()
    return retlist
    
def find2ndIndClause(inpSent):
    indclause = ''
    posComArr = posCommaSep(splitOnCommas(inpSent))
    foundSentenceAtOnce = False
    
    for j in range(1,len(posComArr)-1):
        if(maybeASentence(posComArr[j])=='Xtype' and maybeASentence(flatten(posComArr[j+1:]))==True):
            comtex = joinList((',', ','), posComArr[j+1:])
            
            return comtex
            
    #if(maybeASentence(posComArr[-1])==True):
        #return posComArr[-1]
        
    for i in range(1,len(posComArr)):
        curindex = -i
        #print("ci: ", posComArr[curindex])
        #if(curindex==-1 and maybeASentence(posComArr[curindex])==True):
            #return indclause
        
        if(maybeASentence(posComArr[curindex])==False):
            continue
        elif((maybeASentence(posComArr[curindex])==True)):
            remArray = posComArr[curindex:]
            indclause = flatten(remArray)
            
            
    if(indclause!=''):
        foundSentenceAtOnce = True
        return indclause
        
    if(foundSentenceAtOnce==False):
        
        for i in range(len(posComArr)):
            curindex = -i 
            cursubarr = flatten(posComArr[curindex:])
            if(maybeASentence(cursubarr)==True):
                return cursubarr
                
    return ''
    
    

    
print(find2ndIndClause("Since biological species concept is dependent upon reproductive isolation of reproducing species, ongoing shit in life, it cannot necessarily be applied to a species that reproduces asexually."))

print(find2ndIndClause("By examining the similarities, likes and differences of different lineages that are related, scientists, researchers and explorers can determine most likely when the species diverged and evolved compared to when the common ancestor was around."))

#print(find2ndIndClause("Although there is a lot of controversy about this issue, it is still not acted upon by the government"))
    


#"Once you have seen a bad person, a good person and an okay person, you will know there is one highly preferred one, a least preferred one and a middle one."
