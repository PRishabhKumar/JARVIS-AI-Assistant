import os
import eel
import subprocess
import time
import threading
from BACK_END.features import playStartSound, detectHotword
from BACK_END.command import *
from BACK_END.Authentication import recognizer
from BACK_END.NLP.engine.intent_router import warmup_ollama

def start():
    # Pre-load Ollama model before anything else to ensure responsiveness
    warmup_ollama()

    # Play the startup sound only after model is ready
    playStartSound()    
    
    # Start hotword detection in a background thread
    hotword_thread = threading.Thread(target=detectHotword, daemon=True)
    hotword_thread.start()

    @eel.expose    
    def initialize(): 
        subprocess.call([r'device.bat']) # call this file to connect the phone to JARVIS using WIFI
        eel.hideLoader() # hide the loading animation
        speak("Ready for face authentication.....")  
        flag = recognizer.AuthenticateFace() # perform authentication
        if flag:
            eel.hideFaceAuth() # if the authentication is succesfull, then hide the authentication animation and play the sucess animation
            speak("Face authentication sucessful !!!")
            eel.hideFaceAuthSuccess() # after the authentication is succcssful, remove the success animation and greet the user
            speak("JARVIS assistant at your service sir......")
            eel.hideStart() # after the entire authentication process is done,, then hiden tha whole section and display the main blob of JARVIS
            playStartSound() # p[lay the sounf one more time when JARVIS appears       
        else:
            speak("Authentication failed......")                
    eel.init("FRONT_END")
    
        
    
    
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)  
    
if __name__ == "__main__":
    start()
