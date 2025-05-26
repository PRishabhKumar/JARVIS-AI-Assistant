import multiprocessing
import subprocess

# function to start JARVIS
def startJARVIS():
    print("Process 1 is running !!!")
    from main import start
    start() # call the function to start JARVIS
    
# function to start hotword detection
def startHotwordDetection():
    print("Process 2 is running !!!")
    from BACK_END.features import detectHotword
    detectHotword() # call the function to start the hotword detection
    
    
if __name__ == "__main__":
    process1 = multiprocessing.Process(target=startJARVIS) # the first subprocess if starting the UI of JARIVS
    process2 = multiprocessing.Process(target=startHotwordDetection) # the second subprocess is to start listening for the hotword
    process1.start()
    process2.start()
    process1.join()