import pyautogui
import time

def click_en_coordenadas_imagen(ruta_imagen, coordenadas=(0, 0), confianza=0.8):
    """
    Busca una imagen en la pantalla y hace clic en coordenadas relativas al centro.
    Reintenta continuamente hasta encontrarla.
    
    :param ruta_imagen: Ruta del archivo de la imagen que se va a buscar.
    :param coordenadas: Coordenadas (x, y) relativas al centro de la imagen donde hacer clic.
    :param confianza: Nivel de confianza para la detección de imagen (0.0 a 1.0).
    """
    print(f"🔍 Buscando imagen: {ruta_imagen}")
    while True:
        imagen = pyautogui.locateOnScreen(ruta_imagen, confidence=confianza)
        if imagen is not None:
            centro_x, centro_y = pyautogui.center(imagen)
            click_x = centro_x + coordenadas[0]
            click_y = centro_y + coordenadas[1]
            pyautogui.moveTo(click_x, click_y)
            print(f"✅ Imagen encontrada. Clic en ({click_x}, {click_y}) relativo al centro.")
            break
        else:
            print("❌ Imagen no encontrada. Reintentando en 0.5s...")
            time.sleep(0.5)

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r'./Personajes_pick/shaco.png'
    click_en_coordenadas_imagen(ruta_imagen)  # Clic exactamente en el centro
