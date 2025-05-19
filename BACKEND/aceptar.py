import pyautogui
import time
import os
import cv2
import numpy as np
import sys 
import os
from enum import Enum
class State(Enum):
    BUSQUEDA   = 1
    WAIT_BAN   = 2
    BAN        = 3
    WAIT_PICK  = 4
    PICK       = 5
    DONE       = 6

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

def esperar_imagen(ruta_objetivo, timeout=30, ruta_boton_aceptar=None, th_objetivo=0.85, th_boton=0.85, stop_event=None):
    print(f"🔎 Esperando imagen objetivo: {ruta_objetivo} (máx {timeout}s)")
    t0 = time.time()
    img_objetivo = cv2.imread(ruta_objetivo)
    tpl_boton = cv2.imread(ruta_boton_aceptar) if ruta_boton_aceptar else None

    if img_objetivo is None:
        print(f"❌ Error: imagen objetivo no cargada desde {ruta_objetivo}")
        return False

    while time.time() - t0 < timeout:
        if stop_event and stop_event.is_set():
            print("🛑 Detención solicitada por stop_event durante espera de imagen.")
            return False

        screen = pyautogui.screenshot()
        screen_bgr = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

        if tpl_boton is not None:
            res_boton = cv2.matchTemplate(screen_bgr, tpl_boton, cv2.TM_CCOEFF_NORMED)
            max_val_boton = res_boton.max()
            print(f"[DEBUG] Comparación botón aceptar: max_val = {max_val_boton:.3f}")
            if max_val_boton >= th_boton:
                print("🔁 Dodge detectado durante espera. Reiniciando flujo.")
                return "DODGE"

        res = cv2.matchTemplate(screen_bgr, img_objetivo, cv2.TM_CCOEFF_NORMED)
        max_val_obj = res.max()
        print(f"[DEBUG] Comparación {ruta_objetivo}: max_val = {max_val_obj:.3f}")
        if max_val_obj >= th_objetivo:
            print(f"✅ Imagen encontrada: {ruta_objetivo}")
            return True

        time.sleep(0.5)

    print(f"❌ Timeout esperando: {ruta_objetivo}")
    return False


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
                            ruta_boton_aceptar, stop_event,
                            confianza=0.85, timeout=60):
    print(f"Esperando pantalla de baneo: {ruta_marker_ban}")
    res = esperar_imagen(ruta_marker_ban, timeout=timeout, ruta_boton_aceptar=ruta_boton_aceptar)
    if res == "DODGE" or (stop_event and stop_event.is_set()):
        return "DODGE"
    elif not res:
        print(f"Error: No se detectó la pantalla de bloqueo ({ruta_marker_ban}) tras {timeout}s.")
        return False

    print(f"📢 Tras detectar bloqueo, baneando al campeón: {campeon}")

    tpl_bus = cv2.imread(ruta_buscador)
    h_bus, w_bus = tpl_bus.shape[:2]
    print(f"Buscando en el buscador al campeón: {campeon}")
    while True:
        if stop_event and stop_event.is_set():
            print("⛔ Interrumpido durante el ban (buscador).")
            return False

        screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        if existe_imagen(ruta_boton_aceptar, confianza):
            print("🔁 Dodge detectado en buscador. Reiniciando flujo.")
            return "DODGE"

        res = cv2.matchTemplate(screen, tpl_bus, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confianza)
        if loc[0].size:
            y, x = loc[0][0], loc[1][0]
            pyautogui.click(x + w_bus//2, y + h_bus//2)
            pyautogui.write(campeon, interval=0.07)
            break
        time.sleep(0.5)

    tpl_cam = cv2.imread(ruta_campeon)
    h_cam, w_cam = tpl_cam.shape[:2]
    inicio = time.time()
    while time.time() - inicio < timeout:
        if stop_event and stop_event.is_set():
            print("⛔ Interrumpido durante el ban (campeón).")
            return False

        screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        if existe_imagen(ruta_boton_aceptar, confianza):
            print("🔁 Dodge detectado en imagen campeón. Reiniciando flujo.")
            return "DODGE"

        res = cv2.matchTemplate(screen, tpl_cam, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confianza)
        if loc[0].size:
            y, x = loc[0][0], loc[1][0]
            pyautogui.click(x + w_cam//2, y + h_cam//2)
            print(f"{campeon} seleccionado para ban.")
            if hacer_click_boton(ruta_click_boton_ban):
                print("✅ Clic en el botón de ban ejecutado.")
            else:
                print("❌ Error al clicar botón de ban.")
            limpiar_buscador(ruta_buscador)
            return True
        time.sleep(0.5)

    print(f"Error: no se encontró {campeon} en pantalla tras {timeout}s.")
    return False


TH_BUS      = 0.85  
TH_BUS_MIN  = 0.60   
TIMEOUT_BUS = 5     
def seleccionar_campeon_pick(campeon, ruta_buscador, ruta_campeon, ruta_boton,
                              ruta_boton_aceptar, ruta_label_bloqueo, stop_event=None):
    print(f"🔎 Buscando en el buscador al campeón: {campeon}")

    tpl_bus = cv2.imread(ruta_buscador)
    tpl_cam = cv2.imread(ruta_campeon)
    tpl_bloq = cv2.imread(ruta_label_bloqueo)
    if tpl_bus is None or tpl_cam is None or tpl_bloq is None:
        print("❌ Faltan plantillas de buscador, campeón o bloqueo.")
        return False

    h_cam, w_cam = tpl_cam.shape[:2]

    limpiar_buscador(ruta_buscador)
    time.sleep(0.2)

    
    for _ in range(10):
        if stop_event and stop_event.is_set():
            print("⛔ Cancelado por stop_event (buscador).")
            return False

        screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

        if existe_imagen(ruta_boton_aceptar, 0.85):
            print("🔁 Dodge detectado antes de escribir. Reiniciando flujo.")
            return "DODGE"

        res = cv2.matchTemplate(screen, tpl_bus, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.85)
        if loc[0].size:
            y, x = loc[0][0], loc[1][0]
            pyautogui.click(x + tpl_bus.shape[1] // 2, y + tpl_bus.shape[0] // 2)
            pyautogui.write(campeon, interval=0.07)
            break
        time.sleep(0.5)
    else:
        print("❌ No encontré el buscador tras varios intentos.")
        return False

    time.sleep(0.8)  

    start = time.time()
    MAX_PICK_TIMEOUT = 6  
    while time.time() - start < MAX_PICK_TIMEOUT:
        if stop_event and stop_event.is_set():
            print("⛔ Cancelado por stop_event (pick).")
            return False

        screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

        if existe_imagen(ruta_boton_aceptar, 0.85):
            print("🔁 Dodge detectado en pick. Reiniciando flujo.")
            return "DODGE"

        res = cv2.matchTemplate(screen, tpl_cam, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.85)
        if not loc[0].size:
            time.sleep(0.5)
            continue

        for y0, x0 in zip(loc[0], loc[1]):
            cx, cy = x0 + w_cam // 2, y0 + h_cam // 2
            pyautogui.moveTo(cx, cy)
            time.sleep(0.5)

            screen2 = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
            res2 = cv2.matchTemplate(screen2, tpl_bloq, cv2.TM_CCOEFF_NORMED)
            if (res2 >= 0.85).any():
                print(f"⚠️ Campeón {campeon} bloqueado al hover.")
                return False

            pyautogui.click(cx, cy)
            print(f"✅ {campeon} seleccionado.")
            limpiar_buscador(ruta_buscador)
            time.sleep(0.2)

            if hacer_click_boton(ruta_boton):
                print("✅ Clic en el botón de pick ejecutado.")
                return True
            else:
                print("❌ Error al hacer clic en el botón de pick.")
                return False

        time.sleep(0.5)

    print(f"❌ No se encontró el campeón {campeon} en pantalla tras {MAX_PICK_TIMEOUT}s.")
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

        time.sleep(1)

    print("Error: No se encontró el botón.")
    return False

def dodge_detectado(ruta_boton_aceptar, confianza=0.85):
    if existe_imagen(ruta_boton_aceptar, confianza):
        print("🔁 Dodge detectado global. Reiniciando flujo desde BUSQUEDA.")
        return True
    return False

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
    max_val = res.max()
    print(f"[DEBUG] Comparación {ruta}: max_val = {max_val:.3f}")
    return max_val >= confianza

def resource_path(rel_path: str) -> str:
    """
    Devuelve la ruta absoluta para datos en dev o dentro del .exe de PyInstaller.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

def ejecutar_seleccion(campeon_pick, campeon_ban, campeon_salvaguarda=None, stop_event=None):
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

    for p in (ruta_campeon_pick, ruta_campeon_ban, ruta_marker_pick):
        if not os.path.exists(p):
            print(f"❌ Archivo no encontrado: {p}")
            return False

    state = State.BUSQUEDA
    accept_last = False
    print("🚀 Iniciando flujo (reinicio automático si hay dodge)…")

    while True:
        if stop_event and stop_event.is_set():
            print("⛔ Cancelado por stop_event.")
            return False

        curr = existe_imagen(ruta_boton_aceptar, TH)

        if curr and not accept_last:
            print("🔁 Botón 'Aceptar' detectado de nuevo, reiniciando flujo desde BUSQUEDA…")
            esperar_y_aceptar_partida(ruta_boton_aceptar, confianza=TH, tiempo_espera=1)
            time.sleep(0.5)
            state = State.WAIT_BAN
            accept_last = True
            continue

        accept_last = curr

        if state == State.BUSQUEDA:
            time.sleep(0.5)
            continue

        elif state == State.WAIT_BAN:
            print(f"⏳ Esperando fase de ban ({ruta_marker_ban})…")
            res = esperar_imagen(ruta_marker_ban, timeout=600, ruta_boton_aceptar=ruta_boton_aceptar, stop_event=stop_event)

            if stop_event and stop_event.is_set():
                print("⛔ Cancelado por stop_event en WAIT_BAN.")
                return False
            if res == "DODGE":
                print("🔁 Dodge detectado en espera ban.")
                state = State.BUSQUEDA
                continue
            elif not res:
                print("❌ No llegó fase de ban.")
                return False
            print("✅ Fase de ban detectada.")
            state = State.BAN

        elif state == State.BAN:
            res = seleccionar_campeon_ban(
                campeon_ban,
                ruta_buscador,
                ruta_campeon_ban,
                ruta_click_boton_ban,
                ruta_marker_ban,
                ruta_boton_aceptar,
                confianza=TH,
                timeout=60,
                stop_event=stop_event
            )
            if res == "DODGE":
                print("🔁 Dodge detectado en BAN.")
                state = State.BUSQUEDA
                continue
            elif not res:
                return False
            state = State.WAIT_PICK

        elif state == State.WAIT_PICK:
            print(f"⏳ Esperando pantalla de pick ({ruta_marker_pick})…")
            res = esperar_imagen(ruta_marker_pick, timeout=600, ruta_boton_aceptar=ruta_boton_aceptar, stop_event=stop_event)

            if stop_event and stop_event.is_set():
                print("⛔ Cancelado por stop_event en WAIT_PICK.")
                return False
            if res == "DODGE":
                print("🔁 Dodge detectado en espera pick.")
                state = State.BUSQUEDA
                continue
            elif not res:
                print("❌ No apareció pantalla de pick.")
                return False
            print("✅ Pantalla de pick detectada.")
            state = State.PICK

        elif state == State.PICK:
            print("🎯 Realizando pick final…")
            res = seleccionar_campeon_pick(
                campeon_pick,
                ruta_buscador,
                ruta_campeon_pick,
                ruta_fijar_boton,
                ruta_boton_aceptar,
                ruta_label_bloqueo,
                stop_event=stop_event
            )
            if res == "DODGE":
                print("🔁 Dodge detectado durante pick final.")
                state = State.BUSQUEDA
                continue

            if not res and campeon_salvaguarda:
                print(f"⚠️ Usando salvaguarda: {campeon_salvaguarda}")
                limpiar_buscador(ruta_buscador)
                ruta_campeon_pick = resource_path(f'Personajes_pick/{campeon_salvaguarda}.png')
                res = seleccionar_campeon_pick(
                    campeon_salvaguarda,
                    ruta_buscador,
                    ruta_campeon_pick,
                    ruta_fijar_boton,
                    ruta_boton_aceptar,
                    ruta_label_bloqueo,
                    stop_event=stop_event
                )
                if res == "DODGE":
                    print("🔁 Dodge detectado durante pick con salvaguarda.")
                    state = State.BUSQUEDA
                    continue
                if res:
                    campeon_pick = campeon_salvaguarda
                    print(f"✅ Salvaguarda {campeon_salvaguarda} pickeada con éxito.")
                else:
                    print(f"❌ Falló también el pick de salvaguarda.")
                    return False
            elif not res:
                print(f"❌ No se pudo pickear {campeon_pick} y no hay salvaguarda definida.")
                return False

            print("⏳ Esperando post-pick por posibles dodges (hasta 150s)...")
            for _ in range(150):
                if stop_event and stop_event.is_set():
                    print("⛔ Cancelado por stop_event durante espera post-pick.")
                    return False
                if existe_imagen(ruta_boton_aceptar, TH):
                    print("🔁 Dodge detectado post-pick. Reiniciando flujo.")
                    esperar_y_aceptar_partida(ruta_boton_aceptar, confianza=TH, tiempo_espera=5)
                    state = State.WAIT_BAN
                    break
                time.sleep(1)
            else:
                print("✅ Pick realizado con éxito.")
                return True

        time.sleep(0.1)

#Este scriot permite automatizar el proceso de selección de campeones en League of Legends.
# Se basa en la detección de imágenes para interactuar con la interfaz del juego.
# El flujo de trabajo incluye la espera de la pantalla de baneo, la selección del campeón a banear,
# la espera de la pantalla de selección de campeones y finalmente la selección del campeón deseado.