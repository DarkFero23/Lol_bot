import pyautogui
import time

def mostrar_imagen_detectada():
    print("Buscando imagen en la pantalla...")
    imagen = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscar.png', confidence=0.6)
    if imagen:
        print(f"Imagen detectada en: {imagen}")
    else:
        print("Imagen no encontrada.")

mostrar_imagen_detectada()