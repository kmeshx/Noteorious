##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project

from tkinter import *
from tkinter import PhotoImage
import time
import pyaudio
import wave
import os
from shutil import copyfile
from tkinter import filedialog
from tkinter import font
from wholeTryWithImg import *

##menu screen created here



##create start BG Image

from PIL import Image
from PIL import *

rectangle_height = 650
rectangle_width = 1000

##finds corner bounds for rounded rectangles
def satisfiesEquation(x, y, mult=0.2, rectHeight = rectangle_height, rectWidth = rectangle_width):
    
    cx, cy = inConcernedBounds(x, y)
    tolerence = 0.5
    radius = mult*min(rectHeight, rectWidth)
    satBool = (x-cx)**2 + (y-cy)**2 <=\
    (radius+tolerence)**2
    
    return satBool
    
def inConcernedBounds(x, y, tl=(0, 0), tr=(rectangle_width, 0), br=(rectangle_width, rectangle_height), bl=(0, rectangle_height), rectHeight = rectangle_height, rectWidth = rectangle_width, mult=0.2):
    
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

##creates rounded rectangles with gradient from scratch
def createMyImage(rectangle_height, rectangle_width, curRV, graddivR, curBV, graddivB, curGV, graddivG, step):
    
    rgbList = []
    
    for i in range(rectangle_height):
        if(i%step==0):
            curRV-=graddivR
        rgbList.append((curRV, 0, 0))
        
    for j in range(rectangle_height):
        if(j%step==0):
            curGV-=graddivG
        #curGV-=random.choice([1, 2])
        rgbList[j] = (curRV, curGV, 0)
        
    for k in range(rectangle_height):
        if(k%step==0):
            curBV-=graddivB
        rgbList[k] = (curRV, curGV, curBV)
    
    finalList = []   
    for l in range(rectangle_height):
        for ll in range(rectangle_width):
        
            if(inConcernedBounds(ll, l) != False):
                
                if(satisfiesEquation(ll, l)):
                    finalList.append(rgbList[l])
                else:
                    finalList.append((255, 255, 255))
            else:
                finalList.append(rgbList[l])
                    
    
    myStartBGImage = Image.new('RGB',(rectangle_width, rectangle_height))
    pixels = list(finalList)
    myStartBGImage.putdata(pixels)
    myStartBGImage.save('startScreenBG3.gif', "GIF")
    
    
    #return myStartBGImage

####################

##solid rounded rectangles

