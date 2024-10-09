import pyautogui
import cv2
import numpy as np
import time
import os

image_path = r'./Personajes_pick/pantalones2.png'  # Usa la ruta completa

if not os.path.isfile(image_path):
    print(f"Error: No se encontró la imagen en la ruta: {image_path}")
else:
    target_image = cv2.imread(image_path)

    confidence_levels = [0.9]  

    time.sleep(3)

    height, width, _ = target_image.shape

    for confidence in confidence_levels:
        print(f"Probando con confianza: {confidence}")

        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(f"Valor máximo encontrado: {max_val} en la ubicación {max_loc}")

        loc = np.where(result >= confidence)

        if loc[0].size > 0:  
            for pt in zip(*loc[::-1]):  
                cv2.rectangle(screenshot, pt, (pt[0] + width, pt[1] + height), (0, 255, 0), 2)

            cv2.imshow('Detección de imagen', screenshot)
            cv2.waitKey(0)  
        else:
            print("No se encontraron coincidencias.")

        cv2.imshow('Resultado de coincidencia', result)
        cv2.waitKey(0)  
        cv2.destroyAllWindows()

    print("Detección completa.")
