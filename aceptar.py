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
bloquear_button =None
# Función que acepta el botón y pickea Sylas.
def aceptar_boton():
    print("Comenzading, esperando que se encuentre el botón 'Aceptar'")
    '''
    global locacion_boton_aceptar
    # Esperar hasta que se encuentre el botón 'Aceptar'
    while locacion_boton_aceptar is None:
        locacion_boton_aceptar = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/aceptar.jpg', confidence=0.7)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Se encontró el botón 'Aceptando la partida'")
    click = pyautogui.center(locacion_boton_aceptar)
    pyautogui.click(click)
    
    print("Esperando a entrar a la partida...")
    '''
    # Buscar y seleccionar Sylas
    print("Buscando pick: Sylas")
    global buscador_pick
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscador.png', confidence=0.7)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU

    print("Pickeando Sylas")
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    print("Sylas encontrado")
    
     # ahora pickear al persoanej para que sepan que lo vas a llevary no lo baneen 
    print("Buscando pick: Sylas")
    buscador_pick = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Personajes_pick/sylas.png', confidence=0.7)
    time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Pickeando Sylas")
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    print("Sylas seleccionado")

    # Banear Leblanc
    print("Buscando pick para banear: leblanc")
    global buscador_ban
    while buscador_ban is None:
        buscador_ban = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Personajes_pick/Leblanc.png', confidence=0.7)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Baneando Leblanc")
    click = pyautogui.center(buscador_ban)
    pyautogui.click(click)
    pyautogui.write('yasuo', interval=0.15)
    print("Leblanc baneado")

    print ("Dandole a bloquear")
    global bloquear_button
    while bloquear_button is None:
        bloquear_button = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/bloqueo.png', confidence=0.7)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Baneando Leblanc")
    click = pyautogui.center(bloquear_button)
    pyautogui.click(click)
    print("Leblanc baneado")
    
    # Seleccionar nuevamente Sylas (ahora para pickear el otro solo era para saber que lo ibas a tener)
    print("Buscando pick: Sylas")
    buscador_pick = None  # Resetear la variable para evitar conflictos
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscador.png', confidence=0.7)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Pickeando Sylas nuevamente")
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    print("Sylas encontrado nuevamente")

      # ahora pickear al persoanej para que sepan que lo vas a llevary no lo baneen 
    print("Buscando pick: Sylas")
    buscador_pick = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Personajes_pick/sylas.png', confidence=0.7)
    time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Pickeando Sylas")
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    print("Sylas seleccionado")
    
    # Seleccionar Sylas para la partida
    print("Seleccionando Campeón para la partida")
    global fijar
    while fijar is None:
        fijar = pyautogui.locateOnScreen('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/fijar.png', confidence=0.7)
        time.sleep(1)  # Espera de 1 segundo para evitar sobrecargar el CPU
    print("Seleccionando Sylas")
    click = pyautogui.center(fijar)
    pyautogui.click(click)
aceptar_boton()
