import playsound as ps
import eel
import os
import sys
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
import requests
import string
import random
import pyperclip
import hugchat
import pymongo
import google.generativeai as genai
import subprocess
import time
import threading
from word2number import w2n
from dotenv import load_dotenv

load_dotenv()

from BACK_END import state

def detectHotword():
    while True:
        # If JARVIS is busy, don't even listen to audio to save resources and avoid feedback
        if state.IS_BUSY:
            time.sleep(1)
            continue

        porcupine = None
        paud = None
        audio_stream = None
        try:
            porcupine = pvporcupine.create(keywords=["jarvis", "alexa"]) 
            paud = pyaudio.PyAudio()
            audio_stream = paud.open(rate=porcupine.sample_rate, channels = 1, format = pyaudio.paInt16, input=True, frames_per_buffer = porcupine.frame_length)
            
            print("Listening for hotword...")
            while not state.IS_BUSY: # Stay in loop as long as JARVIS is not busy
                keyword = audio_stream.read(porcupine.frame_length)
                keyword = struct.unpack_from("h"*porcupine.frame_length, keyword)
                
                keyword_index = porcupine.process(keyword)
                
                if(keyword_index>=0):
                    print("Hotword detected !!")
                    gui.hotkey("win", "j") # use hotkey for cleaner combination simulation
                    # Small wait to let the command handler start
                    time.sleep(1) 
                    break # Exit inner loop to re-check state.IS_BUSY
        except Exception as e:
            print(f"Hotword Error: {e}")
            time.sleep(2) 
        finally:
            if audio_stream:
                audio_stream.close()
            if paud:
                paud.terminate()
            if porcupine:
                porcupine.delete()



# Play start sound
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
@eel.expose
def playStartSound():
    try:
        sound_directory = resource_path(r"FRONT_END\Assets\Audio\start_sound.mp3")
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

def open(appName):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['JARVIS']
    collection = db['JARVISCollection']

    try:
        # No more manual splitting! We use the appName directly from the NLP Brain.
        if not appName:
            speak("I didn't catch the name of the app sir.")
            return

        appInfo = collection.find_one({'name': appName.lower()}, {"_id":0, "path":1})
        if(not appInfo is None):
            speak(f"Opening {appName} sir")
            os.startfile(appInfo["path"])
        else:
            speak(f"I couldn't find {appName} in my database.")
            print("path not found !!")
    except Exception as e:
        speak("An error occurred while opening the app.")
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



def searchAndPlayOnYT(video_name):
    # If video_name is missing, we ask for it, otherwise we play directly
    if not video_name:
        speak("What video should I play on YouTube sir?")
        video_name = takeCommand()
        
    print(f"Playing {video_name} on youtube sir....")
    kit.playonyt(video_name)
    
    
def playOnYT(video_name):
    # If the user just said "open youtube", open the site. 
    # If they gave a video name, play it.
    if not video_name:
        os.startfile("https://www.youtube.com/")
        return

    os.startfile("https://www.youtube.com/") # open youtube
    time.sleep(5) # wait for the screen to stabilize
    gui.click(710, 132) # click on the search bar
    time.sleep(2) # wait for complete loading
    gui.write(video_name, interval=0.05) # type the query in the search bar
    time.sleep(2) # wait for some time
    gui.press('enter') # press enter to search 
    
    
# function to accpet a string and identify the numbers present in it for selection of song number 

def check_for_integer_in_command(string):
    for character in string:
        if character.isdigit():
            return int(character)
    return None
    
# function to play songs using a local music library
def playMusic():    
    speak("Ok sir, opening the music library for you...")
    for i in range(len(musicLibrary.music_library_list)):        
        print(f"{i + 1}) {musicLibrary.folder_names[i]} ")
        print()    
    speak("Please select the folder number that you want to open..")
    folder_num = takeCommand()
    eel.sendersMessage(folder_num)
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
                eel.sendersMessage(song_num)
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

