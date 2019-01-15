##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


##TO CREATE GRADIENTED RECTANGLES

from tkinter import *
from tkinter import font
import random
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import *
from nltk import ngrams
from PIL import Image
from PIL import *

def satisfiesEquation(x, y, rectHeight, rectWidth, mult=0.2):
    cx, cy = inConcernedBounds(x, y, (0, 0), (rectWidth, 0), (rectWidth, rectHeight), (0, rectHeight), rectHeight, rectWidth)
    tolerence = 0.5
    radius = mult*min(rectHeight, rectWidth)
    satBool = (x-cx)**2 + (y-cy)**2 <=\
    (radius+tolerence)**2
    
    return satBool
    
def inConcernedBounds(x, y, tl, tr, br, bl, rectHeight, rectWidth, mult=0.2):
    
    radius = mult*min(rectHeight, rectWidth)
    cx1, cy1 = tl[0] + radius, tl[1] + radius
    cx2, cy2 = tr[0] - radius, tr[1] + radius
    cx3, cy3 = br[0] - radius, br[1] - radius
    cx4, cy4 = bl[0] + radius, bl[1] - radius 
    bool1 = ((tl[0] <= x <= cx1) and (tl[1] <= y <= cy1))
    bool2 = ((tr[0] >= x >= cx2) and (tr[1] <= y <= cy2))
    bool3 = ((br[0] >= x >= cx3) and (br[1] >= y >= cy3))
    bool4 = ((bl[0] <= x <= cx4) and (bl[1] >= y >= cy4))
    if(bool1 == True):
        return cx1, cy1
    if(bool2 == True):
        return cx2, cy2
    if(bool3 == True):
        return cx3, cy3
    if(bool4 == True):
        return cx4, cy4
    return False

def createMyImage(canvas, x1, y1, rectangle_height, rectangle_width, cValues, step):
    
    (curRV, graddivR, curBV, graddivB, curGV, graddivG) = cValues
    rgbList = []
    
    for i in range(int(rectangle_height)):
        if(i%step==0):
            curRV-=graddivR
            if(curRV<0):
                curRV = 10
        
        hexcode = '#%02x%02x%02x' % (curRV, 0, 0)
        #print(hexcode)
        rgbList.append(hexcode)
        
    for j in range(int(rectangle_height)):
        if(j%step==0):
            curGV-=graddivG
            if(curGV<0):
                curGV = 10
        hexcode = '#%02x%02x%02x' % (curRV, curGV, 0)
        #print(hexcode)
        rgbList[j] = hexcode
        
    for k in range(int(rectangle_height)):
        if(k%step==0):
            curBV-=graddivB
            if(curBV<0):
                curBV = 10
                
        hexcode = '#%02x%02x%02x' % (curRV, curGV, curBV)
        #print(hexcode)
        rgbList[k] = hexcode
    
    
     
    for l in range(int(rectangle_height)):
        for ll in range(int(rectangle_width)):
        
            if(inConcernedBounds(ll, l, (0, 0), (rectangle_width, 0), (rectangle_width, rectangle_height), (0, rectangle_height), rectangle_height, rectangle_width) != False):
                
                if(satisfiesEquation(ll, l, rectangle_height, rectangle_width)):
                    canvas.create_line(x1+ll, y1+l, x1+ll+1, y1+l, fill = rgbList[l])
                
            else:
                canvas.create_line(x1+ll, y1+l, x1+ll+1, y1+l, fill = rgbList[l])