import pyautogui
import time

# Inicialización de variables
locacion_boton_aceptar = None
locacion_verificador = None
locacion_bucle = None
boton_comenzar = None
buscador_pick = None
buscador_ban = None
fijar = None
personaje_pick = None
personaje_ban = None

# Función que acepta el botón y pickea Sylas.
def aceptar_boton():
    print("Comenzando el Script, esperando que se encuentre el botón 'Aceptar'")
    global locacion_boton_aceptar

    # Esperar hasta que se encuentre el botón 'Aceptar'
    while locacion_boton_aceptar is None:
        locacion_boton_aceptar = pyautogui.locateOnScreen('D:/Chente/Lolblot/Lol_bot/Launcher/Aceptar.jpg', confidence=0.7)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Se encontró el botón 'Aceptando la partida'")
    click = pyautogui.center(locacion_boton_aceptar)
    pyautogui.click(click)
    
    print("Esperando a entrar a la partida...")
    
    # Buscar y seleccionar Sylas
    print("Buscando pick: Sylas")
    global buscador_pick
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('D:/Chente/Lolblot/Lol_bot/Launcher/buscador.png', confidence=0.9)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU

    print("Pickeando Sylas")
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    print("Sylas encontrado")

    # Banear Yasuo
    print("Buscando pick para banear: Yasuo")
    global buscador_ban
    while buscador_ban is None:
        buscador_ban = pyautogui.locateOnScreen('/Lol_bot/Launcher/buscador.png', confidence=0.9)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Baneando Yasuo")
    click = pyautogui.center(buscador_ban)
    pyautogui.click(click)
    pyautogui.write('yasuo', interval=0.15)
    print("Yasuo baneado")

    # Seleccionar nuevamente Sylas
    print("Buscando pick: Sylas")
    buscador_pick = None  # Resetear la variable para evitar conflictos
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('/Lol_bot/Launcher/buscador.png', confidence=0.9)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Pickeando Sylas nuevamente")
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    print("Sylas encontrado nuevamente")

    # Seleccionar Sylas para la partida
    print("Seleccionando Campeón para la partida")
    global personaje_pick
    while personaje_pick is None:
        personaje_pick = pyautogui.locateOnScreen('/Lol_bot/Personajes_pick/sylas.png', confidence=0.9)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Seleccionando Sylas")
    click = pyautogui.center(personaje_pick)
    pyautogui.click(click)

    # Fijar la selección del Campeón
    print("Iniciando la fijación del campeón")
    global fijar
    while fijar is None:
        fijar = pyautogui.locateOnScreen('/Lol_bot/Launcher/fijar.png', confidence=0.9)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Fijando el Campeón")
    click = pyautogui.center(fijar)
    pyautogui.click(click)

aceptar_boton()
