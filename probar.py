import pyautogui 
import time 

while 1:
    if pyautogui.locateOnScreen('Comenzar.png', confidence=0.48) != None:
        print("Se ve")
        time.sleep(0.5)
    else:
        print("Toy ciego")
        time.sleep(0.5)
        
#grupo= 0.4
#aceptar = 0.35
#Comenzar = 0.48    