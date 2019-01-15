##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


from PIL import Image
from PIL import *
from tkinter import *
from tkinter import font
import textwrap
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


#lightDarkColDic = {'red': '#ff8080', 'orange': '#ffcc99', 'yellow': '#ffff99', 'green':'#cccc33', 'blue': '#80bfff'}
lightDarkColDic = {'red': ['#ffe6e6', '#ffcccc'], 'blue': ['#ccefff', '#e6f7ff'], 'green':['#e6ffe6', '#ccffcc'], 'yellow': ['#ffffe6', '#ffffcc'], 'orange': ['#ffe6cc', '#ffdab3']}

globalColorsList = ["red", "blue", "green", "yellow", "orange"]

##Rounded rectangles to make things look pretty

def roundedRect(canvas, topLeftX, topLeftY, length, breadth, colorHere):
    m=1/6
    canvas.create_arc(topLeftX, topLeftY, topLeftX+length*m, topLeftY+breadth*m, start=90, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    
    canvas.create_arc(topLeftX+length-length*m, topLeftY, topLeftX+length, topLeftY+breadth*m, start=0, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    
    canvas.create_arc(topLeftX+length-length*m, topLeftY+breadth, topLeftX+length, topLeftY+breadth-breadth*m, start=270, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    
    canvas.create_arc(topLeftX, topLeftY+breadth-breadth*m, topLeftX+length*m, topLeftY+breadth,start=180, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    
    canvas.create_rectangle(topLeftX, topLeftY+breadth*m/2, topLeftX+length, topLeftY+breadth-breadth*m/2, fill=colorHere, outline=colorHere, width = 3)
    canvas.create_rectangle(topLeftX+length*m/2, topLeftY, topLeftX+length-length*m/2, topLeftY+breadth, fill=colorHere, outline=colorHere, width = 3)
    
    
##thought bubbles for causality :)

def thoughtBubble(canvas, topLeftX, topLeftY, toX, toY, length, height, colorHere):
    
    dColor = lightDarkColDic[colorHere][0]
    lColor = lightDarkColDic[colorHere][1]
    
    
    m = 1/8
    perRadX = length/4
    canvas.create_polygon(topLeftX+length-length*m, topLeftY+height, topLeftX+length, topLeftY+height-height*m, toX, toY, fill=colorHere, outline="")
    createConc(canvas, topLeftX, topLeftY, topLeftX+2*perRadX, topLeftY+height, dColor, lColor)
    createConc(canvas, topLeftX+2*perRadX, topLeftY, topLeftX+4*perRadX, topLeftY+height, dColor, lColor)
    createConc(canvas, topLeftX+perRadX, topLeftY, topLeftX+3*perRadX, topLeftY+height, dColor, lColor)
    
   
    
def trblThoughtBubble(canvas, topLeftX, topLeftY, toX, toY, length, height, colorHere):
    
    dColor = lightDarkColDic[colorHere][0]
    lColor = lightDarkColDic[colorHere][1]
    
    m = 1/8
    perRadX = length/4
    
    canvas.create_polygon(topLeftX, topLeftY+height-height*m, topLeftX+length*m, topLeftY+height, toX, toY, fill=colorHere, outline="")
    createConc(canvas, topLeftX, topLeftY, topLeftX+2*perRadX, topLeftY+height, dColor, lColor)
    createConc(canvas, topLeftX+2*perRadX, topLeftY, topLeftX+4*perRadX, topLeftY+height, dColor, lColor)
    createConc(canvas, topLeftX+perRadX, topLeftY, topLeftX+3*perRadX, topLeftY+height, dColor, lColor)
    
   
def createConc(canvas, x1, y1, x2, y2, dColor, lColor):
    ow = min(abs(x1-x2), abs(y1-y2))*(1/5)
    
    canvas.create_oval(x1, y1, x2, y2, fill=dColor, outline='')

    for i in range(1,6):
        
        if(i%2== 0):
            canvas.create_oval(x1+ow*i, y1+ow*i, x2-ow*i, y2-ow*i, fill='', outline=lColor, width=ow)
                

##colors generator

def getAColor(colorlist):
    l = len(colorlist)
    index = random.randint(0, len(colorlist)-1)
    return colorlist[index]
    
def getColorProper(anIndex):
    colorIndex = anIndex%5
    retColor = globalColorsList[colorIndex]
    return retColor
    
##custom create text method

        
def getDisplayHeight(inptext):
    wwidth, wheight = 700, 700
    removeX = 4*wwidth/15
    removeY = wheight/10
    yHeight = 60
    customFontSize = 14
        
    #arialmeasure = font.Font(family='Arial', size=customFontSize, weight='bold')
    
    threshWidth = (wwidth-removeX)//(3*8.6)
    #textWidth = arialmeasure.measure(inptext)
    #textHeight = arialmeasure.metrics("linespace")
    textHeight = 19
    #print("win: ", arialmeasure.metrics("linespace"))
    dispHeight = textHeight*len(textwrap.wrap(inptext, width = threshWidth))
    
    if(dispHeight<=yHeight):
        dispHeight = yHeight

        
    finalString = '\n'.join(textwrap.wrap(inptext, width = threshWidth))
    
    return dispHeight+6, finalString

#print(getDisplayHeight("biological diversity in an environment as indicated by numbers of different species of plants and animals essentially you could say that there are four types of biological diversity first is species diversity every ecosystem contains a unique collection of species all interacting with each other secondly genetic diversity describes how closely related the members of one species are in a given ecosystem third consider ecosystem diversity a region may have several ecosystems,"))
        

def prettyText(canvas, inptext, posX, posY, fontFill):
    customFontSize = 14
    rectHeight, dispString = getDisplayHeight(inptext)
    xs = 0.07*rectHeight
    canvas.create_text(posX+xs+5, posY+xs+5, text = dispString, font="Arial "+str(customFontSize)+" bold", fill=fontFill, anchor = "nw")


        
