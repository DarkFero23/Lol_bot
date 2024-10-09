import pyautogui
import time
import os
import cv2
import numpy as np
# Función que espera hasta que el botón 'Aceptar' aparezca en la pantalla y hace clic en él.
def esperar_y_aceptar_partida(ruta_boton_aceptar, confianza=0.85, tiempo_espera=500):
    tiempo_inicial = time.time()
    while time.time() - tiempo_inicial < tiempo_espera:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        boton_aceptar = cv2.imread(ruta_boton_aceptar)
        result = cv2.matchTemplate(screenshot, boton_aceptar, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= confianza)

        if loc[0].size > 0:
            print("Se encontró el botón 'Aceptar'.")
            for pt in zip(*loc[::-1]):  # Cambiar columnas y filas
                cv2.rectangle(screenshot, pt, (pt[0] + boton_aceptar.shape[1], pt[1] + boton_aceptar.shape[0]), (0, 255, 0), 2)
                click = pyautogui.center((pt[0], pt[1], boton_aceptar.shape[1], boton_aceptar.shape[0]))
                pyautogui.click(click)
                print("Botón 'Aceptar' clickeado. Esperando a entrar a la partida...")
                return True
        time.sleep(1)
    
    print("Error: No se encontró el botón 'Aceptar' dentro del tiempo especificado.")
    return False
def esperar_imagen(ruta_imagen_media, timeout=30):
    """
    Espera hasta que una imagen específica aparezca en la pantalla dentro de un tiempo determinado.
    
    :param ruta_imagen_media: Ruta de la imagen que se espera.
    :param timeout: Tiempo máximo de espera en segundos (por defecto 30 segundos).
    :return: True si la imagen apareció, False si no apareció en el tiempo establecido.
    """
    print(f"Esperando la aparición de la imagen: {ruta_imagen_media}")
    tiempo_inicial = time.time()

    while time.time() - tiempo_inicial < timeout:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        imagen_referencia = cv2.imread(ruta_imagen_media)
        result = cv2.matchTemplate(screenshot, imagen_referencia, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.85)

        if loc[0].size > 0:
            print(f"Imagen encontrada: {ruta_imagen_media}")
            return True

        time.sleep(1) 

    print(f"Error: No se encontró la imagen {ruta_imagen_media} en {timeout} segundos.")
    return False
# Función para limpiar el texto en el buscador.
def limpiar_buscador(ruta_buscador):
    """Hace clic en el buscador y luego limpia el texto que está dentro."""
    while True:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        buscador_pick = cv2.imread(ruta_buscador)
        result = cv2.matchTemplate(screenshot, buscador_pick, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.85)

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):  
                click = pyautogui.center((pt[0], pt[1], buscador_pick.shape[1], buscador_pick.shape[0]))
                pyautogui.click(click)
                pyautogui.hotkey('ctrl', 'a')  
                pyautogui.press('backspace')   
                return

