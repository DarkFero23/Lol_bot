import pyautogui
import cv2
import numpy as np
import time
import os

# === Configuración ===
carpeta_imagenes = './Launcher'
salida_log = 'resultados_deteccion.txt'
confidence = 0.90
saturation_threshold = 50

# Esperar unos segundos para cambiar a la ventana del juego
print("🔄 Esperando 3 segundos para cambiar a la ventana del juego...")
time.sleep(3)

# Abrir archivo de salida
with open(salida_log, 'w', encoding='utf-8') as log_file:
    log_file.write("Campeón\tDetectado\tConfidence\tDesaturado\n")

    for nombre_archivo in os.listdir(carpeta_imagenes):
        if not nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue  # Ignorar archivos que no sean imagen

        ruta_imagen = os.path.join(carpeta_imagenes, nombre_archivo)
        target = cv2.imread(ruta_imagen)
        if target is None:
            print(f"❌ Error al leer {ruta_imagen}")
            continue

        h_t, w_t = target.shape[:2]
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        encontrado = max_val >= confidence
        desaturado = False

        if encontrado:
            x, y = max_loc
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            sat_channel = hsv[:, :, 1]
            roi_sat = sat_channel[y: y + h_t, x: x + w_t]
            mean_sat = cv2.mean(roi_sat)[0]
            desaturado = mean_sat < saturation_threshold
            print(f"✅ {nombre_archivo} | Conf: {max_val:.3f} | Sat: {mean_sat:.1f} | Desaturado: {desaturado}")
        else:
            print(f"❌ {nombre_archivo} NO DETECTADO | Conf: {max_val:.3f}")

        log_file.write(f"{nombre_archivo}\t{encontrado}\t{max_val:.3f}\t{desaturado}\n")

print("📄 Detección finalizada. Resultados guardados en 'resultados_deteccion.txt'")

#Bendigo a GPT por darme este codigo tan clean , lo que hace es detectar y comparar la iamgene que esta en Personajes, igual se puede cambiar
#Pero toda esta logica se encargar de comparar esa imagen con la que esta en el juego, y si la imagen es blanca o negra, lo detecta y lo marca
# y si no lo es, lo marca de verde, y si no encuentra la imagen, lo marca de rojo , si no encuentra nada, imprime en consola el confidence obtenido y en base a eso
# se puede cambiar el confidence en la parte de arriba, y si no encuentra nada, lo marca de rojo.