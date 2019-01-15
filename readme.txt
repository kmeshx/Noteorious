README

Required modules for the application:

Tkinter
NLTK (Natural Language Toolkit)
pyaudio
wave
time (only import required)
shutil
PIL
speech_recognition 
itertools
requests
os (only import required)
word2number (only import required)
An API key for using Google’s Speech API


This application primarily makes use of a couple of functions (essentially only part of speech tagging) from the NLTK module. 
Tkinter is used to build the user interface.
Pyaudio and speech_recognition (from Python) are used for for processing audio into audio and text files. 
PIL is used only used for displaying the image on start screen.
The requests module is needed for punctuating the raw, unpunctuated text received from Google’s speech-to-text API. 
os is used for saving/renaming/copying the contents of the chosen audio file to upload.
word2number is used to assist in conversion of Math while speaking to numbers and mathematical operators. 

In order to run the application on a computer, import the modules mentioned above. *Note that the longest, main drawing and declaring main list file with 800 lines in the application is ‘wholeTryWithImg’.

The output of the program is in the form of a postscript file that is saved to the computer and directly opened by the default pdf viewer as pdf.  


Project Description: The application ‘Note-orious’ :
takes in an audio input,
converts it to text, 
calls a punctuator to punctuate the text,
performs operations on the text using techniques of Natural Language Processing such as part of speech tagging and chunking, 
creates a class of containers (bubbles) to display the resultant notes,
runs a draw function over each bubble object in the list of bubbles that is an attribute of the Bubble class, 
And finally returns a corresponding postscript file that is automatically viewed as pdf.
