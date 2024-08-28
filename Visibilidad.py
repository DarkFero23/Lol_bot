import pyautogui
import time

def mostrar_imagen_detectada():
    print("Buscando imagen en la pantalla...")
    imagen = pyautogui.locateOnScreen('D:/Chente/Lolblot/Lol_bot/Launcher/aceptar_redimensionada.png', confidence=0.2)
    if imagen:
        print(f"Imagen detectada en: {imagen}")
    else:
        print("Imagen no encontrada.")

mostrar_imagen_detectada()