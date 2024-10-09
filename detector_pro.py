import pyautogui
import time

ruta_imagen = './Launcher/aceptar_s.png' 

def buscar_y_mostrar_coordenadas():
    print("Presiona Ctrl+C para detener el script.")
    try:
        while True:
            pos = pyautogui.locateOnScreen(ruta_imagen, confidence=0.8)  
            
            if pos is not None:
                left, top, width, height = pos
                print(f"Imagen encontrada:")
                print(f"  left: {left}")
                print(f"  top: {top}")
                print(f"  width: {width}")
                print(f"  height: {height}")
            else:
                print("Imagen no encontrada.")

            time.sleep(1)  
    except KeyboardInterrupt:
        print("\nDeteniendo el script...")

if __name__ == "__main__":
    buscar_y_mostrar_coordenadas()
