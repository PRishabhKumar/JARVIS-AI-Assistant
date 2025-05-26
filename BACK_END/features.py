import playsound as ps
import eel
import os
import pymongo
import webbrowser as wb
import datetime
import re
import pyautogui as gui
import pywhatkit as kit
from BACK_END.command import *
from BACK_END import musicLibrary
import pvporcupine
import struct
import pyaudio
import webbrowser
import pygame as py # for alarm clock
from datetime import datetime
import keyboard as kb
from API_KEYS import api_keys
import requests
import string
import random
import pyperclip
import hugchat
import pymongo
import google.generativeai as genai
import subprocess
def detectHotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"]) # this module has pre-trained hotword detection for the names 'JARIVS' and "Alexa"
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels = 1, format = pyaudio.paInt16, input=True, frames_per_buffer = porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h"*porcupine.frame_length, keyword)
            
            keyword_index = porcupine.process(keyword)
            
            # if any keyowords are detected....
            if(keyword_index>=0):
                print("Hotword detected !!")
                import pyautogui as gui # using pyautogui to simulate the pressing of win+j combination to activate JARVIS
                gui.keyDown("win") # press the win key
                gui.keyDown("j") # press the 'j' key
                time.sleep(2) # wait for some time for the key press to be registered
                gui.keyUp("win")  # lift up the win key
    except Exception as e:
        # cleaning up everything in case every thing goes well 
        if(porcupine is not None):
            porcupine.delete()
        if(audio_stream is not None):
            audio_stream.close()
        if(paud is not None):
            paud.terminate()    
        else:
            print(f"The following error occured : {e}")            



# Play start sound
@eel.expose
def playStartSound():
    try:
        sound_directory = r"FRONT_END\Assets\Audio\start_sound.mp3"
        print('Starting sound play !!')
        ps.playsound(sound_directory)
        print("Sound play complete !!!")
    except Exception as e:
        print("The following error occured : ", e)



# Greeting the user based on the current time

from datetime import datetime

def greetings():
    hour = int(datetime.now().strftime("%H"))
    if 4 <= hour < 12:
        speak("Good morning sir !!!")
    elif 12 <= hour <= 15:
        speak("Good afternoon sir !!!")
    elif 16 <= hour <= 23:
        speak("Good evening sir !!!")
    elif 0 <= hour < 4:
        speak("Good night sir, you should take some sleep now rather than being stuck on a computer screen at this time")



# Opening apps and websites using MongoDB database

def open(string):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['JARVIS']
    collection = db['JARVISCollection']

    try:
        appName = string.lower().split("open")[1].strip()
        appInfo = collection.find_one({'name': appName}, {"_id":0, "path":1}) # this returns the complete dictionary of that particular app and we want to get the value stored for the 'path' key
        if(not appInfo is None):
            speak(f"Opening {appName} sir")
            os.startfile(appInfo["path"])
        else:
            speak("Either the app or the path to the app was not found !!!")
            print("path not found !!")
    except Exception as e:
        speak("The following error occured : ", e)
        print(f"Some error occured : {e}")


# this function is used to get the name of the video we want to play on youtube from the query string given
def getVideoName(string):
    string = string.lower()
    pattern = r'play\s+(.*?)\s+on\s+youtube' # this re checks for the presence of the strings "play" and "on youtube" and in between there must be something that is the name of the video we want to play
    match = re.search(pattern, string, re.IGNORECASE)
    print(f"Video name : {match.group(1)}")
    return match.group(1) if match else None


def getVideoName1(string):
    string = string.lower()
    pattern = r'(?:play\s+(.*))|(?:(.*?)\s+on\s+youtube)'
    match = re.search(pattern, string)
    if match:
        video_name = match.group(1) or match.group(2)
        video_name = video_name.strip()
        print(f"Video name : {video_name}")
        return video_name
    else:
        print("No video name found.")
        return None



def searchAndPlayOnYT(string):
    string = getVideoName(string) # get the name of the video to be played
    print(f"Playing {string} on youtube sir....")
    kit.playonyt(string)
    
    
