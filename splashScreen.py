##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


from tkinter import *
from tkinter import PhotoImage
import time
from startScreen import *



##create start BG Image

from PIL import Image
from PIL import *

rectangle_height = 650
rectangle_width = 1000


def drawStartScreen(canvas, data):
    
    mybgimg = PhotoImage(file="TPBGF.gif")
    labelBG = Label(image=mybgimg)
    labelBG.image = mybgimg # keep a reference! (CITE: stackoverflow)
    labelBG.place(x=0, y=0)
    #time.sleep(5)
    if(4999 <= data.curTime <= 5001):
        #print("AAe le")
        canvas.delete("all")
        labelBG.pack_forget()
        labelBG.config(image='')
        labelBG.destroy()
        data.mode="dead"
        runSS()
        exit()
    

def init(data):
    data.mode= "start"
    data.curTime = 0

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    data.curTime+=100 #milliseconds

def redrawAll(canvas, data):
    
    if(data.mode=="start"):
        drawStartScreen(canvas, data)
    else:
        pass
        
    

####################################
# use the run function as-is (15-112) citation
####################################

def run(width=1000, height=650):
    
    
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





def service_func():
    run(1000, 650)


if __name__ == '__main__':
    # service.py executed as script
    # do something
    service_func()
    #kmtp2o.runDrawing(700, 700)