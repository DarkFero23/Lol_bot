import pyautogui
import cv2
import numpy as np
import time
import os

# Ruta de la imagen a detectar
image_path = r'./Personajes_pick/alistar.png'
#image_path = r'./picks_blancoynegro/sylas11.png'

# Umbral de coincidencia de template
confidence_levels = [0.9]

# Umbral de saturación (0–255): si la saturación media del ROI está por debajo,
# lo consideramos “baja saturación” (blanco y negro o muy desaturado)
saturation_threshold = 50

# Comprobamos que el archivo exista
if not os.path.isfile(image_path):
    print(f"Error: No se encontró la imagen en la ruta: {image_path}")
    exit(1)

target = cv2.imread(image_path)
h_t, w_t = target.shape[:2]

time.sleep(3)  # tiempo para cambiar a la ventana del juego

for conf in confidence_levels:
    print(f"Probando con confianza: {conf}")
    
    # Captura de pantalla y conversión a BGR
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Template matching
    result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f"Valor máximo encontrado: {max_val:.3f} en {max_loc}")
    
    # Todas las ubicaciones por encima del umbral
    loc = np.where(result >= conf)
    
    if loc[0].size == 0:
        print("No se encontraron coincidencias.")
    else:
        # Convertimos la captura a HSV para medir saturación
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        sat_channel = hsv[:, :, 1]
        
        for pt in zip(*loc[::-1]):
            x, y = pt
            # ROI de la región detectada
            roi_sat = sat_channel[y : y + h_t, x : x + w_t]
            mean_sat = cv2.mean(roi_sat)[0]
            print(f"  → Saturación media en ROI: {mean_sat:.1f}")
            
            if mean_sat < saturation_threshold:
                # Si está por debajo del umbral, marcamos en rojo y avisamos
                print("    ¡Imagen desaturada detectada! (blanco/negro o muy baja saturación)")
                cv2.rectangle(screenshot, pt, (x + w_t, y + h_t), (0, 0, 255), 2)
                cv2.putText(screenshot, "DESATURADO", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                # Si tiene suficiente saturación, marcamos en verde
                cv2.rectangle(screenshot, pt, (x + w_t, y + h_t), (0, 255, 0), 2)
        
        # Mostramos el resultado
        cv2.imshow('Detección + Saturación', screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # Mostramos el mapa de calor de coincidencias (opcional)
    cv2.imshow('Mapa de coincidencias', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

print("Detección completa.")
#Bendigo a GPT por darme este codigo tan clean , lo que hace es detectar y comparar la iamgene que esta en Personajes, igual se puede cambiar
#Pero toda esta logica se encargar de comparar esa imagen con la que esta en el juego, y si la imagen es blanca o negra, lo detecta y lo marca
# y si no lo es, lo marca de verde, y si no encuentra la imagen, lo marca de rojo , si no encuentra nada, imprime en consola el confidence obtenido y en base a eso
# se puede cambiar el confidence en la parte de arriba, y si no encuentra nada, lo marca de rojo.