def playOnYT(string):
    os.startfile("https://www.youtube.com/") # open youtube
    time.sleep(5) # wait for the screen to stabilize
    gui.click(710, 132) # click on the search bar
    time.sleep(2) # wait for complete loading
    string = getVideoName1(string) # get the name of the video to be played
    gui.write(string, interval=0.05) # type the query in the search bar
    time.sleep(2) # wait for some time
    gui.press('enter') # press enter to search 
    
    
# function to accpet a string and identify the numbers present in it for selection of song number 

def check_for_integer_in_command(string):
    for character in string:
        if character.isdigit():
            return int(character)
    return None
    
# function to play songs using a local music library
def playMusic(string):    
    speak("Ok sir, opening the music library for you...")
    for i in range(len(musicLibrary.music_library_list)):        
        print(f"{i + 1}) {musicLibrary.folder_names[i]} ")
        print()    
    speak("Please select the folder number that you want to open..")
    folder_num = takeCommand()
    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
    #eel.getSenderMessages(choice)
    folder_number = check_for_integer_in_command(folder_num)
    
    try:
        num = 1
        if not folder_number + 1 == None:
            temp_folder = musicLibrary.music_library[folder_number]
            temp_folder_name = musicLibrary.folder_names[folder_number - 1]            
            speak(f"Ok sir, opening folder number {folder_number}...")            
            speak("Here are all the songs in the selecteed folder : ")
            if folder_number >= 1 and folder_number <= 4:                
                for song in musicLibrary.music_library_list[folder_number - 1]:
                    print(f"{num}) {song}")
                    num += 1                                       
                speak("Please select the song number from the list to play it...")
                song_num = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                #eel.getSenderMessages(choice)
                song_number = check_for_integer_in_command(song_num)
                for i in range(len(temp_folder)):
                    
                    if i + 1 == song_number:                        
                        speak(f"Ok sir, playing song number {song_number} from the selected folder...")
                        webbrowser.open(musicLibrary.music_library[folder_number][song_number])
    except Exception as e:        
        speak("Selected folder number does not exist")        
        speak("Some error occured..")        
        speak("Please try again...")        
        print(f"Error : {e}")
        
    
# function for whatsapp automation

