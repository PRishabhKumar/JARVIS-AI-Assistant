import pyttsx3
import speech_recognition as sr
import pyaudio
import eel 
from datetime import datetime
import time
import re 
import threading
from word2number import w2n
from API_KEYS import api_keys
# this is used to prevent simultaneous microphone usage by hotwords detection as well as takeCommand() function
mic_lock_event = threading.Event()
mic_lock_event.set()  # Initially set, allowing hotword detection



@eel.expose
def speak(string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Lower value = slower speech
    eel.displayMessage(string)
    engine.say(string)
    eel.recieversMessage(string) # display whatever JARVIS speaks to us in the chat history
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        eel.displayMessage("Listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 30, 10)  # Listen for 30s max, or 10s if silent
        try:
            print("Recognizing....")
            eel.displayMessage("Recognizing....")
            string = r.recognize_google(audio, language="en-in")
            print(f'User said : {string}')            
            eel.displayMessage(string)            
            return string
        except Exception as e:
            print(f'The following error occurred: {e}')    
            eel.displayMessage("Sorry, I didn't catch that.")
            return ""  # return empty string to avoid NoneType issues


# Main command handler
@eel.expose
def commands(message=1):     
    try:        
        if(message==1):    
            from BACK_END.features import greetings as greet_func
            greet_func()
            speak("How may I help you today ?")        
            command = takeCommand() # if the value of the message is 1 i.e. no message has been recieved from the chatbox, then take the query from the mic
            eel.sendersMessage(command) # display whatever we speak to JARVIS in the chat history
        else:
            command = message # if a message is recieved from the chatbox, make that message as the query and start processin
            eel.sendersMessage(command) # display whatever we speak to JARVIS in the chat history
            
            
        # testing for the command to open some app or website
        if command and "open" in command:
            # this will distinguis the opening of other apps and whatsapp
            if("whatsapp" in command.lower() or "my chats" in command):
                from BACK_END.features import handleWhatsapp
                handleWhatsapp(command)
            else:
                from BACK_END.features import open
                open(command)    
        # testing for the command to play something on youtbe
        elif (re.search(r'play\s+(.*?)\s+on\s+youtube', command.lower())):
            from BACK_END.features import searchAndPlayOnYT
            searchAndPlayOnYT(command)            
        elif("on youtube" in command.lower()):
            from BACK_END.features import playOnYT
            playOnYT(command)
        elif "play some music" in command.lower() or "play songs" in command.lower() or "play some songs" in command.lower():    
            from BACK_END.features import playMusic
            playMusic(command)
        elif("set an alarm for" in command.lower() or "wake me up at" in command.lower()):
            from BACK_END.features import alarmClock
            alarmClock(command)    
        elif("weather in" in command.lower()):
            from BACK_END.features import getWeather
            getWeather(command)  
        elif("generate a password" in command.lower() or "create a password" in command.lower()):
            speak("Sure sir I can generate a password for you")
            speak("Please tell me the length of the password you want : ")
            try:
                length =  w2n.word_to_num(takeCommand()) 
                eel.sendersMessage(command) # display whatever we speak to JARVIS in the chat history    
                from BACK_END.features import handlePasswordGeneration
                handlePasswordGeneration(length)                     
            except Exception as e:
                speak("Please say a valid number. Try again")
        elif("call" in command.lower() or "make a call" in command.lower()):
            from BACK_END.features import phoneCall
            phoneCall(command) 
        elif("unlock my phone" in command.lower()):
            from BACK_END.features import unlockPhone
            unlockPhone()
        elif("check my notifications" in command.lower() or "open notifications" in command.lower() or "show my notifications" in command.lower()):
            from BACK_END.features import notifications
            notifications()                   
        else:
            from BACK_END.features import setup_model
            model = setup_model(api_keys.geminiAPI)
            from BACK_END.features import chat_with_ai
            chat_with_ai(model, command)                      
    except Exception as e:
        speak(f"The following error occurred: {e}")
        
    eel.displayHood()    
