import pyautogui
import time
from pynput import mouse

clics = []

def on_click(x, y, button, pressed):
    if pressed:
        clics.append((x, y))
        print(f"Clic en: X: {x}, Y: {y}")

        if len(clics) == 4:
            calcular_region()
            return False  

def calcular_region():
    left = min(clic[0] for clic in clics)
    top = min(clic[1] for clic in clics)
    right = max(clic[0] for clic in clics)
    bottom = max(clic[1] for clic in clics)

    width = right - left
    height = bottom - top

    print("\nRegión calculada:")
    print(f"  left: {left}, top: {top}, width: {width}, height: {height}")

if __name__ == "__main__":
    print("Haz clic en 4 puntos de la pantalla para definir la región.")
    print("Presiona Ctrl+C para detener el script.")
    
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
#Este script permite al usuario hacer clic en cuatro puntos de la pantalla para definir una región rectangular.
# Luego calcula y muestra las coordenadas de la región definida. Aveces puede fallar, pero es útil para obtener coordenadas de una imagen.
# Se recomienda usar el script @probar.py para detectar personajes, ya que es más confiable.