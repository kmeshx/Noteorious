##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project




# -*- coding: utf-8 -*-
import speech_recognition as sr  
import itertools
import requests
import textwrap
import random
import os
import nltk
from pydub import AudioSegment,silence
from os import path
from PIL import Image
from PIL import *
from tkinter import *
from tkinter import font
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import *
from nltk import ngrams
from nltk.corpus import wordnet as wn
from itertools import product
from word2number import w2n
from extractIndependentClause import *
from mathConverter import *
from findingUselessPhrases import *
from similarityAndKeyword import *
from createGradientRect import *
from bubbleGraphics import *


##This code generates a postscript file to view notes.

#this code also tests the program on test strings.

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/kushamaharshi/Downloads/TPlearn-c9ebbc1e8845.json"
# from oauth2client.client import GoogleCredentials
# credentials = GoogleCredentials.get_application_default()
# from googleapiclient.discovery import build
# service = build('compute', 'v1', credentials=credentials)

# obtain audio from the microphone  
#!/usr/bin/env python3


##test strings

punctuatedString3 = "Species are different varieties of animals. They are formed over a long time. They can interbreed. Just need some words here. If you have more money, then you automatically have more happiness, due to increased sense of security. They have differences in color, size, strength, gender roles, etcetera. There are three ways to do this. first, we can charge. Still talking about first here. still going bleh. Second, we can dance. Droning about second here. still going bleh. Third, we can sing. still going bleh. Singing like shit. Okay, moving on. Life is good. This can be done in four ways: swimming, charging, dancing and bathing. This is a nice thing to do."

##ALL GLOBALS:
###


uselessDic = {"Basically", "Essentially", "in other words", "is","say", "was", "mean", "means", "saying", "what", "you", 'could',  'that', 'I', 'to', 'as', 'should', 'also', 'um', 'uh', 'yeah', 'so', 'this', 'am', 'What'}

puncDic = {',', '.', ':', '!', '?'}

usefulTagDic = {'NN', 'NNS', 'NNPS', 'NNP', 'JJ', 'JJR', "JJS", "CD", 'LS', 'RB'}

verbCheckDic = {'VB', 'VBZ', 'VBG', 'VBP', 'VBN', 'VBD'}

megaDic = {"results in": "clty", 'therefore': 'clty', "leads to": "clty", 'accordingly': 'clty', 'as a result': 'clty', 'Subsequently': 'clty', 'thus': 'clty', "causes": "clty", "If": "prec", "in case": "prec", 'As a result of': 'prec', "When": "prec", "Because": "prec", "due to": "ub", "because of": "ub", "thanks to": "ub", "courtesy of": "ub", "then": "clty", 'if': 'precc', 'although': 'sc', 'Although': 'sc', 'Whenever': 'sc', 'Without': 'sc', 'By': 'sc', 'Since': 'sc'}

numberListArray = ["there are *n* ways to do this", "in the following ways", "there are *n* possibilities", "in *n* ways"]

stopIndDic = {"Okay", "Now", "Let's", "Bingo", 'bingo'}

numAdverbDic = {1: ['First', 'Firstly', 'first', 'firstly'], 2: ['second', 'secondly', 'Second', 'Secondly'], 3:['third', 'Third'], 4: ['fourth', 'Fourth'], 5: ['fifth', 'Fifth'], 6: ['sixth', 'Sixth'], 7: ['seventh', 'Seventh'], 8: ['eighth', 'Eighth'], 9:['ninth', 'Ninth']}

setRemoveTags = {'CC', 'EX', 'DT', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP$', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB'}

RBGTupDic = {"red": (255, 1, 120, 2, 150, 1), "blue": (141, 1, 255, 1, 225, 1), "green": (255, 0, 77, 1, 160, 1), "yellow": (30, 0, 130, 1, 255, 1), "orange": (204, 1, 255, 2, 0, 0)}

enumTriggers = {"ways", "methods", "kinds", "types", "sorts", 'cases'}  

numberDic = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

mathDic = {'times': '*', 'divided by': '/', 'plus': '+', 'minus': '-', 'subtracted from': '-', 'added to': '+', 'over': '/'}

#lightDarkColDic = {'red': '#ff8080', 'orange': '#ffcc99', 'yellow': '#ffff99', 'green':'#cccc33', 'blue': '#80bfff'}

lightDarkColDic = {'red': ['#ffe6e6', '#ffcccc'], 'blue': ['#ccefff', '#e6f7ff'], 'green':['#e6ffe6', '#ccffcc'], 'yellow': ['#ffffe6', '#ffffcc'], 'orange': ['#ffe6cc', '#ffdab3']}

globalColorsList = ["red", "blue", "green", "yellow", "orange"]

##functions to return tagged sentences

def tagPreprocess(testString):
    testStrsent = sent_tokenize(testString)
    testStrsent = [nltk.word_tokenize(sent) for sent in testStrsent]
    testStrsent = [nltk.pos_tag(sent) for sent in testStrsent]
    
    return testStrsent
    

