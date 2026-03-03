import pyttsx3
import speech_recognition as sr
import pyaudio
import eel
import threading
import re
from word2number import w2n
import os
from dotenv import load_dotenv
from BACK_END import state

load_dotenv()

# --- NLP BRAIN INTEGRATION ---
try:
    from BACK_END.NLP.engine.intent_router import get_intent
except Exception as e:
    print(f"Intent Router Error: {e}")
    

mic_lock_event = threading.Event()
mic_lock_event.set()

@eel.expose
def speak(string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    eel.displayMessage(string)
    engine.say(string)
    eel.recieversMessage(string)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        eel.displayMessage("Listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 30, 10)
        try:
            string = r.recognize_google(audio, language="en-in")
            eel.displayMessage(string)
            return string
        except:
            return ""

# --- THE INTENT DISPATCHER ---

def dispatch_intent(intent, query, subject):
    from BACK_END import features
    # helper functions for missing parameters
    def ask_for_parameter(text):
        speak(text)
        response = takeCommand()
        eel.sendersMessage(response)
        return response if response else None
    
    # questions to ask for parameters for specific functions needing one
    if intent == "GET_WEATHER" and not subject:
        subject = ask_for_parameter("Which city should I check the weather for ??")
    elif intent == "PHONE_CALL" and not subject:
        subject = ask_for_parameter("Whom should I call sir ??")
    elif intent == "OPEN_APP_WEB" and not subject:
        subject = ask_for_parameter("Which app would you like me to open sir ??")
    
        
    # Helper for complex flows
    def handle_password():
        speak("Sure sir, tell me the length of the password you want:")
        try:
            length_str = takeCommand()
            eel.sendersMessage(length_str)
            features.handlePasswordGeneration(w2n.word_to_num(length_str))
        except:
            speak("Please say a valid number.")

    

    # Dispatch Mapping - Now using 'subject' instead of 'query' for content-heavy features
    mapping = {
        "OPEN_APP_WEB":        lambda: features.open(subject),
        "PLAY_YOUTUBE":        lambda: features.searchAndPlayOnYT(subject if subject else query),
        "PLAY_MUSIC":          lambda: features.playMusic(),
        "SEND_WHATSAPP":       lambda: features.handleWhatsapp(subject),
        "SET_ALARM":           lambda: features.alarmClock(subject),
        "GET_WEATHER":         lambda: features.getWeather(subject),
        "GENERATE_PASSWORD":   handle_password,
        "PHONE_CALL":          lambda: features.phoneCall(subject),
        "UNLOCK_PHONE":        lambda: features.unlockPhone(),
        "CHECK_NOTIFICATIONS": lambda: features.notifications(),
        "CLOSE_JARVIS":        lambda: features.closeJARVIS(),
    }

    if intent in mapping:
        mapping[intent]()
    else:
        # Fallback to Gemini AI
        from BACK_END.features import setup_model, chat_with_ai
        m = setup_model(os.getenv("geminiAPI"))
        chat_with_ai(m, query)

@eel.expose
def commands(message=1):
    try:
        state.IS_BUSY = True
        if message == 1:
            query = takeCommand()
            # Noise Filter: If query is empty or just a tiny noise, stop immediately.
            if not query or len(query.strip()) < 3:
                print(f"DEBUG [JARVIS]: Noise/Silence detected. Ignoring.")
                return
            
            eel.sendersMessage(query)
        else:
            query = message
            eel.sendersMessage(query)

        if not query: return

        result = get_intent(query) # ask ollama for which function to execute
        intent = result['intent']
        parameter = result['parameter']
        dispatch_intent(intent, query, parameter)        

    except Exception as e:
        print(f"Error in commands: {e}")
    finally:
        state.IS_BUSY = False
        eel.displayHood()