def pre_pick_campeon(campeon, ruta_buscador, ruta_campeon):
    print(f"Buscando el campeón: {campeon}")

    while True:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        buscador_pick = cv2.imread(ruta_buscador)
        result = cv2.matchTemplate(screenshot, buscador_pick, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.85)

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):  
                click = pyautogui.center((pt[0], pt[1], buscador_pick.shape[1], buscador_pick.shape[0]))
                pyautogui.click(click)
                pyautogui.write(campeon, interval=0.15)
                time.sleep(1)  
                campeon_imagen = cv2.imread(ruta_campeon)
                tiempo_inicial = time.time()
                while time.time() - tiempo_inicial < 60:  
                    screenshot = pyautogui.screenshot()
                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    result = cv2.matchTemplate(screenshot, campeon_imagen, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(result >= 0.85)
                    if loc[0].size > 0:
                        for pt in zip(*loc[::-1]):  
                            click = pyautogui.center((pt[0], pt[1], campeon_imagen.shape[1], campeon_imagen.shape[0]))
                            pyautogui.click(click)
                            print(f"{campeon} seleccionado. Siguiendo con lo demas")
                            limpiar_buscador(ruta_buscador)  

                            return True

                print(f"Error: No se encontró la imagen del campeón {campeon} en la pantalla.")
                return False

def seleccionar_campeon_ban(campeon, ruta_buscador, ruta_campeon, ruta_boton):
    print(f"Buscando el campeón: {campeon}")

    while True:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        buscador_pick = cv2.imread(ruta_buscador)
        result = cv2.matchTemplate(screenshot, buscador_pick, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.85)

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):  
                click = pyautogui.center((pt[0], pt[1], buscador_pick.shape[1], buscador_pick.shape[0]))
                pyautogui.click(click)
                pyautogui.write(campeon, interval=0.15)
                time.sleep(1)  
                campeon_imagen = cv2.imread(ruta_campeon)
                tiempo_inicial = time.time()
                while time.time() - tiempo_inicial < 60:  
                    screenshot = pyautogui.screenshot()
                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    result = cv2.matchTemplate(screenshot, campeon_imagen, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(result >= 0.85)

                    if loc[0].size > 0:
                        for pt in zip(*loc[::-1]):  
                            click = pyautogui.center((pt[0], pt[1], campeon_imagen.shape[1], campeon_imagen.shape[0]))
                            pyautogui.click(click)
                            print(f"{campeon} seleccionado.")
                            if hacer_click_boton(ruta_boton):
                                print("Clic en el botón exitoso.")
                            else:
                                print("Error: No se pudo hacer clic en el botón.")
                            limpiar_buscador(ruta_buscador)  

                            return True

                print(f"Error: No se encontró la imagen del campeón {campeon} en la pantalla.")
                return False
            
def seleccionar_campeon_pick(campeon, ruta_buscador, ruta_campeon, ruta_boton):
    print(f"Buscando el campeón: {campeon}")

    while True:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        buscador_pick = cv2.imread(ruta_buscador)
        result = cv2.matchTemplate(screenshot, buscador_pick, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.85)

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):  
                click = pyautogui.center((pt[0], pt[1], buscador_pick.shape[1], buscador_pick.shape[0]))
                pyautogui.click(click)
                pyautogui.write(campeon, interval=0.15)
                time.sleep(1)  
                campeon_imagen = cv2.imread(ruta_campeon)
                tiempo_inicial = time.time()
                while time.time() - tiempo_inicial < 60:  
                    screenshot = pyautogui.screenshot()
                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    result = cv2.matchTemplate(screenshot, campeon_imagen, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(result >= 0.85)

                    if loc[0].size > 0:
                        for pt in zip(*loc[::-1]):  
                            click = pyautogui.center((pt[0], pt[1], campeon_imagen.shape[1], campeon_imagen.shape[0]))
                            pyautogui.click(click)
                            print(f"{campeon} seleccionado.")
                            if hacer_click_boton(ruta_boton):
                                print("Clic en el botón exitoso.")
                            else:
                                print("Error: No se pudo hacer clic en el botón.")
                            limpiar_buscador(ruta_buscador)  

                            return True

                print(f"Error: No se encontró la imagen del campeón {campeon} en la pantalla.")
                return False
            

def hacer_click_boton(ruta_boton):
    """
    Función para buscar y hacer clic en un botón basado en la ruta de la imagen.
    
    :param ruta_boton: Ruta de la imagen del botón a hacer clic.
    :return: True si el clic fue exitoso, False en caso contrario.
    """
    print("Buscando botón para hacer clic...")
    
    while True:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        boton = cv2.imread(ruta_boton)
        result = cv2.matchTemplate(screenshot, boton, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.85)

        print(f"Buscando botón. Detecciones encontradas: {loc[0].size}")

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):
                click = pyautogui.center((pt[0], pt[1], boton.shape[1], boton.shape[0]))
                pyautogui.click(click)
                print("Botón clickeado.")
                return True

        # Puedes poner un delay aquí si lo deseas
        time.sleep(1)

    print("Error: No se encontró el botón.")
    return False

# Función principal que ejecuta todo el proceso de selección y baneo de campeones.
def ejecutar_seleccion(campeon_pick=None, campeon_ban=None):
    ruta_buscador = './Launcher/buscador1.0.png'
    ruta_fijar_boton = './Launcher/fijar.png'
    ruta_click_boton_bloqueo = './Launcher/bloqueo2.png'
    ruta_boton_aceptar = './Launcher/aceptar.png'
    ruta_campeon_pick = f'./Personajes_pick/{campeon_pick}.png'
    ruta_campeon_ban = f'./Personajes_pick/{campeon_ban}.png'
    ruta_imagen_media = './Launcher/BloqueoLetras.png'

    if campeon_pick and not os.path.exists(ruta_campeon_pick):
        print(f"Error: La imagen para el campeón {campeon_pick} no se encuentra en la ruta {ruta_campeon_pick}.")
        return False
    if campeon_ban and not os.path.exists(ruta_campeon_ban):
        print(f"Error: La imagen para el campeón {campeon_ban} no se encuentra en la ruta {ruta_campeon_ban}.")
        return False
    
    print("Iniciando proceso de selección de campeón...")

    #Esperar y aceptar la partida
    if not esperar_y_aceptar_partida(ruta_boton_aceptar):
        print("Proceso abortado: No se pudo aceptar la partida.")
        return

    #Este es el pre-pick antes del baneo , donde no aparece el boto nde FIJAR (todavia)
    if campeon_pick and not pre_pick_campeon(campeon_pick, ruta_buscador, ruta_campeon_pick):
        print("Proceso abortado durante la selección del campeón para pick.")
        return
    
    # Esperar hasta que aparezca la imagen clave que indica que puedes proceder al ban
    if not esperar_imagen(ruta_imagen_media, timeout=30):  
        print("Error: No se pudo detectar la pantalla de bloqueo (ban).")
        return
    
     # Bloquear campeón (ban)
    if campeon_ban and not seleccionar_campeon_ban(campeon_ban, ruta_buscador, ruta_campeon_ban, ruta_click_boton_bloqueo):
        print("Proceso abortado durante el bloqueo del campeón.")
        return
    
    # Seleccionar campeón para pick
    if campeon_pick and not seleccionar_campeon_pick(campeon_pick, ruta_buscador, ruta_campeon_pick,ruta_fijar_boton):
        print("Proceso abortado durante la selección del campeón para pick.")
        return

    print("El proceso de selección de campeones ha finalizado con éxito.")

