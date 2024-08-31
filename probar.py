import pyautogui 
import time 

while True:
    try:
        if pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscador.png', confidence=0.7) is not None:
            print("Se ve")
        else:
            print("No se ve")
    except pyautogui.ImageNotFoundException:
        print("Error: Imagen no encontrada")
    except Exception as e:
        print(f"Error inesperado: {e}")
    
    time.sleep(0.5)

        
#grupo= 0.4
#aceptar = 0.35
#Comenzar = 0.48    