def handleWhatsapp(contact_name):
    speak("Opening whatsapp sir....")
    gui.press("win") 
    time.sleep(2) 
    gui.write("whatsapp", interval=0.05) 
    time.sleep(1)
    gui.press('Enter') 
    
    # If NLP didn't find a name, we ask for it
    if not contact_name:
        speak("To whom should I send the message?")
        contact_name = takeCommand()

    # Search for the contact
    gui.click(253,  153) # click on the search bar
    time.sleep(1)
    gui.write(contact_name, interval=0.05) 
    time.sleep(2) 
    gui.click(317, 222)# click on the first chat
    
    speak("What is the message sir?")
    message = takeCommand()
    
    gui.click(799, 991) # click on the message input box
    time.sleep(1) 
    gui.write(message, interval=0.05) 
    time.sleep(0.5) 
    gui.press("Enter") 
    speak("Message sent sir.")
    speak("Do you wish to send another message sir ?")
    order = takeCommand()
    eel.sendersMessage(order)
    #eel.getSenderMessages(choice)
    while "yes" in order.lower():            
        speak("Do you want to send another message to the same person sir ??")
        order = takeCommand()
        eel.sendersMessage(order)
    if "yes" in order.lower():                
        speak("Please speak out the message to be sent :")
        message = takeCommand()
        eel.sendersMessage(message)
        #eel.getSenderMessages(choice)
        gui.click(317, 222)  # Clicking on the chat to open it                
        speak("Please speak out the message to be sent :")
        order = takeCommand()
        eel.sendersMessage(order)
        #eel.getSenderMessages(choice)
        gui.click(799, 991)  # Click the message input box
        time.sleep(0.5)  # Ensure focus is on the message input box
        gui.write(order.lower(), interval=0.05)  # Typing the message
        gui.press('Enter')  # Hit the enter key to send the message                
        speak("Message sent sir...")                
        speak("Do you wish to send another message sir ??")
        order = takeCommand()
        eel.sendersMessage(order)
        #eel.getSenderMessages(choice)
        while "yes" in order.lower():                    
            speak("Please speak out the message to be sent sir :")
            order = takeCommand()
            eel.sendersMessage(order)
            #eel.getSenderMessages(choice)
            gui.click(799, 991)  # Click the message input box
            time.sleep(0.5)  # Ensure focus is on the message input box
            gui.write(order.lower(), interval=0.05)  # Typing the message
            gui.press('enter') #pressing enter to send the message
            # gui.click(1884, 979)  # Clicking to send the message                    
            speak("Message sent sir...")                    
            speak("Do you wish to send another message sir ??")
            order = takeCommand()
            eel.sendersMessage(order)
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
        eel.sendersMessage(name)
        #eel.getSenderMessages(choice)
        gui.click(253, 153)  # Clicking on the search bar
        gui.write(name.lower(), interval=0.05)  
        gui.click(317, 222)  # Clicking on the chat to open it                
        speak("Please speak out the message to be sent :")
        order = takeCommand()
        eel.sendersMessage(order)
        #eel.getSenderMessages(choice)
        gui.click(799, 991)  # Click the message input box
        time.sleep(0.5)  # Ensure focus is on the message input box
        gui.write(order.lower(), interval=0.05)  # Typing the message
        gui.press("Enter")  # Hit the enter key to send the message                
        speak("Message sent sir...")                
        speak("Do you wish to send another message sir ??")
        order = takeCommand()
        eel.sendersMessage(order)
        #eel.getSenderMessages(choice)
        while "yes" in order.lower():                    
            speak("Please tell me to whom you want to send the message sir :")
            name = takeCommand()
            eel.sendersMessage(name)
            #eel.getSenderMessages(choice)
            gui.click(253, 153)  # Clicking on the search bar
            gui.write(name.lower(), interval=0.5)  
            gui.click(317, 222)  # Clicking on the chat to open it
            
            speak("Please speak out the message to be sent :")
            order = takeCommand()
            eel.sendersMessage(order)
            #eel.getSenderMessages(choice)
            gui.click(799, 991)  # Click the message input box
            time.sleep(0.5)  # Ensure focus is on the message input box
            gui.write(order.lower(), interval=0.05)  # Typing the message
            gui.press('Enter')  # Hit the enter key to send the message                    
            speak("Message sent sir...")                    
            speak("Do you wish to send another messsage sir ??")
            order = takeCommand()
            eel.sendersMessage(order)
            #eel.getSenderMessages(choice)
            if "no" in order.lower():                        
                speak("Ok sir stopped sending messages....")                        
                speak("Closing whatsapp sir...")
                gui.click(1887, 11) #closing whatsapp
                break                
            speak("Do you wish to send another message sir ??")
            order = takeCommand()
            eel.sendersMessage(order)
            
            ##eel.getSenderMessages(choice)
            if "no" in order.lower():                
                speak("Ok sir stopped sending messages....")                
                speak("Closing whatsapp sir...") 
                


def _alarm_loop(hours, minutes):
    """Helper function to run the alarm loop in a background thread."""
    py.mixer.init()
    print(f"DEBUG [Alarm Thread]: Waiting for {hours:02d}:{minutes:02d}...")
    while True:
        now = datetime.now()
        if now.hour == hours and now.minute == minutes:
            try:
                py.mixer.music.load(r"BACK_END\Assets\sound1.mp3")
                py.mixer.music.play(-1) 
                print("\n[ALARM] Ringing !!!")
                # Wait for any key press to stop the alarm
                kb.read_event() 
                py.mixer.music.stop()
                print("[ALARM] Stopped.")
            except Exception as e:
                print(f"Alarm Playback Error: {e}")
            break
        time.sleep(10) # check every 10 seconds to save CPU

