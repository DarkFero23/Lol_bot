import cv2
import numpy as np

# 🔧 RUTAS DE LAS IMÁGENES A COMPARAR
IMG1_PATH = r'./Lineas/Mid.png'
IMG2_PATH = r'./debug_roi.png'

def comparar_imagenes(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None:
        print(f"❌ No se pudo cargar: {img1_path}")
        return
    if img2 is None:
        print(f"❌ No se pudo cargar: {img2_path}")
        return

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    if h2 > h1 or w2 > w1:
        img2 = cv2.resize(img2, (w1, h1))

    res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # 🔥 Mostramos la confianza directo y sin floro
    print(f"\n📌 CONFIDENCE: {max_val:.4f}\n")

if __name__ == "__main__":
    comparar_imagenes(IMG1_PATH, IMG2_PATH)

