import os
import time
import cv2
import numpy as np
import pyautogui
import sys
import os
# Parámetros
TH = 0.85
TIMEOUT_SEC = 5  # segundos máximo para detectar línea

# Offset medido entre la franja amarilla y tu círculo de pick
offset_x = 35  # píxeles a la derecha de la franja
offset_y = 2   # píxeles abajo de la franja
ROI_W = 59     # ancho del área de interés
ROI_H = 75     # alto del área de interés


def resource_path(relative_path):
    try:
        # PyInstaller crea una carpeta temporal y almacena ahí los archivos
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# Rutas relativas
LINEAS_DIR = resource_path('Lineas')
STRIPE_PATH = resource_path('Launcher/amarillo.png')


def encontrar_coordenadas(template_path: str, image: np.ndarray, threshold: float):
    tpl = cv2.imread(template_path)
    if tpl is None:
        return None
    th, tw = tpl.shape[:2]
    ih, iw = image.shape[:2]
    if ih < th or iw < tw:
        return None
    res = cv2.matchTemplate(image, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return (max_loc[0], max_loc[1], tw, th)
    return None


def detectar_mi_linea(timeout=TIMEOUT_SEC):
    start = time.time()
    while True:
        # Timeout?
        if time.time() - start > timeout:
            print(f"⌛ Timeout tras {timeout}s. No se detectó línea.")
            return None

        # 1) Captura de pantalla
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # 2) Detectar franja amarilla
        coords = encontrar_coordenadas(STRIPE_PATH, screen, TH)
        if not coords:
            # sigue intentando
            time.sleep(0.2)
            continue

        x, y, w, h = coords
        print(f"✅ Franja amarilla detectada en ({x}, {y}) tamaño ({w}×{h}).")

        # 3) Definir ROI respecto a la franja
        x0 = x + w + offset_x
        y0 = y + offset_y
        ih, iw = screen.shape[:2]
        x1 = min(iw, x0 + ROI_W)
        y1 = min(ih, y0 + ROI_H)
        print(f"🔍 ROI en ({x0}, {y0}) tamaño ({ROI_W}×{ROI_H}).")

        roi = screen[y0:y1, x0:x1]

        # 4) Probar cada plantilla de línea
        for fn in sorted(os.listdir(LINEAS_DIR)):
            print(f"▶ Probando plantilla: {fn}")
            ruta_ln = os.path.join(LINEAS_DIR, fn)
            if encontrar_coordenadas(ruta_ln, roi, TH):
                linea = os.path.splitext(fn)[0].upper()
                print(f"🏷️ Línea detectada: {linea}")
                return linea

        print("⚠️ Ninguna línea reconocida en la ROI. Reintentando…")
        time.sleep(0.2)


if __name__ == '__main__':
    linea = detectar_mi_linea()
    if linea:
        print(f"✅ Estás en: {linea}")
    else:
        print("❌ No se pudo determinar la línea.")