##KEY: clty = causes/leads to, ub = underbubble, prec = precondition, postc= postcondition, lo = list out, tc = textchunk

def labeler(sentArray):
    returnArray = []
    l = len(sentArray)
    prevcw2 = ""
    for index in range(l):
        curword1 = sentArray[index]
        curword2 = " ".join(sentArray[index:index+2])
        
        if(curword1 in megaDic):
            returnArray.append((curword1, megaDic[curword1]))
        elif(curword2 in megaDic):
            returnArray.append((curword2, megaDic[curword2]))
            prevcw2 = curword2
        else:
            if(curword1 in prevcw2):
                continue
            else:
                returnArray.append((curword1, "tc"))
    return returnArray


##text chunking based on cause effect relation

def chunker(labSent):
    chunkedArray = []
    l = len(labSent)
    previndex = 0
    prevword, prevtype = labSent[0]
    cc=0
    for index in range(l):
        word, type = labSent[index]
        #print(word, type)
        
        if(type!="tc"):
            cc+=1
            curchunkTuple = (prevtype, labSent[previndex:index])
            
            #print("previndwordtype", previndex, prevword, prevtype)
            #print("curchunkTuple \n", curchunkTuple)
            if(curchunkTuple[1]!=[]):
                chunkedArray.append(curchunkTuple)
            prevtype = type
            prevword = word
            previndex = index
    
    if(cc==1 and labSent[0][1]=='sc'):
            
        #print("CHUUUUUSTART")
        cursent = labSent
        #print('cursent: ', cursent)
        texthere = changeToText(cursent)
        #print('texthere: ', texthere)
        cl = changeToText(find2ndIndClause(texthere))
        #print('f2i: ', find2ndIndClause(texthere))
        #print('cl: ', cl)
        cln = (texthere.strip()).replace(cl.strip(), "")
        #print('cln: ', cln)
        if(cl!=''):
            #print("CHUUUUUSTART")
            #print("CHUUUUUUU: ", chunkedArray)
            #chunkedArray.pop()
            #print("CHUUUUUUU: ", chunkedArray)
            chunkedArray.append(('sc', labeler(cln.split())))
            #print("CHUUUUUUU: ", chunkedArray)
            chunkedArray.append(('tc', labeler(cl.split())))
            #print("CHUUUUUUU: ", chunkedArray)
            #print()
        return chunkedArray

        
            
    lastCurChunkTuple = (prevtype, labSent[previndex:])
    chunkedArray.append(lastCurChunkTuple)
    
    
    return chunkedArray
    

##checking for enumeration triggers

 
def checkEnumTrig(labelledSubArr, arrind):
    prevWord, prevLabel = labelledSubArr[0]
    for index in range(len(labelledSubArr)):
        word, label = labelledSubArr[index]
        if(word in enumTriggers):
            if(prevLabel=='CD'):
                num = prevWord
                checkForAndLabelBif(mainPosArr, index, num, arrind)
        prevWord, prevLabel = word, label
        
    return mainPosArr #change name, remove return?


def checkBubBifB(mainPosArray):
    bifBubbles, bifIndices, bifJumps, bifPrecSents = [], [], [], []
    prevWord, prevLabel = mainPosArray[0][0]
    for index in range(len(mainPosArray)):
        subArray = mainPosArray[index]
        #print(subArray)
        for j in range(len(subArray)-1):
            word, label = subArray[j]
            #print(word, subArray[j-1][1])

            if(word in enumTriggers and subArray[j-1][1]=='CD'):
                #print("yay")
                num = subArray[j-1][0]
                remainingSent = subArray[j+1:]
                #print(remainingSent)
                bifPrecSents.append(subArray[:j+1])
                if(remainingSent[0][0]==":"):
                    remainingSent.pop(0)
                    bifBubbles.append(giveBubBif(remainingSent, num))
                    
                    bifIndices.append(index)
                    bifJumps.append(0)
                    
                elif(subArray[-1][0]!=":"):
                    bifBubbles.append(giveBubBif2(mainPosArray[index+1:index+1+numberDic[num]], num))
                    bifIndices.append(index)
                    bifJumps.append(numberDic[num])
            
                
                
    return bifBubbles, bifIndices, bifJumps, bifPrecSents
    
