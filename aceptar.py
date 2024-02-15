import pyautogui
import time

#Inicializacion de variables
#Se puede trabajar con una global , aunque seria dificl determinar en que parte  fallaria el codigo. 
locacion_boton_aceptar = None
locacion_verificador= None
locacion_bucle = None
boton_comenzar = None
buscador_pick = None
buscador_ban = None
sylas = None
fijar = None
yasuo = None
#Funcion que acepta el boton y pickea sylas. 

def aceptar_boton():
    print("Comenzando el Script, esperando que se encuentre el boton 'Aceptar' ")
    while locacion_boton_aceptar is None:
        locacion_boton_aceptar = pyautogui.locateOnScreen('aceptar.png', confidence=0.7)
        time.sleep(1)
    #if locacion_boton_aceptar is not None :
        #locacion_verificador = pyautogui.locateOnScreen('barra_aceptar_lol.png', confidence=0.7)
        #time.sleep(1) 
    print("Se encontro el boton 'Aceptando la partida'")
    click = pyautogui.center(locacion_boton_aceptar)
    pyautogui.click(click)
    
    print("Esperando a entrar a la partida ")  
    time.sleep(10)
        
    print("Buscando pick : Sylas ")  
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('buscador.png', confidence=0.9)
        time.sleep(1)
    print("Pickea Sylas")     
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    time.sleep(1)
    print("Encontrado")   
    ################################################################
    print("Buscando pick para banear : Yasuo ")  
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('buscador.png', confidence=0.9)
        time.sleep(1)
    print("Baneando Yasuo")     
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('yasuo', interval=0.15)
    time.sleep(1)
    print("Pick Baneado")   
    ################################################################
    print("Buscando pick : Sylas ")  
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('buscador.png', confidence=0.9)
        time.sleep(1)
    print("Pickea Sylas")     
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    time.sleep(1)
    print("Encontrado") 
    ################################################################
    print("Seleccionar Campeon para la partida")  
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