def roundedRect(canvas, topLeftX, topLeftY, length, breadth, colorHere):
    m=1/6
    canvas.create_arc(topLeftX, topLeftY, topLeftX+length*m, topLeftY+breadth*m, start=90, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    canvas.create_arc(topLeftX+length-length*m, topLeftY, topLeftX+length, topLeftY+breadth*m, start=0, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    canvas.create_arc(topLeftX+length-length*m, topLeftY+breadth, topLeftX+length, topLeftY+breadth-breadth*m, start=270, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    canvas.create_arc(topLeftX, topLeftY+breadth-breadth*m, topLeftX+length*m, topLeftY+breadth,start=180, extent=90, outline=colorHere, style="pieslice", fill=colorHere, width = 3)
    
    canvas.create_rectangle(topLeftX, topLeftY+breadth*m/2, topLeftX+length, topLeftY+breadth-breadth*m/2, fill=colorHere, outline=colorHere, width = 3)
    
    canvas.create_rectangle(topLeftX+length*m/2, topLeftY, topLeftX+length-length*m/2, topLeftY+breadth, fill=colorHere, outline=colorHere, width = 3)

##draw ruled page on menu screen
def drawRuledPage(canvas, data):
    textToDisplay = """Instructions:\nHello there! Looks like you are feeling a bit note-orious…\n
Let’s get started then!\nClick on ‘Record Audio’ to record your lecture/revision and\n let Note-orious generate beautiful\n notes for you.\nClick on ‘Upload Audio’ to use an audio file\n to generate notes.\nClick on ‘Exit’ to close the application. \n\nAnd don’t forget, you may want\n to help Note-orious help you better! \nIf you want to start a list,\n say something like,\n 'there are three ways to do this’,\n and preferably use ‘first’, ’second’,\n etc. as indicators.\n To end enumerating a list, say something \n like “moving on”, or ‘okay, let’s move on’,\n or better still 'Bingo!'…\n\nAnd you are good to go!"""

    instrucArray = textToDisplay.split("\n")
    
    lenPage = 3*data.width/4
    
    canvas.create_rectangle(0, 0, lenPage, data.height, fill="#bbff33", outline='')
    numlines = 25
    lineGap = data.height//numlines
    for i in range(numlines):
        yPos = i*lineGap
        canvas.create_line(0, yPos, lenPage, yPos, fill="#333300")
        font1 = font.Font(family = "courier", size = 18, weight='bold')
        if(i < len(instrucArray)):
            canvas.create_text(10, (i+1)*lineGap, text = instrucArray[i], font = 'courier 20 bold', fill = '#003300', anchor = 'nw')
    
def drawRightWhite(canvas, data):
    
    lenPage = 3*data.width/4
    
    canvas.create_rectangle(lenPage, 0, data.width, data.height, fill="white", outline='')
    
def drawThreeButtons(canvas, data):
    
    #lenPage = 3*data.width/4
    length, breadth = 150, 60
    
    # x1, y1 = lenPage-length/2, data.height/4
    # x2, y2 = lenPage-length/2, 2*data.height/4
    # x3, y3 = lenPage-length/2, 3*data.height/4
    roundedRect(canvas, data.x2, data.y2, length, breadth, "#004d00")
    roundedRect(canvas, data.x3, data.y3, length, breadth, "#004d00")
    
    
    canvas.create_text(data.x2+5, data.y2+5, text="UPLOAD \n AUDIO", font = "calibri 20 bold", fill="white", anchor="nw")
    canvas.create_text(data.x3+5, data.y3+5, text="EXIT", font = "calibri 20 bold", fill="white", anchor="nw")
    
    
    
    #if(data.isRecording==False):
    roundedRect(canvas, data.x1, data.y1, length, breadth, "#004d00")
    canvas.create_text(data.x1+5, data.y1+5, text="RECORD \n AUDIO", font = "calibri 20 bold", fill="white", anchor="nw")
    """else:
        roundedRect(canvas, data.x1, data.y1, length, breadth, "#004d00")
        canvas.create_text(data.x1+5, data.y1+5, text="Press 's' \n to stop", font = "calibri 20 bold", fill="white", anchor="nw")"""
    
    
    
def onButton1(event, data):
    length, breadth = 150, 60
    if((data.x1 <= event.x<= data.x1+length) and (data.y1 <= event.y <= data.y1+breadth)):
        return True
    return False
    
def onButton2(event, data):
    length, breadth = 150, 60
    if((data.x2 <= event.x<= data.x2+length) and (data.y2 <= event.y <= data.y2+breadth)):
        return True
    return False
    
def onButton3(event, data):
    length, breadth = 150, 60
    if((data.x3 <= event.x<= data.x3+length) and (data.y3 <= event.y <= data.y3+breadth)):
        return True
    return False

def recFinished(canvas, data):
    canvas.create_text(30, (data.height*9.5)/10, text=data.finishRecSig, anchor = 'nw', font="calibri 8 bold", fill='#003300')    

def drawMenuScreen(canvas, data):
    #print("menu")
    
    drawRuledPage(canvas, data)
    drawRightWhite(canvas, data)
    drawThreeButtons(canvas, data)
    recFinished(canvas, data)
    
def init(data):
    #data.mode= "start"
    data.curTime = 0
    data.lenPage = 3*data.width/4
    length, breadth = 150, 60
    data.isRecording = False
    data.finishRecSig = ""
    data.openFile = False
    data.file_pathhere = ''
    
    data.x1, data.y1 = data.lenPage-length/2, data.height/4
    data.x2, data.y2 = data.lenPage-length/2, 2*data.height/4
    data.x3, data.y3 = data.lenPage-length/2, 3*data.height/4
    
    data.selfName = ''
    data.topicName = ''
    data.profName = ''

def mousePressed(event, data):
    if(onButton1(event, data)):
        
        
        data.isRecording = True
        print("RC", data.isRecording)
        length, breadth = 150, 60
        
        
        FORMAT = pyaudio.paInt16
        
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 6
        
        WAVE_OUTPUT_FILENAME = "lastSavedFile.wav"
        
        audio = pyaudio.PyAudio()
        
        # start Recording
        
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print("recording...")
        frames = []
        
        start_time = time.time()
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            #print(time.time())
            if(data.isRecording==False):
                # stop Recording
                print(time.time())
                stream.stop_stream()
                stream.close()
                audio.terminate()
                break
            dataS = stream.read(CHUNK)
            frames.append(dataS)
        print("finished recording")
        data.finishRecSig = 'Finished Recording!'
        
        print("siged")
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
        print("waved")
        #data.finishRecSig = 'Generating File'
        """data.selfName = input('Please enter your name:')
        data.topicName = input('Please enter the topic of the audio:')
        data.profName = input("Please enter the lecturer's name:")"""
        import wholeTryWithImg
        #main(data.selfName, data.topicName, data.profName)
        #import wholeTryWithImg
        main()
        print("imported")
        data.finishRecSig = 'Done!'
        resetFunc()
        
    elif(onButton2(event, data)):
        data.openFile = True
        #file_pathhere = filedialog.askopenfilename()
        #root.update()
        #data.file_pathhere = filedialog.askopenfilename()
        #from tkinter import *
        from tkinter import filedialog
        #root2 = Tk()
        #root2.withdraw()
        data.file_pathhere = filedialog.askopenfilename()
        
        #file_read = file.read()
        copyfile(data.file_pathhere, "lastSavedFile.wav")
        #data.finishRecSig = 'Generating File'
        #canvas.create_text(30, (data.height*9)/10, text='Generating File', anchor = 'nw', font="calibri 28 bold", fill='#003300') 
        #pb = ttk.Progressbar(root,orient ="horizontal",length = 200, mode ="indeterminate")
        """data.selfName = input('Please enter your name:')
        data.topicName = input('Please enter the topic of the audio:')
        data.profName = input("Please enter the lecturer's name:")"""
        import wholeTryWithImg
        main()
        data.finishRecSig = 'Done!'
        
        resetFunc()
        
        #os.rename(, filename[7:])
        
        
    elif(onButton3(event, data)):
        exit()
        #root.destroy()
        #ds

def keyPressed(event, data):
    if(data.isRecording==True):
        if(event.keysym=='s'):
            
            data.isRecording = False
            print("RC", data.isRecording)
    else:
        if(event.keysym=="p"):
            print("BLEH")
        
    
    

def timerFired(data):
    data.curTime+=100 #milliseconds

def redrawAll(canvas, data):
    
    drawMenuScreen(canvas, data)
    # if(data.openFile == True):
    #     data.file_pathhere = filedialog.askopenfilename()
        
    

####################################
# use the run function as-is (from 15-112 WEBSITE)
####################################

def runSS(width=1000, height=650):
    
    
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        #canvas.create_rectangle(0, 0, data.width, data.height,
                                #fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    
    
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    
    
    
    timerFiredWrapper(canvas, data)
    
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


#run(1000, 650)