def alarmClock(time_str):
    if not time_str:
        speak("For what time should I set the alarm?")
        time_str = takeCommand()
    
    try:
        # Standardize string for parsing
        original_time = time_str
        time_str = time_str.upper().strip().replace(".", "")
        
        # Extract numbers (handles "10:30", "11 20", etc.)
        numbers = re.findall(r'\d+', time_str)
        if not numbers:
            raise ValueError("No numbers found")
            
        hours = int(numbers[0])
        minutes = int(numbers[1]) if len(numbers) > 1 else 0
        
        # Logic to handle PM/AM conversion
        is_pm = "PM" in time_str or "P M" in time_str
        is_am = "AM" in time_str or "A M" in time_str
        
        if is_pm and hours < 12:
            hours += 12
        elif is_am and hours == 12:
            hours = 0
            
        speak(f"Ok sir, alarm set for {hours:02d}:{minutes:02d}")
        print(f"Alarm confirmed for {hours:02d}:{minutes:02d}")

        # Start the alarm in a background thread so JARVIS doesn't hang
        alarm_thread = threading.Thread(target=_alarm_loop, args=(hours, minutes), daemon=True)
        alarm_thread.start()

    except Exception as e:
        speak("There was an error in the time format. Please say it like '10 30 PM'.")
        print(f"Alarm Error: {e}")


# function to get the weather data using the weather API

def getWeather(city): 
    if not city:
        speak("Which city should I check the weather for?")
        city = takeCommand()
        
    api_key = os.getenv("weatherAPI")
    base_url = "https://api.openweathermap.org/data/2.5/weather?q="
    complete_url = base_url + city + "&appid=" + api_key
    response = requests.get(complete_url)
    
    if response.status_code != 200:
        speak(f"I couldn't get the weather for {city}. Please check the city name.")
        return

    weather_data = response.json()
    
    weather_report = {
        "LATITUDE": round(weather_data["coord"]["lat"]),
        "LONGITUDE": round(weather_data["coord"]["lon"]),
        "WEATHER DESCRIPTION": weather_data["weather"][0]["description"],  
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
    speak(f"The weather is currently {weather_report['WEATHER DESCRIPTION']} with a temperature of {weather_report['CURRENT TEMPERATURE']} degrees.")


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
    eel.sendersMessage(order)
    while True:
        if("yes" in order.lower()):
            speak("Thank you sir for using my password generation services...")
            return
        elif("no" in order.lower() or "different" in order.lower() or "change it" in order.lower()):
            speak("The two possible actions are : \n1) Shuffle the existing password\n2) Generate a new password")
            speak("Please tell me your choice sir")
            cmd_input = takeCommand()
            choice = check_for_integer_in_command(cmd_input)
            eel.sendersMessage(cmd_input)
            if(choice == 1):
                random.shuffle(password)
                print(password)
                pyperclip.copy(password)
                speak("The shuffled password has been copied to your cliipboard sir")
                speak("Do you accept this password sir ??")
                order = takeCommand()
                eel.sendersMessage(order)
            elif(choice == 2):
                password = generatePassword(length)
                print(password)
                pyperclip.copy(password)
                speak("The new password has been copied to your clipboard sir....")
                speak("Do you accept this password sir ??")
                order = takeCommand()
                eel.sendersMessage(order)
                
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
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
    )
    return model

def chat_with_ai(model, query):
    chat_session = model.start_chat()
    response = chat_session.send_message(query)
    print(response.text)
    speak(response.text)
    
    
#************************************************************ Android automation starts here #************************************************************

def phoneCall(name):
    if not name:
        speak("Whom should I call sir?")
        name = takeCommand()
        
    name = name.lower().replace(" ", "") # remove spaces for DB search
    
    # database connections
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['JARVIS']
    collection = db['JARVISCollection']
    
    # Search for the contact
    contact = collection.find_one({"name": name})
    if contact:
        speak(f"Calling {name} sir...")
        print(f"Contact name : {contact['name']}")
        print(f"Phone number of contact : {contact['number']}")
        command = f"adb shell am start -a android.intent.action.CALL -d tel:+91{contact['number']}"  
        os.system(command)
    else:
        speak(f"I couldn't find {name} in your contacts.")
    
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
        
        
# Closing JARVIS

def closeJARVIS():
    speak("Ok sir closing the application..")
    speak("It was a pleasure serving you sir ...Bye sir")
    gui.keyDown("ctrl")
    gui.keyDown("w")
    time.sleep(0.1)
    gui.keyUp("w")
    gui.keyUp("ctrl")