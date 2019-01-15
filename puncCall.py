##NAME: KUSHA MAHARSHI

##SECTION: D

##FALL 2017

##15-112 Term Project


import requests
import speech_recognition as sr  

AUDIO_FILE = "/Users/kushamaharshi/Desktop/TERM PROJECT!/tp1/lastSavedFile.wav"

#code from google usage for uri, not used
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Print the first alternative of all the consecutive results.
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
        
        
transcribe_gcs("/Users/kushamaharshi/Desktop/TERM PROJECT!/tp1/lastSavedFile.wav")



r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file


# Speech recognition using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    #testString = r.recognize_google(audio, key='AIzaSyBN---qwBodUX49pdbF0NNsGn00DnV9HPA')
    testString = r.recognize_google(audio, key="APIKeyFinal")

    #testString = r.recognize_google(audio)
    print("You said: " + testString)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    
testString = "there are four types of biological diversity first is species diversity every ecosystem contains a unique collection of species all interacting with each other secondly genetic diversity describes how closely related the members of one species are in a given ecosystem third consider ecosystem diversity a region may have several ecosystems, or it may have one wide expanses of oceans or deserts would be examples of regions with low ecological diversity fourth is functional diversity understanding an ecosystem’s functional diversity can be useful to ecologists trying to conserve or restore damaged it okay let’s move on by examining the similarities and differences of different lineages that are related, scientists can determine most likely when the species diverged and evolved compared to when the common ancestor was around since biological species concept is dependent upon reproductive isolation of reproducing species it cannot necessarily be applied to a species that reproduces asexually the lineage species concept does not have that restraint and therefore can be used to explain simpler species that do not need a partner to reproduce the five types of species interactions are predation competition parasitism mutualism and commensalism to conclude showing a bit of math here five hundred seventy six is twenty four times twenty four"    

"""data = {'text': testString}
req = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
punctuatedString = req.text
print(punctuatedString)"""

result = """There are four types of biological diversity. First is species diversity. Every 
ecosystem contains a unique collection of species all interacting with each othe
r. Secondly, genetic diversity describes how closely related the members of one 
species are in a given ecosystem. Third consider ecosystem diversity. A region m
ay have several ecosystems, or it may have one wide expanses of oceans, or deser
ts would be examples of regions with low ecological diversity. Fourth is functio
nal diversity. Understanding an ecosystem’s functional diversity can be useful t
o ecologists, trying to conserve or restore damaged it. Okay, let’s move on by e
xamining the similarities and differences of different lineages that are related
. Scientists can determine most likely when the species diverged and evolved com
pared to when the common ancestor was around. Since biological species concept i
s dependent upon reproductive isolation of reproducing species, it cannot necess
arily be applied to a species that reproduces asexually. The lineage species con
cept does not have that restraint and therefore can be used to explain simpler s
pecies that do not need a partner to reproduce. The five types of species intera
ctions are predation competition, parasitism, mutualism and commensalism. To con
clude, showing a bit of math here, five hundred seventy six is twenty four times
 twenty four """