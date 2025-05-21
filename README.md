
# LoL AutoPicker - Automatizador para Selección de Campeones 🎮

## 📌 DESCRIPCIÓN GENERAL

LoL AutoPicker es una herramienta automatizada desarrollada en Python usando `CustomTkinter` que te ayuda a aceptar partidas, seleccionar campeones, banear, y aplicar picks de respaldo en el cliente de **League of Legends** automáticamente. 

Fue creada por necesidad, aunque en realidad fue una emergencia mental provocada por un mononeuronal llamado Enzo Valentino LLapa Arce , mejor conocido en el mundo del hampa como el *92* —un ser al que lamentablemente tengo que llamar amigo. Un pedido suyo se transformó en un proyecto con muchas horas de desarrollo, bugs corregidos a mano y [gpt], testeo en tiempo real y capturas repetidas a las 3am para encontrar la maldita posición exacta del botón de "ACEPTAR".

El .exe esta dentro de "Backend" , "dist". Listo para descargar y usar, aunque se que fallara.

---

## ✨ FUNCIONALIDADES PRINCIPALES

- ✅ **Automatización completa del flujo de selección**:
  - Detecta y hace clic automáticamente en el botón “Aceptar”.
  - Hace el **BAN** y **PICK** automáticamente del campeón seleccionado en la GUI.
  - Si el pick está bloqueado, intenta usar el pick de **salvaguarda**.
  - Detecta dodgeos y reinicia el flujo de forma segura y robusta.

- 🛟 **Modo Salvaguarda**:
  - Si el pick principal no está disponible, usará uno alternativo previamente configurado.

- 🔁 **Reintentos automáticos**:
  - Si alguien se va de la sala, reinicia la espera de nuevo automáticamente.

- 👁️ **Reconocimiento visual**:
  - Usa imágenes `.png` del cliente para identificar fases del juego como búsqueda, ban, pick, etc.

- 💾 **Sistema de caché**:
  - Guarda la última selección en `last_selection.json` para que no tengas que configurar todo de nuevo cada vez.
  - Al iniciar la app, si existe el archivo, se cargan automáticamente los picks previos (aunque solo los que hayan sido visualizados previamente en la GUI).

- 💻 **Interfaz**:
  - Scroll responsivo para seleccionar campeones.
  - Confirmaciones visuales (bordes verdes, amarillos, rojos) para picks, salvaguardas y ban.
  - Sistema de búsqueda integrado para encontrar campeones rápido.
  - Etiquetas siempre visibles mostrando qué campeón ha sido elegido por carril.

---

## 📦 ESTRUCTURA DEL PROYECTO

```
📁 Personajes_pick/       # Imágenes PNG de los campeones
📁 Launcher/              # Plantillas para detectar: aceptar, bloquear, pick, etc.
📁 Lineas/                # Plantillas de cada línea (TOP, MID, JG, ADC, SUPP)
📄 aceptar.py             # Lógica principal de automatización
📄 amarillo.py            # Detección de línea usando franja amarilla y ROI
📄 app.py                 # GUI principal en CustomTkinter
📄 last_selection.json    # Archivo con la última selección hecha por el usuario
```

---

## 📜 FLUJO DETALLADO

1. El sistema inicia en modo BUSQUEDA.
2. Si detecta el botón “Aceptar”, hace clic automáticamente.
3. Entra en fase **BAN**, busca y banea el campeón indicado.
4. Espera la fase **PICK**, detecta automáticamente tu línea (TOP/MID/etc.).
5. Realiza el pick del campeón correspondiente.
6. Si el pick falla, intenta usar la **salvaguarda**.
7. Espera por posibles dodgeos (hasta 150s) y reinicia si ocurre.
8. Si todo sale bien, finaliza con éxito y vuelve al estado inicial.

---

## 🧠 FUNCIONALIDAD DE `amarillo.py` (Detección de Línea) 

Se desarrolló un script separado (`amarillo.py`) que permite detectar automáticamente tu carril (TOP, MID, etc.) basándose en:

- La detección de la **franja amarilla** a la izquierda de tu avatar en la selección , al principio fue dificil determinar como es que a alguien le toca su linea pero.
- A partir de esa franja, se define un **área de interés (ROI)** donde se comparan plantillas guardadas en la carpeta `Lineas`.

Esto permite que el sistema sepa si debe pickear tu TOP, MID, etc., sin que lo configures manualmente.

---

## 🧪 PROBLEMAS COMUNES Y OBSERVACIONES

- 🐛 **OpenCV y capturas**:
  - La función `cv2.matchTemplate()` es costosa, y cuando se ejecuta en bucle continuo (ej: cada 0.1s), puede provocar lentitud **invisible** (no CPU alta, pero sí bloqueo de hilos).
  - Esto se mitiga limitando capturas a intervalos mayores (`time.sleep(1)` o más en algunos casos).

- ⚠️ **Dodgeos**:
  - Si alguien se sale de la partida, se reinicia todo automáticamente.
  - El sistema detecta estos casos gracias a la imagen del botón “Aceptar” reapareciendo.

- 🧊 **Uso de `last_selection.json`**:
  - Este archivo guarda los picks y salvaguardas por línea, y el ban. Al abrir la app, intenta cargar estos datos para facilitar el uso.
  - Sin embargo, solo se marcan visualmente los campeones de las pestañas que hayas visitado (esto es por rendimiento).

- 📸 **Capturas manuales**:
  - Se tomaron capturas reales del cliente de LoL (botones, textos, buscador, estados como "bloqueado", etc.) para lograr una automatización visual robusta.
  - Estas imágenes están en `Launcher/`.

- 🧍‍♂️ **Importancia del usuario ausente**:
  - El programa **no está diseñado para ser usado mientras estás moviendo el mouse o usando la PC activamente**.
  - Ideal para gente que no está frente a su PC durante selección de campeones.

---

## 🚀 EJECUCIÓN DEL PROGRAMA

### 🔧 Requisitos

- Python 3.10 o superior
- Librerías necesarias:

```bash
pip install opencv-python pyautogui numpy Pillow customtkinter
```

### ▶️ Para ejecutar en local (modo desarrollador)

```bash
python app.py
```

### 📦 Para compilar como `.exe` (con PyInstaller)

```bash
pyinstaller --noconfirm --onefile --windowed app.py 
```

Luego de compilar, dentro de `dist/` encontrarás el ejecutable.

---

## 🤬 SOBRE EL INFAME 92
Este proyecto no habría existido sin la gloriosa torpeza de mi amigo 92. Un tipo con la misma precisión que un Teemo full AP con lag. Si el campeón enemigo era "raro", ya se tilteaba. Si le baneaban su pick, lloraba. Y si tenía que aceptar la partida, ¡se iba al baño!

Gracias 92. No por tu ayuda, sino porque sin vos no habría creado una app tan inútil solo para que no arruines nuestras rankeds y luego te andes quejando.

---

## 💬 Final

Puedes compartirlo, clonarlo, mejorarlo... solo no le preguntes a 92 cómo se usa. No queremos otro bug ni que pida mil cosas y para anteayer.

---
## "Adelante Mantengase Firmes"