def handleWhatsapp(string):
    speak("Opening whatsapp sir....")
    gui.press("win") # press the windows key to open the search bar 
    time.sleep(2) # wait for some time
    gui.write("whatsapp", interval=0.05) # type "whatsapp" into the search bar
    time.sleep(1)
    gui.press('Enter') # hit the enter key to open whatsapp
    speak("Please tell me what you want to do now sir....")
    string = takeCommand() # ask for the uer's query
    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
    if("send a message" in string.lower() or "message" in string.lower()):
        string = string.split("to")[1] # split the string from the first occurence of "to" and from the resultng list, select the second element i.e. the name of the person to whom the message is to be sent
        gui.click(253,  153) # click on teh search bar
        time.sleep(1)
        gui.write(string, interval=0.05) # type the name of the person in the search box
        time.sleep(2) # wait for the searches to stabilize
        gui.click(317, 222)# click on the first chat that appears after the search (i.e. the closest match)
        speak("Please speak out the message you want to send !!!")
        message = takeCommand()
        eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
        gui.click(799, 991) # click on the message input box
        time.sleep(1) # make sure the focus is correct on the message input box
        gui.write(message, interval=0.05) # write the message with an interval of 0.1 seconds after every character (looks cool)
        time.sleep(1) # wait for some time
        gui.press("Enter") # hit the enter key to send the message
        speak("Message sent sir....")
        speak("Do you wish to send another message sir ?")
        order = takeCommand()
        eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
        #eel.getSenderMessages(choice)
        while "yes" in order.lower():            
            speak("Do you want to send another message to the same person sir ??")
            order = takeCommand()
            eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
            #eel.getSenderMessages(choice)
            if "yes" in order.lower():                
                speak("Please speak out the message to be sent :")
                message = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                #eel.getSenderMessages(choice)
                gui.click(317, 222)  # Clicking on the chat to open it                
                speak("Please speak out the message to be sent :")
                order = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                #eel.getSenderMessages(choice)
                gui.click(799, 991)  # Click the message input box
                time.sleep(0.5)  # Ensure focus is on the message input box
                gui.write(order.lower(), interval=0.05)  # Typing the message
                gui.press('Enter')  # Hit the enter key to send the message                
                speak("Message sent sir...")                
                speak("Do you wish to send another message sir ??")
                order = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                #eel.getSenderMessages(choice)
                while "yes" in order.lower():                    
                    speak("Please speak out the message to be sent sir :")
                    order = takeCommand()
                    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                    #eel.getSenderMessages(choice)
                    gui.click(799, 991)  # Click the message input box
                    time.sleep(0.5)  # Ensure focus is on the message input box
                    gui.write(order.lower(), interval=0.05)  # Typing the message
                    gui.press('enter') #pressing enter to send the message
                    # gui.click(1884, 979)  # Clicking to send the message                    
                    speak("Message sent sir...")                    
                    speak("Do you wish to send another message sir ??")
                    order = takeCommand()
                    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                    #eel.getSenderMessages(choice)
                    if "no" in order.lower():                        
                        speak("Ok sir stopped sending messages....")
                        speak("Closing whatsapp sir ....")
                        gui.press('Ctrl')
                        gui.press('w') # press ctrl+w to close whatsapp
                        
                        break
            elif "no" in order.lower() or "different" in order.lower():                
                speak("Please tell me to whom you want to send the message :")
                name = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                #eel.getSenderMessages(choice)
                gui.click(253, 153)  # Clicking on the search bar
                gui.write(name.lower(), interval=0.05)  
                gui.click(317, 222)  # Clicking on the chat to open it                
                speak("Please speak out the message to be sent :")
                order = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                #eel.getSenderMessages(choice)
                gui.click(799, 991)  # Click the message input box
                time.sleep(0.5)  # Ensure focus is on the message input box
                gui.write(order.lower(), interval=0.05)  # Typing the message
                gui.press("Enter")  # Hit the enter key to send the message                
                speak("Message sent sir...")                
                speak("Do you wish to send another message sir ??")
                order = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                #eel.getSenderMessages(choice)
                while "yes" in order.lower():                    
                    speak("Please tell me to whom you want to send the message sir :")
                    name = takeCommand()
                    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                    #eel.getSenderMessages(choice)
                    gui.click(253, 153)  # Clicking on the search bar
                    gui.write(name.lower(), interval=0.5)  
                    gui.click(317, 222)  # Clicking on the chat to open it
                    
                    speak("Please speak out the message to be sent :")
                    order = takeCommand()
                    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                    #eel.getSenderMessages(choice)
                    gui.click(799, 991)  # Click the message input box
                    time.sleep(0.5)  # Ensure focus is on the message input box
                    gui.write(order.lower(), interval=0.05)  # Typing the message
                    gui.press('Enter')  # Hit the enter key to send the message                    
                    speak("Message sent sir...")                    
                    speak("Do you wish to send another messsage sir ??")
                    order = takeCommand()
                    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                    #eel.getSenderMessages(choice)
                    if "no" in order.lower():                        
                        speak("Ok sir stopped sending messages....")                        
                        speak("Closing whatsapp sir...")
                        gui.click(1887, 11) #closing whatsapp
                        break                
            speak("Do you wish to send another message sir ??")
            order = takeCommand()
            eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
            
            ##eel.getSenderMessages(choice)
            if "no" in order.lower():                
                speak("Ok sir stopped sending messages....")                
                speak("Closing whatsapp sir...") 
                


# function to set alarm

