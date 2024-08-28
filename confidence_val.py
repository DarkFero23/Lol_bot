import pyautogui
import time

ruta_imagen = 'D:/Chente/Lolblot/Lol_bot/Launcher/aceptar_redimensionada.png'

for conf in [0.3,0.4, 0.5, 0.6, 0.7, 0.8]:
    try:
        # Intentar localizar la imagen en la pantalla con el nivel de confianza actual
        ubicacion = pyautogui.locateOnScreen(ruta_imagen, confidence=conf)
        
        if ubicacion is not None:
            print(f"Se ve con confianza = {conf}")
        else:
            print(f"No se ve con confianza = {conf}")
    except pyautogui.ImageNotFoundException:
        print(f"Error: Imagen no encontrada con confianza = {conf}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    
    time.sleep(0.5)
