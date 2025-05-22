import os
import time
import cv2
import numpy as np
import pyautogui
import sys

# ——— Parámetros ———
TH = 0.85
TH_AMARILLO = 0.95

TIMEOUT_SEC = 5
offset_x = 35
offset_y = 4
ROI_W = 61
ROI_H = 75

# ——— Paths ———
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LINEAS_DIR = resource_path('Lineas')
STRIPE_PATH = resource_path('Launcher/amarillo.png')

def obtener_confidence(template_path: str, image: np.ndarray):
    tpl = cv2.imread(template_path)
    if tpl is None:
        print(f"❌ No se pudo cargar plantilla: {template_path}")
        return 0.0
    th, tw = tpl.shape[:2]
    ih, iw = image.shape[:2]
    if ih < th or iw < tw:
        return 0.0
    res = cv2.matchTemplate(image, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    return max_val

def detectar_mi_linea(timeout=TIMEOUT_SEC):
    start = time.time()
    while True:
        if time.time() - start > timeout:
            print(f"⌛ Timeout tras {timeout}s. No se detectó línea.")
            return None

        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        cv2.imwrite("debug_screen.png", screen)

        coords = encontrar_coordenadas(STRIPE_PATH, screen, TH_AMARILLO)
        if not coords:
            time.sleep(0.2)
            continue

        x, y, w, h = coords
        print(f"✅ Franja amarilla detectada en ({x}, {y}) tamaño ({w}×{h}).")

        x0 = x + w + offset_x
        y0 = y + offset_y
        ih, iw = screen.shape[:2]
        x1 = min(iw, x0 + ROI_W)
        y1 = min(ih, y0 + ROI_H)
        print(f"🔍 ROI en ({x0}, {y0}) tamaño ({ROI_W}×{ROI_H}).")

        roi = screen[y0:y1, x0:x1]
        cv2.imwrite("debug_roi.png", roi)

        mejor_conf = 0
        mejor_linea = None

        for fn in sorted(os.listdir(LINEAS_DIR)):
            ruta_ln = os.path.join(LINEAS_DIR, fn)
            confidence = obtener_confidence(ruta_ln, roi)
            print(f"🔎 {fn}: confidence = {confidence:.4f}")

            if confidence >= TH and confidence > mejor_conf:
                mejor_conf = confidence
                mejor_linea = os.path.splitext(fn)[0].upper()

        if mejor_linea:
            print(f"🏷️ Línea detectada: {mejor_linea} (confidence: {mejor_conf:.4f})")
            return mejor_linea

        print("⚠️ Ninguna línea reconocida en la ROI. Reintentando…")
        time.sleep(0.2)

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

if __name__ == '__main__':
    linea = detectar_mi_linea()
    if linea:
        print(f"✅ Estás en: {linea}")
    else:
        print("❌ No se pudo determinar la línea.")
