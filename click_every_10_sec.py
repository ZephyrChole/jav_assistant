import time
from winsound import Beep
import pyautogui


while True:
    time.sleep(10)
    Beep(1000,1000)
    pyautogui.click(button='left')