def alarmClock(string):
    if "set an alarm for" in string.lower():
        time = string.lower().split('for')[1]
    elif "wake me up at" in string.lower():
        time = string.lower().split('at')[1]
    
    time = time.upper().strip()
    time_parts = time.split(":")
    hours = int(time_parts[0])
    min = int(time_parts[1].split()[0])  # removes AM/PM
    print(f"Ok sir. Alarm set for {time}")
    if hours == 12 and ("A.M." in time or "a.m." in time):
        hours = 0
    elif ("P.M." in time or "p.m." in time.lower()) and hours < 12:
        hours += 12

    print(f"Hours = {hours}")
    print(f"Minutes = {min}")
    print(f"Alarm set for {hours}:{min}")

    py.mixer.init()
    while True:
        now = datetime.now()
        if now.hour == hours and now.minute == min:
            py.mixer.music.load(r"BACK_END\Assets\sound1.mp3")
            py.mixer.music.play(-1) # this is used to play the sound infinitely until explicitly stopped
            print("Alarm Ringing !!!")

            kb.read_event()  # Wait for any key press
            py.mixer.music.stop()
            print("Alarm stopped !!")
            break


# function to get the weather data using the weather API

def getWeather(string): 
    city = string.split("in")[1] # get the city from the string   
    api_key = api_keys.weather_api
    base_url = "https://api.openweathermap.org/data/2.5/weather?q="
    complete_url = base_url + city + "&appid=" + api_key
    response = requests.get(complete_url)
    weather_data = response.json()
    
    # print("RAW WEATHER DATA:", json.dumps(weather_data, indent=4))
    # printing the raw data for reference purpose
    
    # covnert the raw JSON data to a proper dictionary format to get the data systematically and also convert the temperatures to degree celcius from kelvin 
    weather_report = {
        "LATITUDE": round(weather_data["coord"]["lat"]),
        "LONGITUDE": round(weather_data["coord"]["lon"]),
        "WEATHER DESCRIPTION": weather_data["weather"][0]["description"],  # Fixed typo and corrected the key
        "CURRENT TEMPERATURE": round(weather_data["main"]["temp"] - 273.15, 3),
        "FEELS LIKE TEMPERATURE": round(weather_data["main"]["feels_like"] - 273.15, 3),
        "MAXIMUM TEMPERATURE": round(weather_data["main"]["temp_max"] - 273.15, 3),
        "MINIMUM TEMPERATURE": round(weather_data["main"]["temp_min"] - 273.15, 3),
        "PRESSURE": round(weather_data["main"]["pressure"]),
        "HUMIDITY": round(weather_data["main"]["humidity"]),
        "VISIBILITY": round(weather_data["visibility"]),
        "WIND SPEED": round(weather_data["wind"]["speed"]),
        "WIND DEGREE": round(weather_data["wind"]["deg"]),
        "SUNRISE": datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime('%I:%M:%S %p'),
        "SUNSET": datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime('%I:%M:%S %p')
    }
    speak(f"Ok sir, here's the weather report for {city}")
    speak(weather_report)


def generatePassword(length):
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation
    s = []
    s.extend(s1)
    s.extend(s2)
    s.extend(s3)
    s.extend(s4)
    random.shuffle(s)
    password = []
    password = "".join(s[0:length])
    return password

def handlePasswordGeneration(length):
    password = generatePassword(length)
    pyperclip.copy(password)
    print(password)
    speak("The generated password is copied successfully onto your clip board")
    speak('Do you accept this password sir ??')
    order = takeCommand()
    eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
    while True:
        if("yes" in order.lower()):
            speak("Thank you sir for using my password generation services...")
            return
        elif("no" in order.lower() or "different" in order.lower() or "change it" in order.lower()):
            speak("The two possible actions are : \n1) Shuffle the existing password\n2) Generate a new password")
            speak("Please tell me your choice sir")
            choice = check_for_integer_in_command(takeCommand()) # take the command and extract the option number from it
            eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
            if(choice == 1):
                random.shuffle(password)
                print(password)
                pyperclip.copy(password)
                speak("The shuffled password has been copied to your cliipboard sir")
                speak("Do you accept this password sir ??")
                order = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
            elif(choice == 2):
                password = generatePassword(length)
                print(password)
                pyperclip.copy(password)
                speak("The new password has been copied to your clipboard sir....")
                speak("Do you accept this password sir ??")
                order = takeCommand()
                eel.sendersMessage(string) # display whatever we speak to JARVIS in the chat history
                