def checkBubBifA(mainPosArray):
    bifBubbles, bifIndices, bifJumps, bifPrecSents = [], [], [], []
    prevWord, prevLabel = mainPosArray[0][0]
    #print("pw, pl: ", prevWord, prevLabel)
    for index in range(len(mainPosArray)):
        subArray = mainPosArray[index]
        #print(subArray)
        for j in range(len(subArray)-1):
            word, label = subArray[j]
            #print(word, subArray[j-1][1])

            if(word in enumTriggers and subArray[j-1][1]=='CD'):
                #print("yay")
                num = subArray[j-1][0]
                remainingSent = subArray[j+1:]
                #print(remainingSent)
                bifPrecSents.append(subArray[:j+1])
                
                if(remainingSent[0][0]==":"):
                    #print("the old iffing")
                    remainingSent.pop(0)
                    bifBubbles.append(giveBubBif(remainingSent, num))
                    bifIndices.append(index)
                    bifJumps.append(0)
                    
                elif(subArray[-1][0]=='.' and (mainPosArray[index+1][0][0] in ['first', 'firstly', 'First', 'Firstly'])):
                    
                    arrayTillLastCount = mainPosArray[index+1:]
                    mCSS = []
                    curSubSent = []
                    numPosnCount = 0
                    toJump = 0
                    for subSubSent in arrayTillLastCount:
                        #print("subsubsent: ", subSubSent)
                        
                        if(numPosnCount==numberDic[num] and subSubSent[0][0] in stopIndDic):
                            mCSS.append(curSubSent)
                            #print("breaking")
                            #print()
                            break
                            
                        else:
                            toJump+=1
                            #print("tojump: ", toJump)
                            if(subSubSent[0][0] in numAdverbDic[numPosnCount+1]):
                                #print("curSubSent: ", curSubSent)
                                #print()
                                
                                if(curSubSent!=[]):
                                    
                                    mCSS.append(curSubSent)
                                    
                                curSubSent = []
                                #print("new css: ", curSubSent)
                                #print()
                                
                                curSubSent.append(subSubSent)
                                numPosnCount+=1
                                #print("npc: ", numPosnCount)
                                
                            else:
                                curSubSent.append(subSubSent)
                                
                        
                    
                    bifBubbles.append(mCSS)
                    #print("ahhhhhh: ", bifBubbles)    
                    bifIndices.append(index)
                    bifJumps.append(toJump)
    
    #print()
    #print()
    #print("returning")
    #print("bbb: ", bifBubbles)
    return bifBubbles, bifIndices, bifJumps, bifPrecSents 
    
    
def giveBubBif(remainingSent, num):
    #https://stackoverflow.com/questions/15357830/python-spliting-a-list-based-on-a-delimiter-word
    
    spl = [list(y) for x, y in itertools.groupby(remainingSent, lambda z: z == (",", ",")) if not x]
    
    for i in spl:
        if (("and", "CC") in i):
            fi = i.index(("and", "CC"))
            p1 = i[:fi]
            p2 = i[fi+1:]
            spl.remove(i)
            spl.append(p1)
            spl.append(p2)
            
    if(len(spl)==numberDic[num]):
        return spl
    return spl
        
def giveBubBif2(remainingSent, num):
    return remainingSent
               
               
def getBifYChange(bubArray):
    maxConBifs = 0
    if(isinstance(bubArray[0][0], list)):
        for bifDiv in bubArray:
            curlen = len(bifDiv)
            if(curlen>maxConBifs):
                maxConBifs = curlen
        return maxConBifs
    return 1

def getBifYMax(bubArray):
    gap = 20
    maxBifY = 0
    curbify = 0
    if(isinstance(bubArray[0][0], list)):
        for bifDiv in bubArray:
            curbify=0
            for subsub in bifDiv:
                curTextLength, newtext = getDisplayHeight(changeToText(subsub))
                curbify=curbify+curTextLength+gap
            curbify-=gap
            if(curbify>maxBifY):
                maxBifY = curbify
                
        return maxBifY
        
    else:
        maxBifY2 = 0
        #curbify2 = 0
        for bifDiv in bubArray:
            curTextLength2, newtext2 = getDisplayHeight(changeToText(bifDiv))
            if(curTextLength2>maxBifY2):
                maxBifY2 = curTextLength2
        
        return maxBifY2+gap
            

            
##next comes the bubble class code along with tkinter data

