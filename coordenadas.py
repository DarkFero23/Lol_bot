import pyautogui
import time

# Función para hacer clic en coordenadas específicas dentro de una imagen.
def click_en_coordenadas_imagen(ruta_imagen, coordenadas):
    """
    Busca una imagen en la pantalla y hace clic en las coordenadas específicas dentro de ella.
    
    :param ruta_imagen: Ruta del archivo de la imagen que se va a buscar.
    :param coordenadas: Coordenadas (x, y) dentro de la imagen donde hacer clic.
    """
    # Buscar la imagen en la pantalla
    time.sleep(2)

    imagen = pyautogui.locateOnScreen(ruta_imagen, confidence=0.7)
    if imagen is not None:
        # Obtener el centro de la imagen
        x, y = pyautogui.center(imagen)
        
        # Ajustar las coordenadas relativas al centro de la imagen
        x_relativo = x + coordenadas[0]
        y_relativo = y + coordenadas[1]
        
        # Hacer clic en las coordenadas específicas
        pyautogui.click(x_relativo, y_relativo)
        print(f"Clic en las coordenadas {x_relativo}, {y_relativo}.")
    else:
        print("Imagen no encontrada en la pantalla.")

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = 'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscador.png'
    coordenadas = (50, 30)  # Coordenadas relativas dentro de la imagen
    click_en_coordenadas_imagen(ruta_imagen, coordenadas)