# function to integrate gemini API 

def setup_model(api_key):
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    return model

def chat_with_ai(model, query):
    chat_session = model.start_chat()
    response = chat_session.send_message(query)
    print(response.text)
    speak(response.text)
    
    
#************************************************************ Android automation starts here #************************************************************

def phoneCall(string):
    if(string.lower().startswith("call")):
        string = string.lower().replace("call ", "")
        print(f'String after removing waste words : {string}')
        if(" " in string):
            name = string.replace(" ", "") # remove the space in case of multi-word names
        else:
            name = string           
    elif("make a call" in string.lower()):
        string = string.split("to")[1].strip().lower() # get the name by spplitting the string
        if(" " in string):
            name = string.replace(" ", "")
        else:
            name = string
    # database connections
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['JARVIS']
    collection = db['JARVISCollection']
    
    # Search for the contact
    speak(f"Calling {name} sir...")
    contact = collection.find_one({"name":name}) # find the contact with the correct name
    print(f"Contact name : {contact['name']}")
    print(f"Phone number of contact : {contact['number']}")
    command = f"adb shell am start -a android.intent.action.CALL -d tel:+91{contact['number']}"  
    os.system(command)
    
def unlockPhone():
    speak("OK sir....")
    command = "adb shell input keyevent KEYCODE_POWER"
    os.system(command)
    time.sleep(0.5)
    print("Screen turned on ....")
    command = "adb shell input swipe 313 1952 100 785"
    os.system(command)
    print("Swiped up....")

    PINCoordinates = {
        '0': (540, 1660),
        '1': (270, 970),
        '2': (520, 983),
        '3': (800, 965),
        '4': (275, 1229),
        '5': (530, 1229),
        '6': (808, 1196),
        '7': (300, 1436),
        '8': (550, 1436),
        '9': (803, 1436)
    }

    pin = "26042005"  

    for number in pin:
        print(f"Typing {number}.....")
        x, y = PINCoordinates[number]
        command = f"adb shell input tap {x} {y}"
        os.system(command)
        time.sleep(0.01) # wait for some time before typing the next number        
    print("PIN entered....")
    speak("Phone unlocked sir....")
    
def notifications():
    output = subprocess.getoutput("adb shell dumpsys window | findstr mDreamingLockscreen")
    if "mDreamingLockscreen=true" in output:
        speak("Your phone is locked sir , unlocking it first....")
        command = "adb shell input keyevent KEYCODE_POWER"
        os.system(command)
        time.sleep(0.5)
        print("Screen turned on ....")
        command = "adb shell input swipe 313 1952 100 785"
        os.system(command)
        print("Swiped up....")
        PINCoordinates = {
        '0': (540, 1660),
        '1': (270, 970),
        '2': (520, 983),
        '3': (800, 965),
        '4': (275, 1229),
        '5': (530, 1229),
        '6': (808, 1196),
        '7': (300, 1436),
        '8': (550, 1436),
        '9': (803, 1436)
        }
        pin = "26042005"
        for number in pin:
            print(f"Typing {number}.....")
            x, y = PINCoordinates[number]
            command = f"adb shell input tap {x} {y}"
            os.system(command)
            time.sleep(0.01) # wait for some time before typing the next number        
        print("PIN entered....")
        time.sleep(0.5)
        command = "adb shell input swipe 450 710 370 2032 10" # the last number represents the duration of the swipe in milliseconds, reduce the value to make the swipes faster
        os.system(command)
        speak("Opened Notifications sir....")
        
    else:
        command = "adb shell input swipe 500 0 500 1000 100"
        os.system(command)
        speak("Opened Notifications sir....")