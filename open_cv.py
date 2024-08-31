import cv2
import numpy as np
import pyautogui

def encontrar_imagen_en_pantalla(template_path, threshold=0.7):
    # Captura de pantalla
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convertir a BGR si es necesario
    
    # Leer la imagen de referencia y convertir a escala de grises
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    
    # Convertir la captura de pantalla a escala de grises
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Coincidencia de plantilla
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    if len(loc[0]) > 0:
        for pt in zip(*loc[::-1]):
            # Dibujar un rectángulo alrededor de la coincidencia (opcional)
            cv2.rectangle(screenshot_gray, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
            # Retornar la posición del centro de la coincidencia
            return pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2
    return None

# Ejemplo de uso
position = encontrar_imagen_en_pantalla('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/aceptar_redimensionadas.png', threshold=0.3)
if position:
    pyautogui.click(position)
    print("Imagen encontrada y clic realizada.")
else:
    print("No se encontró la imagen.")
