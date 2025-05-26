import pyautogui as gui
import time
while(True):
    x, y = gui.position()
    print(f"{x}, {y}")