class Bubble(object):
    
    bubbleList = [] #list of all bubble objects currently on screen
    dM1 = 1/4 #avoiding magic numbers, 112 teaches a lot
    dM2 = 4/5
    dM3 = 3/4
    dM4, dM5 = 9/10, 1/10
    
    yHeight = 30
    curnum = -1

    
    def __init__(self, bubtype, bubtext, bubcolor, bifIndex=None, bifYChange = 0, bifYActual=0):
        
        self.bubtype = bubtype
        self.bubtext = bubtext
        self.color = bubcolor
        self.xCor = 0
        self.yCor = 0
        Bubble.curnum+=1
        self.index = Bubble.curnum
        self.bifIndex = bifIndex
        self.bifYChange = bifYChange
        self.bifYActual = bifYActual
        
        removeX = 4*700/15
        removeY = 700/10
        wwidth, wheight = 700, 700
        yHeight = 60
        shift = (700-removeX)/3 + removeX/4
        shift1 = 2*removeX/4
        gap = 20
        
        # wwidth, wheight = 700, 700
        # yHeight = 60
        # removeX = 4*wwidth/15
        # removeY = wheight/10
        if(Bubble.bubbleList==[]):
            self.xCor = (wwidth-removeX)/3 + removeX/2
            self.yCor = wheight-removeY-yHeight
        else:
            
            if(self.bubtype=="clty"):
                xtext = changeToText(self.bubtext)
                rectHeight, xtext = getDisplayHeight(xtext)
                #self.xCor = Bubble.bubbleList[-1].xCor+shift
                #self.xCor = (wwidth-removeX)/3 + removeX/2 + shift
                self.xCor = Bubble.bubbleList[self.index-1].xCor+(wwidth-removeX)/3+shift1
                self.yCor = Bubble.bubbleList[self.index-1].yCor-rectHeight-gap
            elif(self.bubtype=="prec" or self.bubtype=='precc' or self.bubtype=='sc'):
                xtext = changeToText(self.bubtext)
                rectHeight, xtext = getDisplayHeight(xtext)
                #self.xCor = Bubble.bubbleList[-1].xCor-shift
                self.xCor = (wwidth-removeX)/3 + removeX/2 - shift
                self.yCor = Bubble.bubbleList[self.index-1].yCor-rectHeight-gap
            
            elif(self.bubtype=="postc"):
                xtext = changeToText(self.bubtext)
                rectHeight, xtext = getDisplayHeight(xtext)
                #self.xCor = Bubble.bubbleList[-1].xCor-shift
                self.xCor = (wwidth-removeX)/3 + removeX/2 + shift
                self.yCor = Bubble.bubbleList[self.index-1].yCor-rectHeight-gap
            elif(self.bubtype=="ub"):
                xtext = changeToText(self.bubtext)
                rectHeight, xtext = getDisplayHeight(xtext)
                if(Bubble.bubbleList[self.index-1].bubtype in ['clty', 'postc', 'tc']):
                    self.xCor = Bubble.bubbleList[self.index-1].xCor+(wwidth-removeX)/3
                    self.yCor = Bubble.bubbleList[self.index-1].yCor-rectHeight
                elif(Bubble.bubbleList[self.index-1].bubtype == 'prec'):
                    self.xCor = Bubble.bubbleList[self.index-1].xCor-(wwidth-removeX)/3
                    self.yCor = Bubble.bubbleList[self.index-1].yCor-rectHeight
                    
            elif(self.bubtype=="bif"):
                #xtext = changeToText(self.bubtext)
                #rectHeight, xtext = getDisplayHeight(xtext)
                self.xCor = (wwidth-removeX)/3 + removeX/2
                self.yCor = Bubble.bubbleList[self.index-1].yCor-yHeight-gap
            else:
                xtext = changeToText(self.bubtext)
                rectHeight, xtext = getDisplayHeight(xtext)
                self.xCor = (wwidth-removeX)/3 + removeX/2
                self.yCor = Bubble.bubbleList[self.index-1].yCor-rectHeight-gap
                
                
                
            if(Bubble.bubbleList[self.index-1].bubtype=='bif'):
                #self.yCor = self.yCor-(yHeight+gap)*Bubble.bubbleList[self.index-1].bifYChange
                self.yCor = self.yCor - Bubble.bubbleList[self.index-1].bifYActual-gap
                
            if(self.bubtype in {"clty", "prec", "postc", "ub"}):
                self.color = Bubble.bubbleList[self.index-1].color
                
                
        #print("Object created!")
            
        Bubble.bubbleList.append(self)
        
