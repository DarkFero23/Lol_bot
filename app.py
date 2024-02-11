import pyautogui
import time

def aceptar_boton():
#Optimizar estas variables , para que se trabje con una sola, aunque la identificaicon de problemas seria mas dificil 
#Proceso para entrenamiento
    locacion_boton_aceptar = None
    boton_comenzar = None
    buscador_pick = None
    buscador_ban = None
    sylas = None
    fijar = None
    yasuo = None
    
    
    print("Comenzo")
    while boton_comenzar is None:
        boton_comenzar = pyautogui.locateOnScreen('Comenzar.png', confidence=0.7)
        time.sleep(1)
    print("Econtro el boton comenzar")
    click = pyautogui.center(boton_comenzar)
    pyautogui.click(click)
    print("Siguiente paso")  
    time.sleep(1)
    print("Buscador de pick ")  
    while buscador_pick is None:
        buscador_pick = pyautogui.locateOnScreen('buscador.png', confidence=0.9)
        time.sleep(1)
    print("Pickea Sylas ")     
    click = pyautogui.center(buscador_pick)
    pyautogui.click(click)
    pyautogui.write('sylas', interval=0.15)
    

    #print("Exito")
    time.sleep(1)
    print("Exito")   
    
    print("Seleccionar Campeon")  
    while sylas is None:
        sylas = pyautogui.locateOnScreen('sylas.png', confidence=0.9)
        time.sleep(1)
    print("Pickea Sylas ")     
    click = pyautogui.center(sylas)
    pyautogui.click(click)
    time.sleep(1)
         
    print("Empieza la fijacion")  
    while fijar is None:
        fijar = pyautogui.locateOnScreen('fijar.png', confidence=0.9)
        time.sleep(1)
    print("Fija ")     
    click = pyautogui.center(fijar)
    pyautogui.click(click)
    time.sleep(1)

aceptar_boton()