import pyautogui
import time
import os
import cv2
import numpy as np
import sys 
import os
from enum import Enum
# Definición de los estados de la máquina de estados
class State(Enum):
    BUSQUEDA   = 1
    WAIT_BAN   = 2
    BAN        = 3
    WAIT_PICK  = 4
    PICK       = 5
    DONE       = 6

# Función que espera hasta que el botón 'Aceptar' aparezca en la pantalla y hace clic en él.
def esperar_y_aceptar_partida(ruta_boton_aceptar: str,
                              confianza: float = 0.85,
                              tiempo_espera: float = 500) -> dict:
    """
    Espera hasta que el botón 'Aceptar' aparezca y hace clic en él.
    Devuelve {'success': bool, 'elapsed': float}.
    """
    print(f"Esperando el botón de aceptar: {ruta_boton_aceptar}")
    inicio = time.time()
    try:
        template = cv2.imread(ruta_boton_aceptar)
        h, w = template.shape[:2]
    except Exception as e:
        print(f"Error al cargar plantilla: {e}")
        return {'success': False, 'elapsed': 0.0}

    while True:
        elapsed = time.time() - inicio
        if elapsed > tiempo_espera:
            return {'success': False, 'elapsed': elapsed}

        screenshot = pyautogui.screenshot()
        screen_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confianza)

        if loc[0].size:
            x, y = loc[1][0], loc[0][0]
            pyautogui.click(x + w//2, y + h//2)
            print("Botón de aceptar clickeado.")
            return {'success': True, 'elapsed': elapsed}

        time.sleep(1)

def esperar_imagen(ruta_imagen_media, timeout=6000):
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
def limpiar_buscador(
    ruta_buscador: str,
    confianza: float = 0.90,
    min_conf: float = 0.70,
    timeout: float = 10
) -> bool:
    """
    Hace clic en el buscador y limpia el texto dentro.
    Primero intenta con 'confianza', si no lo encuentra en 'timeout/2' segundos,
    baja el umbral a 'min_conf' y vuelve a intentar hasta el timeout total.
    """
    tpl = cv2.imread(ruta_buscador)
    if tpl is None:
        print(f"❌ No existe plantilla buscador: {ruta_buscador}")
        return False
    h, w = tpl.shape[:2]
    inicio = time.time()
    mitad = inicio + timeout/2

    while time.time() - inicio < timeout:
        screenshot = cv2.cvtColor(
            np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR
        )
        res = cv2.matchTemplate(screenshot, tpl, cv2.TM_CCOEFF_NORMED)

        # Decide umbral dinámico
        umbral = confianza if time.time() < mitad else min_conf
        loc = np.where(res >= umbral)

        if loc[0].size:
            y, x = loc[0][0], loc[1][0]
            cx, cy = x + w//2, y + h//2
            if umbral < confianza:
                print(f"⚠️ Buscador detectado con confianza reducida ({res.max():.2f})")
            pyautogui.click(cx, cy)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            return True

        time.sleep(0.3)

    print(f"❌ Timeout limpiando buscador (max_conf={res.max():.2f})")
    return False

def pre_pick_campeon(campeon, ruta_buscador, ruta_campeon):
    print(f"Buscando en el buscador al campeón: {campeon}")      

    while True:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        buscador_pick = cv2.imread(ruta_buscador)
        result = cv2.matchTemplate(screenshot, buscador_pick, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.85)
        # Si se encuentra el buscador   
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
                            print(f"{campeon} seleccionado. Siguiendo con el Baneo")
                            limpiar_buscador(ruta_buscador)  

                            return True

                print(f"Error: No se encontró la imagen del campeón {campeon} en la pantalla.")
                return False

def seleccionar_campeon_ban(campeon, ruta_buscador, ruta_campeon,
                            ruta_click_boton_ban, ruta_marker_ban,
                            confianza=0.85, timeout=6000):
    """
    Espera la pantalla de ban, luego busca y hace clic en el campeón a banear.
    """
    # 1. Detectar fase de ban
    print(f"Esperando pantalla de baneo: {ruta_marker_ban}")
    if not esperar_imagen(ruta_marker_ban, timeout=timeout):
        print(f"Error: No se detectó la pantalla de bloqueo ({ruta_marker_ban}) tras {timeout}s.")
        return False
    print(f"📢 Tras detectar bloqueo, baneando al campeón: {campeon}")

    # 2. Búsqueda en el buscador
    tpl_bus = cv2.imread(ruta_buscador)
    h_bus, w_bus = tpl_bus.shape[:2]
    print(f"Buscando en el buscador al campeón: {campeon}")      
    while True:
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(screen, tpl_bus, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confianza)
        # Si se encuentra el buscador
        if loc[0].size:
            y, x = loc[0][0], loc[1][0]
            pyautogui.click(x + w_bus//2, y + h_bus//2)
            pyautogui.write(campeon, interval=0.07)
            break
        time.sleep(1)
        
    # 3. Esperar y click en la miniatura del campeón
    tpl_cam = cv2.imread(ruta_campeon)
    h_cam, w_cam = tpl_cam.shape[:2]
    inicio = time.time()
    while time.time() - inicio < timeout:
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(screen, tpl_cam, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confianza)
        if loc[0].size:
            y, x = loc[0][0], loc[1][0]
            pyautogui.click(x + w_cam//2, y + h_cam//2)
            print(f"{campeon} seleccionado para ban.")
            # 4. Click en el botón de bloqueo
            if hacer_click_boton(ruta_click_boton_ban):
                print("✅ Clic en el botón de ban ejecutado.")
            else:
                print("❌ Error al clicar botón de ban.")
            # 5. Limpia el buscador
            limpiar_buscador(ruta_buscador)
            return True
        time.sleep(0.5)

    print(f"Error: no se encontró {campeon} en pantalla tras {timeout}s.")
    return False

TH_BUS      = 0.85   # umbral alto
TH_BUS_MIN  = 0.60   # umbral bajo si no lo encuentra con el alto
TIMEOUT_BUS = 5      # segundos totales para limpiar 
def seleccionar_campeon_pick(campeon, ruta_buscador, ruta_campeon, ruta_boton, ruta_label_bloqueo='./Launcher/bloqueado.png'):
    """
    1) Limpia el buscador y escribe el nombre.
    2) Espera la miniatura del campeón en color.
    3) Al hacer hover, comprueba si aparece el tooltip “Bloqueado”:
         - Si lo ve, devuelve False para que use la salvaguarda.
    4) Si no está bloqueado, hace click en la miniatura, luego en “Fijar” y limpia.
    """
    print(f"Buscando en el buscador al campeón: {campeon}")

    # 1) Click en buscador y escribe
    tpl_bus = cv2.imread(ruta_buscador)
    limpiar_buscador(
    ruta_buscador,
    confianza=TH_BUS,
    min_conf=TH_BUS_MIN,
    timeout=TIMEOUT_BUS
    )
    time.sleep(0.2)

    screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(screen, tpl_bus, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.85)
    if not loc[0].size:
        print("❌ No encontré el buscador.")
        return False
    yb, xb = loc[0][0], loc[1][0]
    pyautogui.click(xb + tpl_bus.shape[1]//2, yb + tpl_bus.shape[0]//2)
    pyautogui.write(campeon, interval=0.07)
    time.sleep(1)

    # 2) Carga plantillas
    tpl_cam = cv2.imread(ruta_campeon)
    tpl_bloq = cv2.imread(ruta_label_bloqueo)
    if tpl_cam is None or tpl_bloq is None:
        print("❌ Faltan plantillas de campeón o de bloqueado.")
        return False
    h_cam, w_cam = tpl_cam.shape[:2]

    # 3) Busca la miniatura y procesa cada candidato
    start = time.time()
    while time.time() - start < 60:
        screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(screen, tpl_cam, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.85)
        if not loc[0].size:
            time.sleep(0.5)
            continue

        for y0, x0 in zip(loc[0], loc[1]):
            cx, cy = x0 + w_cam//2, y0 + h_cam//2

            # hover
            pyautogui.moveTo(cx, cy)
            time.sleep(0.5)

            # 3a) comprueba overlay “Bloqueado”
            screen2 = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
            res2 = cv2.matchTemplate(screen2, tpl_bloq, cv2.TM_CCOEFF_NORMED)
            if (res2 >= 0.85).any():
                print(f"⚠️ Campeón {campeon} bloqueado al hover.")
                return False

            # 4) click en miniatura
            pyautogui.click(cx, cy)
            print(f"{campeon} seleccionado.")
           
            # 🚿 Limpiar el buscador justo tras clicar la miniatura
            limpiar_buscador(
                ruta_buscador,
                confianza=TH_BUS,
                min_conf=TH_BUS_MIN,
                timeout=TIMEOUT_BUS
            )
            time.sleep(0.2)

            # 5) click en “Fijar”
            if hacer_click_boton(ruta_boton):
                print("Clic en el botón exitoso.")
            else:
                print("Error: No se pudo hacer clic en el botón.")
                return False

            return True

        time.sleep(0.5)

    print(f"Error: No se encontró la imagen del campeón {campeon} en pantalla.")
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

def existe_imagen(ruta, confianza=0.85):
    tpl = cv2.imread(ruta)
    if tpl is None:
        return False
    screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
    return (res >= confianza).any()

def esperar_a_desaparecer(ruta, espera=10, confianza=0.85):
    """Espera hasta que la imagen deje de estar en pantalla."""
    t0 = time.time()
    while time.time() - t0 < espera:
        if not existe_imagen(ruta, confianza):
            return True
        time.sleep(0.5)
    return False

def existe_imagen(ruta: str, confianza: float) -> bool:
    tpl = cv2.imread(ruta)
    if tpl is None:
        print(f"❌ Plantilla no encontrada: {ruta}")
        return False
    screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
    return (res >= confianza).any()

# ——— Helpers para resolución de rutas ———
def resource_path(rel_path: str) -> str:
    """
    Devuelve la ruta absoluta para datos en dev o dentro del .exe de PyInstaller.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

def ejecutar_seleccion(campeon_pick, campeon_ban, campeon_salvaguarda=None, stop_event=None) -> bool:
    """
    Flujo simplificado: auto-acept, ban y pick final (solo imágenes a color).
    stop_event: threading.Event opcional para cancelar el flujo.
    """

    # Resolución de todos los paths
    ruta_buscador        = resource_path('Launcher/buscador1.0.png')
    ruta_fijar_boton     = resource_path('Launcher/fijar.png')
    ruta_click_boton_ban = resource_path('Launcher/bloqueo2.png')
    ruta_boton_aceptar   = resource_path('Launcher/aceptar.png')
    ruta_marker_ban      = resource_path('Launcher/BloqueoLetras.png')
    ruta_label_bloqueo   = resource_path('Launcher/bloqueado.png')
    ruta_marker_pick     = resource_path('Launcher/selecciona_tu_campeon.png')
    ruta_campeon_pick    = resource_path(f'Personajes_pick/{campeon_pick}.png')
    ruta_campeon_ban     = resource_path(f'Personajes_pick/{campeon_ban}.png')
    TH = 0.85

    # Validación de archivos
    for p in (ruta_campeon_pick, ruta_campeon_ban, ruta_marker_pick):
        if not os.path.exists(p):
            print(f"Error: archivo no encontrado: {p}")
            return False

    state = State.BUSQUEDA
    accept_last = False
    print("🚀 Iniciando flujo (sin pre-pick ni B/N)…")

    while True:
        # Chequeo de cancelación
        if stop_event and stop_event.is_set():
            print("⚠️ Flujo cancelado por stop_event.")
            return False

        # Auto-click “Aceptar”
        curr = existe_imagen(ruta_boton_aceptar, TH)
        if curr and not accept_last:
            print("🔄 'Aceptar' detectado, clickeando y continuando…")
            esperar_y_aceptar_partida(ruta_boton_aceptar, confianza=TH, tiempo_espera=1)
            time.sleep(0.5)
            state = State.WAIT_BAN
            print ("nos encontradmos en la fase de "+ state.name)
        accept_last = curr

        if state == State.BUSQUEDA:
            time.sleep(0.5)
            continue

        elif state == State.WAIT_BAN:
            print(f"⏳ Esperando fase de ban ({ruta_marker_ban})…")
            if not esperar_imagen(ruta_marker_ban, timeout=6000):
                print("❌ No llegó fase de ban.")
                return False
            print("✅ Fase de ban detectada.")
            state = State.BAN

        elif state == State.BAN:
            print("🔨 Baneando campeón…")
            if not seleccionar_campeon_ban(
                campeon_ban,
                ruta_buscador,
                ruta_campeon_ban,
                ruta_click_boton_ban,
                ruta_marker_ban
            ):
                return False
            state = State.WAIT_PICK

        elif state == State.WAIT_PICK:
            print(f"⏳ Esperando pantalla de pick ({ruta_marker_pick})…")
            if not esperar_imagen(ruta_marker_pick, timeout=6000):
                print("❌ No apareció pantalla de pick.")
                return False
            print("✅ Pantalla de pick detectada.")
            state = State.PICK

        elif state == State.PICK:
            print("🎯 PICK final…")

            ruta_label_bloqueo = './Launcher/bloqueado.png'

            # 1) Intento con el pick original (incluye hover + check “Bloqueado”)
            ok = seleccionar_campeon_pick(
                campeon_pick,
                ruta_buscador,
                ruta_campeon_pick,
                ruta_fijar_boton,
                ruta_label_bloqueo  # <-- aquí le pasas la plantilla del tooltip
            )
            if ok:
                print(f"✅ Campeón original “{campeon_pick}” pickeado correctamente.")
            else:
                # 2) Si hay salvaguarda, limpio el buscador y pruebo de nuevo
                if campeon_salvaguarda:
                    print(f"⚠️ Usando salvaguarda: {campeon_salvaguarda}")
                    limpiar_buscador(ruta_buscador)
                    time.sleep(0.2)

                    ruta_campeon_pick = f'./Personajes_pick/{campeon_salvaguarda}.png'
                    ok = seleccionar_campeon_pick(
                        campeon_salvaguarda,
                        ruta_buscador,
                        ruta_campeon_pick,
                        ruta_fijar_boton,
                        ruta_label_bloqueo
                    )
                    if ok:
                        print(f"✅ Salvaguarda “{campeon_salvaguarda}” pickeada con éxito.")
                        campeon_pick = campeon_salvaguarda
                    else:
                        print(f"❌ Falló también el pick de salvaguarda “{campeon_salvaguarda}”.")
                else:
                    print(f"❌ No se pudo pickear “{campeon_pick}” y no hay salvaguarda definida.")

            # 3) Abortamos si no hubo éxito
            if not ok:
                return False

            print("✅ Flujo completado correctamente.")
            return True

        time.sleep(0.1)