#center, leadsTo, causedBy etc., are different kinds of bubbles that we want in our notes
    

    def drawCenterBubble(self, canvas):
        
        removeX = 4*700/15
        removeY = 700/10
        yHeight = 60
        
        self.bubtext = changeToText(self.bubtext)
        rectHeight, self.bubtext = getDisplayHeight(self.bubtext)
        #print("prey: ", self.yCor)
        #self.yCor = self.yCor - 2*rectHeight
        #print("prea: ", self.yCor)
        createMyImage(canvas, self.xCor, self.yCor, rectHeight, (700-removeX)//3, RBGTupDic[self.color], 1)
        
        #roundedRect(canvas, self.xCor, self.yCor, (700-removeX)/3,rectHeight, self.color)
        
        prettyText(canvas, self.bubtext, self.xCor, self.yCor, 'white')
        
    def drawLeadsToBub(self, canvas):
        wwidth, wheight = 700, 700
        removeX = 4*wwidth/15
        removeY = wheight/10
        
        yHeight = 60
        
        self.bubtext = changeToText(self.bubtext)
        rectHeight, self.bubtext = getDisplayHeight(self.bubtext)
        
        rectHeight = rectHeight+10
        #self.yCor = self.yCor + yHeight - rectHeight
       
        #trblThoughtBubble(canvas, self.xCor, self.yCor, self.xCor, self.yCor+yHeight+20, (data.width-removeX)/3,yHeight, self.color)
        #trblThoughtBubble(canvas, self.xCor, self.yCor, Bubble.bubbleList[self.index-1].xCor, Bubble.bubbleList[self.index-1].yCor, (wwidth-removeX)/3, yHeight, self.color)
        #trblThoughtBubble(canvas, self.xCor, self.yCor, Bubble.bubbleList[self.index-1].xCor+(wwidth-removeX)/3, Bubble.bubbleList[self.index-1].yCor+rectHeight, (wwidth-removeX)/3, rectHeight, self.color)
        trblThoughtBubble(canvas, self.xCor, self.yCor, Bubble.bubbleList[self.index-1].xCor+(wwidth-removeX)/3, Bubble.bubbleList[self.index-1].yCor, (wwidth-removeX)/3, rectHeight, self.color)
        
        prettyText(canvas, self.bubtext, self.xCor+10, self.yCor+10, 'black')
        
        
    def drawCausedBy(self, canvas):
        wwidth, wheight = 700, 700
        removeX = 4*wwidth/15
        removeY = wheight/10
        
        yHeight = 60
       
        
        self.bubtext = changeToText(self.bubtext)
        
        
        #trblThoughtBubble(canvas, self.xCor+rightShift, self.yCor, self.xCor+(data.width-removeX)/3, self.yCor+yHeight+20, (data.width-removeX)/3, yHeight, self.color)
        
        #rectHeight, self.bubtext = getDisplayHeight(self.bubtext)
        rectHeight, self.bubtext = getDisplayHeight(self.bubtext)
        rectHeight = rectHeight+10
        self.yCor = self.yCor + yHeight - rectHeight
        #thoughtBubble(canvas, self.xCor, self.yCor, Bubble.bubbleList[self.index+1].xCor, Bubble.bubbleList[self.index+1].yCor, (wwidth-removeX)/3, yHeight, self.color)
        
        if(self.index<len(Bubble.bubbleList)-1):
            thoughtBubble(canvas, self.xCor, self.yCor, Bubble.bubbleList[self.index+1].xCor,
            Bubble.bubbleList[self.index+1].yCor, (wwidth-removeX)/3, rectHeight, self.color)
        else:
            thoughtBubble(canvas, self.xCor, self.yCor, self.xCor+(wwidth-removeX)/3,
            self.yCor+rectHeight, (wwidth-removeX)/3, rectHeight, self.color)
            
        
        prettyText(canvas, self.bubtext, self.xCor+10, self.yCor+10, 'black')
        
        
    def drawCausedByC(self, canvas):
        
        wwidth, wheight = 700, 700
        removeX = 4*wwidth/15
        removeY = wheight/10
        
        yHeight = 60
       
        
        self.bubtext = changeToText(self.bubtext)
        
        
        #trblThoughtBubble(canvas, self.xCor+rightShift, self.yCor, self.xCor+(data.width-removeX)/3, self.yCor+yHeight+20, (data.width-removeX)/3, yHeight, self.color)
        
        #rectHeight, self.bubtext = getDisplayHeight(self.bubtext)
        rectHeight, self.bubtext = getDisplayHeight(self.bubtext)
        rectHeight = rectHeight+10
        self.yCor = self.yCor + yHeight - rectHeight
        #thoughtBubble(canvas, self.xCor, self.yCor, Bubble.bubbleList[self.index+1].xCor, Bubble.bubbleList[self.index+1].yCor, (wwidth-removeX)/3, yHeight, self.color)
        
        thoughtBubble(canvas, self.xCor, self.yCor, Bubble.bubbleList[self.index-1].xCor, Bubble.bubbleList[self.index-1].yCor, (wwidth-removeX)/3, rectHeight, self.color)
        
        prettyText(canvas, self.bubtext, self.xCor+10, self.yCor+10, 'black')
        
        
    def drawBifBub2(self, canvas):
        wwidth, wheight = 700, 700
        removeX = 4*wwidth/15
        removeY = wheight/10
        gap=20
        yHeight = 60
        
        sentences = bifBubbles[self.bifIndex]
        numBifs = len(sentences)
        
        precedingSent = bifPrecSents[self.bifIndex]
        precSentText = changeToText(precedingSent)
        
        rectHeight, precSentText = getDisplayHeight(precSentText)
        
        
        roundedRect(canvas, self.xCor, self.yCor, (wwidth-removeX)/3, rectHeight, self.color)
        prettyText(canvas, precSentText, self.xCor, self.yCor)
        
        
        if(numBifs%2==0):
            startXCor = self.xCor-(numBifs/2-1)*(wwidth-removeX)/3-(wwidth-removeX)/6-(numBifs/2-1)*gap
            startYCor = self.yCor-yHeight-gap
        else:
            startXCor = self.xCor - (wwidth-removeX)/3*(numBifs-1)/2 - gap*(numBifs-1)/2
            startYCor = self.yCor-yHeight-gap
        
            
        for i in range(numBifs):
            x = startXCor + i*(gap+(wwidth-removeX)/3)
            y = startYCor
            roundedRect(canvas, x, y, (wwidth-removeX)/3,yHeight, self.color)
            
            textToShow = changeToText(sentences[i])
            prettyText(canvas, textToShow, x, y)
            
        #self.yCor = self.yCor - yHeight - gap
        
    def drawBifBub(self, canvas):
        wwidth, wheight = 700, 700
        removeX = 4*wwidth/15
        removeY = wheight/10
        gap=20
        yHeight = 60
        drawTo1 = []
        drawTo2 = []
        ##
        #print("bb: ", bifBubbles)
        ##
        #print("selfi: ", self.bifIndex)
        sentences = bifBubbles[self.bifIndex]
        
        numBifs = len(sentences)
        
        precedingSent = bifPrecSents[self.bifIndex]
        precSentText = changeToText(precedingSent)
        
        rectHeight, precSentText = getDisplayHeight(precSentText)
        #self.yCor = self.yCor + yHeight - rectHeight
        
        createMyImage(canvas, self.xCor, self.yCor, rectHeight, (700-removeX)//3, RBGTupDic[self.color], 1)
        #roundedRect(canvas, self.xCor, self.yCor, (wwidth-removeX)/3, rectHeight, self.color)
        prettyText(canvas, precSentText, self.xCor, self.yCor, 'white')
        
        xii, yii  = self.xCor, self.yCor
        
        
        
        if(numBifs%2==0):
            startXCor = self.xCor-(numBifs/2-1)*(wwidth-removeX)/3-(wwidth-removeX)/6-(numBifs/2-1)*gap
            startYCor = self.yCor-rectHeight-gap
        else:
            startXCor = self.xCor - (wwidth-removeX)/3*(numBifs-1)/2 - gap*(numBifs-1)/2
            startYCor = self.yCor-rectHeight-gap
        #print("sentences: ", sentences)
        if(isinstance(sentences[0][0], list)):
            
            
            for i in range(numBifs):
                
                x = startXCor + i*(gap+(wwidth-removeX)/3)
                drawTo1.append(((x+(700-removeX)//6), yii - gap))
                #- getDisplayHeight(changeToText(sentences[0][0]))[0]))
                #drawTo1.append(((x+(700-removeX)//6), ydt))
                
                
                y = yii
                for j in range(len(sentences[i])):
                    
                    
                    textToShow = changeToText(sentences[i][j])
                    rectHeight, textToShow = getDisplayHeight(textToShow)
                    
                    
                    #self.yCor = self.yCor + yHeight - rectHeight
                    
                    y = y - gap - rectHeight
                    
                    
                    #roundedRect(canvas, x, y, (wwidth-removeX)/3,yHeight, self.color)
                    
                    self.yCor -= (yHeight + gap)
                    
                    createMyImage(canvas, x, y, rectHeight, (700-removeX)//3, RBGTupDic[self.color], 1)
                    
                    prettyText(canvas, textToShow, x, y, 'white')
                    
            for aa in drawTo1:
                canvas.create_line(aa, (xii+(700-removeX)//6 , yii), fill='white', width=4)
                
        else:
            #ydt = startYCor+yHeight
            y = yii
            for i in range(numBifs):
                x = startXCor + i*(gap+(wwidth-removeX)/3)
                drawTo2.append(((x+(700-removeX)//6), yii - gap))
                #- getDisplayHeight(changeToText(sentences[0]))[0]))
                #drawTo2.append(((x+(700-removeX)//6), ydt))
                
                #y = startYCor
                
                #roundedRect(canvas, x, y, (wwidth-removeX)/3,yHeight, self.color)
                
                textToShow = changeToText(sentences[i])
                rectHeight, textToShow = getDisplayHeight(textToShow)
                
                y = yii - gap - rectHeight
                
                createMyImage(canvas, x, y, rectHeight, (700-removeX)//3, RBGTupDic[self.color], 1)
                prettyText(canvas, textToShow, x, y, 'white')
                
            for aa in drawTo2:
                canvas.create_line(aa, (self.xCor+(700-removeX)//6 , self.yCor), fill='white', width=4)
                
                
        #self.yCor = self.yCor - yHeight - gap
    
    def drawUbBub(self, canvas):
        wwidth, wheight = 700, 700
        removeX = 4*wwidth/15
        removeY = wheight/10
        
        yHeight = 60
        
        self.bubtext = changeToText(self.bubtext)
        rectHeight, self.bubtext = getDisplayHeight(self.bubtext)
        rectHeight+=10
        
        createMyImage(canvas, self.xCor, self.yCor, rectHeight, (700-removeX)//3, RBGTupDic[self.color], 1)
        #roundedRect(canvas, self.xCor, self.yCor, (wwidth-removeX)/3,rectHeight, self.color)
        
        prettyText(canvas, self.bubtext, self.xCor+10, self.yCor+10, 'white')
        
        
            
    def actualDrawBubble(self, canvas):
       # print("X Cor: ", self.xCor)
        #print("Y Cor: ", self.yCor)
        if(self.bubtype=="clty"):
            self.drawLeadsToBub(canvas)
        elif(self.bubtype=="prec" or self.bubtype=='sc'):
            self.drawCausedBy(canvas)
        elif(self.bubtype=='precc'):
            self.drawCausedByC(canvas)
        elif(self.bubtype=="postc"):
            self.drawLeadsToBub(canvas)
        elif(self.bubtype=="bif"):
            self.drawBifBub(canvas)
        elif(self.bubtype=="ub"):
            self.drawUbBub(canvas)
        else:
            self.drawCenterBubble(canvas)
            

##CANVAS DRAWING WITHOUT ANIMATION

def draw(canvas, width, height):
    for aBubble in Bubble.bubbleList:
        aBubble.actualDrawBubble(canvas)

def runDrawing(width=700, height=700):
    
    root = Tk()
    canvas = Canvas(root, width=width, height=height, background='black')
    canvas.pack()
    bubXMax, bubXMin = 0, 0
    bubYMax, bubYMin = 0, 0
    for i in Bubble.bubbleList:
        if(i.xCor > bubXMax):
            bubXMax = i.xCor
        if(i.xCor < bubXMin):
            bubXMin = i.xCor
            
    for j in Bubble.bubbleList:
        if(j.yCor > bubYMax):
            bubYMax = j.yCor
        if(j.yCor < bubYMin):
            bubYMin = j.yCor
        
    fileBoundX, fileBoundY =  bubXMin-350, bubYMin-350
    canvas.create_rectangle(fileBoundX, fileBoundY, fileBoundX+abs(bubXMax-fileBoundX)+1000, fileBoundY+abs(bubYMax-fileBoundY)+650, fill='#2c3e50')
    draw(canvas, width, height)
    #canvas.create_text(fileBoundX+40, 20, text='Name: '+perName, font = 'Courier 20 bold', fill='white')
    #canvas.create_text(fileBoundX + 40, 60, text='Topic: '+topName, font = 'Courier 20 bold', fill='white')
    #canvas.create_text(fileBoundX + 40, 100, text="Lecturer's Name: "+profName, font = 'Courier 20 bold', fill='white')
    canvas.postscript(file = "outputNotes.ps", x= fileBoundX, y = fileBoundY, width = abs(bubXMax-fileBoundX)+1000, height = abs(bubYMax-fileBoundY)+650, colormode='color')
    root.withdraw()
    os.system("open '/Users/kushamaharshi/Desktop/TERM PROJECT!/tp1/outputNotes.ps'")
    #root.mainloop()
    print("Thank You!")



##Making main bubble list

finalLabelledArray = []
finalPOSArray = []

bifBubbles, bifIndices, bifJumps, bifPrecSents = [], [], [], []

punctuatedString = ""

def makeMainList():
    """AUDIO_FILE = "/Users/kushamaharshi/Desktop/TERM PROJECT!/tp1/lastSavedFile.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    
    
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        testString = r.recognize_google(audio)
    
        #testString = r.recognize_google(audio)
        print("You said: " + testString)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))"""
        
        #above code from uberi, github
    """testString = "Species are different varieties of animals. They are formed over a long time. They can interbreed. Just need some words here. This happens only if you act like a bad person. If you have more money, due to increased sense of security, then you automatically have more happiness. They have differences in color, size, strength, gender roles, etcetera. There are three ways to do this. first, we can charge. Still talking about first here. still going bleh. Second, we can dance. Droning about second here. still going bleh. Hello people of earth. Third, we can sing. still going bleh. Singing like shit. Going on about the same old thing. Okay, moving on. Life is good. This can be done in four ways: swimming, charging, dancing, liking, making and bathing, if for whatever reason. This is a nice thing to do. Although there is a lot of controversy about this issue, it is still not acted upon by the government. Whenever I go on a walk, I like to get some food, milk and pizza.
    
    testString = "there are four types of biological diversity first is species diversity every ecosystem contains a unique collection of species all interacting with each other secondly genetic diversity describes how closely related the members of one species are in a given ecosystem third consider ecosystem diversity a region may have several ecosystems, or it may have one wide expanses of oceans or deserts would be examples of regions with low ecological diversity fourth is functional diversity understanding an ecosystem’s functional diversity can be useful to ecologists trying to conserve or restore damaged it okay let’s move on by examining the similarities and differences of different lineages that are related, scientists can determine most likely when the species diverged and evolved compared to when the common ancestor was around since biological species concept is dependent upon reproductive isolation of reproducing species it cannot necessarily be applied to a species that reproduces asexually the lineage species concept does not have that restraint and therefore can be used to explain simpler species that do not need a partner to reproduce the five types of species interactions are predation competition parasitism mutualism and commensalism to conclude showing a bit of math here five hundred seventy six is twenty four times twenty four"""
    
    testString = "Biological diversity in an environment is indicated by numbers of different species of plants and animals. Essentially you could say that there are four types of biological diversity. First is species diversity. Every ecosystem contains a unique collection of species, all interacting with each other. Secondly, genetic diversity describes how closely related the members of one species are in a given ecosystem. Third consider ecosystem diversity. A region may have several ecosystems, or it may have one. Wide expanses of oceans or deserts would be examples of regions with low ecological diversity. Fourth is functional diversity. Understanding an ecosystem’s functional diversity can be useful to ecologists trying to conserve or restore damaged it. Okay, let’s move on. By examining the similarities, likes and differences of different lineages that are related, scientists, researchers and explorers can determine most likely when the species diverged and evolved compared to when the common ancestor was around. Since biological species concept is dependent upon reproductive isolation of reproducing species, it cannot necessarily be applied to a species that reproduces asexually. The lineage species concept does not have that restraint and therefore can be used to explain simpler species that do not need a partner to reproduce. Species have five types: predation, competition, parasitism, mutualism and commensalism. To conclude,showing a bit of math here. Also note that two thousand seventy four added to sixty four is not equal to twenty four times twenty four right. I would also like to say this project was made possible thanks to the wonderful support of my TP mentor and all the faculty and staff of 15-112. Subsequently, I had super fun doing this!"
    
    testString1 = "biological diversity in an environment as indicated by numbers of different species of plants and animals essentially you could say that there are four types of biological diversity first is species diversity every ecosystem contains a unique collection of species all interacting with each other secondly genetic diversity describes how closely related the members of one species are in a given ecosystem third consider ecosystem diversity a region may have several ecosystems, or it may have one wide expanses of oceans or deserts would be examples of regions with low ecological diversity fourth is functional diversity understanding an ecosystem’s functional diversity can be useful to ecologists trying to conserve or restore damaged it okay let’s move on by examining the similarities and differences of different lineages that are related, scientists can determine most likely when the species diverged and evolved compared to when the common ancestor was around since biological species concept is dependent upon reproductive isolation of reproducing species it cannot necessarily be applied to a species that reproduces asexually the lineage species concept does not have that restraint and therefore can be used to explain simpler species that do not need a partner to reproduce the five types of species interactions are: predation, competition parasitism mutualism and commensalism to conclude showing a bit of math here. five hundred seventy six is twenty four times twenty four" 
    
    testString = convertToSymbols(testString)
    
    """data = {'text': testString}
    req = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
    punctuatedString = req.text
    print(punctuatedString)"""
    
    punctuatedString = testString
    
    tstart = sent_tokenize(punctuatedString)
    sstart = []
    toRemove = []
    for sent in tstart:
        #print("sent start")
        tg = nltk.word_tokenize(sent)
        for j in range(6, 3, -1):
            #print(str(j)+"grams")
            aGram = ngrams(tg, j)
            for i in aGram:
                #print(i)
                boolNFU = newFindUseless(i)
                #print()
                if(boolNFU==True):
                    toRemove.append(i)
                    
    #print("toREMOVE: ", toRemove)
    
    for remPhrase in toRemove:
        stringCon = ' '.join(remPhrase) + " "
        punctuatedString = punctuatedString.replace(stringCon, "")
        
    #punctuatedString = convertToSymbols(punctuatedString)
        
    finalPOSArray = tagPreprocess(punctuatedString)
    #print("fpA: ", finalPOSArray)
    ##
    global bifBubbles, bifIndices, bifJumps, bifPrecSents
    
    bifBubbles, bifIndices, bifJumps, bifPrecSents = checkBubBifA(finalPOSArray)
    
    ##
    
    #print('********************8bifBubbles!!!!!!!!!!: ', bifBubbles)
        
    testStrsentp = sent_tokenize(punctuatedString)
    
    testStrsentp = [nltk.word_tokenize(sent) for sent in testStrsentp]
    
    
    for aSentence in testStrsentp:
        finalLabelledArray.append(labeler(aSentence))
    
    
    indexi = 0
    
    while(indexi <= len(testStrsentp)-1):
        sentence = testStrsentp[indexi]
        
        if(indexi in bifIndices):
            #print("BIFHERE")
            bifIndex = bifIndices.index(indexi)
            #print("bifindex: ", bifIndex)
            bifYChange = getBifYChange(bifBubbles[bifIndex])
            bifYActual = getBifYMax(bifBubbles[bifIndex])
            #print("bify: ", bifYChange)
            curBubble = Bubble("bif", sentence, getColorProper(indexi), bifIndex, bifYChange, bifYActual)
            indexi+=1
            #print("bj", bifJumps)
            indexi+=bifJumps[bifIndex]
        else:
            chunkedSent = chunker(labeler(sentence))
            for chunk in chunkedSent:
                type, sent = chunk[0], chunk[1]
                
                curBubble = Bubble(type, sent, getColorProper(indexi))
            indexi+=1
        
##CALLING MAIN FUNCTION
def main():
    makeMainList()
    runDrawing(700, 700)
    
def resetFunc():
    global finalLabelledArray, finalPOSArray, bifBubbles, bifIndices, bifJumps, bifPrecSents, punctuatedString
    finalLabelledArray = []
    finalPOSArray = []
    bifBubbles, bifIndices, bifJumps, bifPrecSents = [], [], [], []
    punctuatedString = ""
    

if __name__ == "__main__":
    #main(perName, topName, profName)
    main()

