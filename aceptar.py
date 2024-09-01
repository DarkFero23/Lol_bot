import pyautogui
import time
import os

# Función que espera hasta que el botón 'Aceptar' aparezca en la pantalla y hace clic en él.
def esperar_y_aceptar_partida(ruta_boton_aceptar, confianza=0.7, tiempo_espera=500):
    locacion_boton_aceptar = None
    tiempo_inicial = time.time()
    while locacion_boton_aceptar is None and time.time() - tiempo_inicial < tiempo_espera:
        locacion_boton_aceptar = pyautogui.locateOnScreen(ruta_boton_aceptar, confidence=confianza)
        time.sleep(1)
    
    if locacion_boton_aceptar is not None:
        print("Se encontró el botón 'Aceptar'.")
        click = pyautogui.center(locacion_boton_aceptar)
        pyautogui.click(click)
        print("Botón 'Aceptar' clickeado. Esperando a entrar a la partida...")
        return True
    else:
        print("Error: No se encontró el botón 'Aceptar' dentro del tiempo especificado.")
        return False

# Función para limpiar el texto en el buscador.
def limpiar_buscador(ruta_buscador):
    """
    Hace clic en el buscador y luego limpia el texto que está dentro.
    """
    buscador_pick = None
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen(ruta_buscador, confidence=0.7)
        time.sleep(1)
    
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.hotkey('ctrl', 'a')  # Selecciona todo el texto
    pyautogui.press('backspace')   # Elimina el texto seleccionado
    
# Función que selecciona un campeón.

def seleccionar_campeon(campeon, ruta_buscador, ruta_campeon):
    print(f"Buscando el campeón: {campeon}")
    
    buscador_pick = None
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen(ruta_buscador, confidence=0.7)
        time.sleep(1)
    
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write(campeon, interval=0.15)
    time.sleep(1)  # Tiempo para que aparezca la imagen del campeón

    if os.path.exists(ruta_campeon):
        campeon_imagen = pyautogui.locateOnScreen(ruta_campeon, confidence=0.7)
        if campeon_imagen is not None:
            click = pyautogui.center(campeon_imagen)
            pyautogui.click(click)
            print(f"{campeon} seleccionado.")
            limpiar_buscador(ruta_buscador)  # Limpia el buscador después de seleccionar el campeón
            return True
        else:
            print(f"Error: No se encontró la imagen del campeón {campeon} en la pantalla.")
            return False
    else:
        print(f"Error: La imagen del campeón {campeon} no existe en la ruta especificada.")
        return False

# Función para bloquear un campeón (ban).
def bloquear_campeon(ruta_bloquear_boton):
    bloquear_button = None
    while bloquear_button is None:
        bloquear_button = pyautogui.locateOnScreen(ruta_bloquear_boton, confidence=0.7)
        time.sleep(1)
    
    click = pyautogui.center(bloquear_button)
    pyautogui.click(click)
    print("Campeón baneado.")
    return True

# Función para fijar la selección del campeón.
def fijar_seleccion(ruta_fijar_boton):
    fijar = None
    while fijar is None:
        fijar = pyautogui.locateOnScreen(ruta_fijar_boton, confidence=0.7)
        time.sleep(1)
    
    click = pyautogui.center(fijar)
    pyautogui.click(click)
    print("Campeón fijado.")
    return True

# Función principal que ejecuta todo el proceso de selección y baneo de campeones.
def ejecutar_seleccion(campeon_pick, campeon_ban):
    ruta_buscador = 'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscador.png'
    ruta_fijar_boton = 'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/fijar.png'
    ruta_bloquear_boton = 'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/bloqueo.png'
    ruta_boton_aceptar = 'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/aceptar_s.png'
    ruta_campeon_pick = f'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Personajes_pick/{campeon_pick}.png'
    ruta_campeon_ban = f'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Personajes_pick/{campeon_ban}.png'

    print("Iniciando proceso de selección de campeón...")
    '''
    # Esperar y aceptar la partida
    if not esperar_y_aceptar_partida(ruta_boton_aceptar):
        print("Proceso abortado: No se pudo aceptar la partida.")
        return
'''
    # Seleccionar campeón para pick
    if not seleccionar_campeon(campeon_pick, ruta_buscador, ruta_campeon_pick):
        print("Proceso abortado durante la selección del campeón para pick.")
        return
    time.sleep(15)
    # Seleccionar campeón para ban
    if not seleccionar_campeon(campeon_ban, ruta_buscador, ruta_campeon_ban):
        print("Proceso abortado durante la selección del campeón para ban.")
        return
    
    # Bloquear campeón baneado
    if not bloquear_campeon(ruta_bloquear_boton):
        print("Proceso abortado durante el bloqueo del campeón.")
        return
    
    # Volver a seleccionar el campeón inicial antes de fijarlo

    if not seleccionar_campeon(campeon_pick, ruta_buscador, ruta_campeon_pick):
        print("Proceso abortado durante la selección del campeón para pick.")
        return
    
    # Fijar selección del campeón pickeado
    if not fijar_seleccion(ruta_fijar_boton):
        print("Proceso abortado durante la fijación de la selección.")
        return
    
    print("Proceso de selección completado exitosamente.")

# Ejemplo de uso
if __name__ == "__main__":
    campeon_a_pickear = "sylas"
    campeon_a_banear = "leblanc"
    #campeon_a_pickear = input("Ingresa el nombre del campeón que deseas pickear: ").strip().lower()
    #campeon_a_banear = input("Ingresa el nombre del campeón que deseas banear: ").strip().lower()
    ejecutar_seleccion(campeon_a_pickear, campeon_a_banear)
