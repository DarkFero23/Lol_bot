LoL AutoPicker - Automatizador para Selección de Campeones 🎮

📌 DESCRIPCIÓN GENERAL
───────────────────────
LoL AutoPicker es una herramienta automatizada desarrollada en Python con CustomTkinter para ayudarte a seleccionar, banear y asegurar campeones automáticamente en el cliente de League of Legends (LoL). 
Está pensada especialmente para jugadores que, por distintos motivos (estar lejos del teclado, conversando con su mamá o papá, preparando algo en casa, etc.), 
no pueden estar frente a su PC durante la fase de “Aceptar partida” o en la selección de campeones. 
Nació como un proyecto personal a raíz del pedido de un mononeuronal llamado 92 (a quien, lamentablemente, tengo que llamar amigo). 
Lo que empezó como una solución a su torpeza para seleccionar campeones terminó evolucionando en una herramienta útil para cualquier jugador de LoL que quiera automatizar su selección de campeones.

✨ PRINCIPALES FUNCIONALIDADES

───────────────────────────────

✅ Automatización completa del flujo de selección:
  - Detecta automáticamente el botón “Aceptar” al inicio de la partida y responde al instante.  
  - Realiza BAN y PICK automáticamente con el campeón indicado desde la GUI.  
  - Si el campeón está bloqueado, intenta usar el campeón de "salvaguarda".  
  - Detecta *dodges* en cualquier fase (ban, pick, post-pick) y reinicia todo sin errores.  
  - Totalmente interactivo y controlado desde una interfaz gráfica con botones e imágenes.  

🛟 Modo Salvaguarda:
   Si el campeón principal no está disponible (por estar baneado u ocupado),
   se activa automáticamente un segundo pick alternativo que se selecciona en la GUI.

🔄 Reintentos automáticos tras dodgeos:
   Si alguien se sale de la sala o la partida es cancelada, LoL AutoPicker
   reinicia el flujo sin intervención del usuario.

👁️ Detecta el estado del cliente LoL mediante imágenes:
   - Se basa en plantillas PNG de elementos del cliente.
   - Utiliza reconocimiento visual para saber si estás en fase de ban, pick o aceptación.

🖱️ Control de errores:
   - Se detiene automáticamente si el usuario pulsa "Reiniciar".
   - Respeta hilos activos y asegura que todo se reinicie sin dejar procesos colgados.

💡 DISEÑO DE LA INTERFAZ

────────────────────────
- UI moderna en modo oscuro (CustomTkinter).
- Botones grandes e intuitivos para confirmar Pick, Ban y Salvaguarda.
- Vista previa de los campeones en scroll responsivo.
- Indicadores claros de qué campeón está elegido para cada fase.
- Estado actual siempre visible ("BUSQUEDA", "BAN", "PICK", etc.).

📦 ESTRUCTURA DEL SISTEMA

──────────────────────────

📁 /Personajes_pick/
→ Carpeta donde debes colocar las imágenes PNG de los campeones.
→ Importante: usa imágenes oficiales claras y con buena resolución.

📁 /Launcher/
→ Aquí están los templates necesarios para detectar fases como:
   - aceptar.png
   - bloqueo2.png
   - buscador.png
   - selecciona_tu_campeon.png
   - bloqueado.png

📜 FUNCIONAMIENTO DETALLADO

────────────────────────────

1. **Búsqueda**: Se detecta automáticamente cuando el cliente está buscando partida.
2. **Aceptar**: Cuando aparece el botón "Aceptar", se hace clic automáticamente.
3. **BAN**: Una vez en la fase de baneo, se busca al campeón y se banea con precisión.
4. **PICK**: En la fase de selección, se pickea el campeón principal.
5. **SALVAGUARDA**: Si el campeón principal está bloqueado o no se encuentra,
   se usa el salvaguarda automáticamente.
6. **Post-pick**: El sistema espera por posibles dodgeos (hasta 150s), y reinicia si ocurre.

🚨 IMPORTANTE

──────────────

- Es fundamental que tengas **todos los campeones en la carpeta Personajes_pick**, ya que si uno no se encuentra o no se visualiza bien, podría fallar el flujo.
- El sistema depende de que el cliente no sea modificado visualmente (temas o resoluciones muy distintas pueden afectar).
- Se recomienda usar imágenes claras, sin bordes ni transparencia, para garantizar detección óptima.
- Es de suma importancia de que el usuario no haga movimientos con el mouse, ya que si se detecta un movimient ocuando esta ejecutando una fase de "pyautogui" es muy probable que el sistema se rompa y ya no haga nada automaticamente,
- Por eso esta diseñado para gente que no se encuentre en su PC en todo el proceso, desde "Aceptar partida", hasta que inicie.
 
🔧 REQUISITOS (por si quieres clonarlo y mejorarlo)

──────────────

- Python 3.10 o superior
- Bibliotecas necesarias:
   - `opencv-python`
   - `pyautogui`
   - `numpy`
   - `Pillow`
   - `customtkinter`

💬 CRÉDITOS Y ORIGEN
────────────────────
Este proyecto como bien se dijo al inicio, nació a pedido de mononeural  llamado 92 al que lamentablemente tengo que llamar amigo , y como jugador también, sentí que podría beneficiar a muchos. 
¡Si te gusta, puedes contribuir o compartirlo con tus amigos!
"VAN A TEMBLAR"
