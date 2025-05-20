import pyautogui, time

print("Mueve el cursor hasta el punto que necesites medir y pulsa Ctrl-C para parar.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"Cursor en: ({x}, {y})")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Medición finalizada.")
