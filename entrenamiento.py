import pyautogui
import time

def aceptar_boton():
#Optimizar estas variables , para que se trabje con una sola, aunque la identificaicon de problemas seria mas dificil 
#Proceso para entrenamiento
#Inicializacion de variables
    locacion_boton_aceptar = None
    boton_comenzar = None
    buscador_pick = None
    buscador_ban = None
    sylas = None
    fijar = None
    yasuo = None

    print("Comenzando el Script, esperando a comenzar partida la partida")
    

    while locacion_boton_aceptar is None:
        locacion_boton_aceptar = pyautogui.locateOnScreen('comenzar.png', confidence=0.7)
        time.sleep(1)
    print("Se encontro el boton, aceptando partida")
    click = pyautogui.center(locacion_boton_aceptar)
    pyautogui.click(click)
    
    print("Siguiente paso")  
    time.sleep(10)
    
    if locacion_boton_aceptar is None == 0:  # True
        print("z is even")
        
    print("Buscador de pick ")  
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('buscador.png', confidence=0.9)
        time.sleep(1)
    print("Pickea Sylas ")     
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    time.sleep(1)
    print("Exito")   
    ################################################################
    print("Seleccionar Campeon")  
    while sylas is None:
        sylas = pyautogui.locateOnScreen('sylas.png', confidence=0.9)
        time.sleep(1)
    print("Pickea Sylas ")     
    click = pyautogui.center(sylas)
    pyautogui.click(click)
    time.sleep(1)
    ################################################################
    print("Empieza la fijacion")  
    while fijar is None:
        fijar = pyautogui.locateOnScreen('fijar.png', confidence=0.9)
        time.sleep(1)
    print("Fija ")     
    click = pyautogui.center(fijar)
    pyautogui.click(click)
    time.sleep(1)
    """
    print ("Salir partida")
    while fijar is None:
        fijar = pyautogui.locateOnScreen('salir.png', confidence=0.9)
        time.sleep(1)
    print("Fija ")     
    click = pyautogui.center(fijar)
    pyautogui.click(click)
    time.sleep(1)
    """
aceptar_boton()