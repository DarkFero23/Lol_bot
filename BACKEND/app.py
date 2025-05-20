import sys
import os
import threading
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as mbox
from aceptar import ejecutar_seleccion
import json

# ——— Helpers para PyInstaller ———
def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

# ——— Configuración global de CustomTkinter ———
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CAMPEONES_DIR = resource_path("Personajes_pick")
ICON_PATH    = resource_path("lol_autopicker.ico")
# Directorio del script principal
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SCRIPT_DIR, 'last_selection.json')

class LoLAutoPicker(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        # Ventana
        self.title("LoL AutoPicker")
        self.geometry("1920x1080")
        icon = Image.open(ICON_PATH)
        self.iconphoto(True, ImageTk.PhotoImage(icon))

        # Estado interno
        self.lanes = ["TOP", "MID", "JG", "ADC", "SUPP"]
        self.picks = {lane: None for lane in self.lanes}
        self.salvaguardas = {lane: None for lane in self.lanes}
        self.ban = None
        self.temp_selection = {lane: None for lane in self.lanes + ["BAN"]}
        self.champ_buttons = {}  # {lane: {champ: button}}
        self.ban_buttons = {}
        self.champ_frames = {}             # { 'TOP': champ_frame, …, 'BAN': ban_scroll }
        self.pick_confirm_buttons = {}     # { 'TOP': pick_btn, … }
        self.salv_confirm_buttons = {}     # { 'TOP': salv_btn, … }
        self.ban_confirm_btn = None
        # ——— Inicializar diccionarios de botones de confirmación ———
        self.pick_confirm_buttons  = {}  # guardaremos acá pick_btn por lane
        self.salv_confirm_buttons  = {}  # guardaremos acá salv_btn por lane
        self.ban_confirm_btn       = None
        # Precarga imágenes
        self.imagenes = self._precargar_imagenes()

        # Estado visual
        self.status_label = ctk.CTkLabel(self, text="Estado: Esperando selecciones", font=("Roboto", 18, "bold"))
        self.status_label.pack(pady=10)

        # ——— Search bar + warning ———
        self.search_var = ctk.StringVar()
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(search_frame, text="🔍 Buscar campeón:", font=("Roboto", 14)).grid(row=0, column=0, sticky="w")
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Escribe el nombre...",
            width=200
        )
        search_entry.grid(row=0, column=1, padx=5, sticky="w")
        warning_lbl = ctk.CTkLabel(
            search_frame,
            text="⚠️ Es preferible tener todos los campeones\nen Personajes, de lo contrario puede fallar",
            text_color="orange",
            font=("Roboto", 12),
            wraplength=400,
            justify="left"
        )
        warning_lbl.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="w")
        # Cada vez que cambie el texto, aplicamos el filtro
        self.search_var.trace_add("write", lambda *args: self._on_search())
        # Crear pestañas y controles
        self._create_tabs()
        self._create_controls()
        # … después de build UI …
        self.after(2000, self._load_last_selection)

        # y luego actualiza visualmente cualquier pick/ban que haya cargado
        for lane in self.lanes:
            if self.picks[lane]:
                getattr(self, f"{lane.lower()}_pick_lbl").configure(
                    text=f"Pick: {self.picks[lane].capitalize()}"
                )
            if self.salvaguardas[lane]:
                getattr(self, f"{lane.lower()}_salv_lbl").configure(
                    text=f"Salv: {self.salvaguardas[lane].capitalize()}"
                )
        if self.ban:
            self.ban_lbl.configure(text=f"Ban: {self.ban.capitalize()}")
        
    def _load_last_selection(self):
        """Lee last_selection.json y pinta la UI con lo guardado."""
        if not os.path.exists(CACHE_FILE):
            return
        try:
            with open(CACHE_FILE, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print("⚠️ error leyendo cache:", e)
            return

        # Para cada carril, si existe en champ_buttons → marca pick y salv
        for lane in self.lanes:
            p = data.get('picks', {}).get(lane)
            if p and p in self.champ_buttons[lane]:
                self.picks[lane] = p
                self._mark_pick_ui(lane, p)
            s = data.get('salvaguardas', {}).get(lane)
            if s and s in self.champ_buttons[lane]:
                self.salvaguardas[lane] = s
                self._mark_salv_ui(lane, s)

        # Ban
        b = data.get('ban')
        if b and b in self.ban_buttons:
            self.ban = b
            self._mark_ban_ui(b)
        # Esto asegura que el frontend tenga todo para enviar luego
        self.picks = data.get('picks', {})
        self.salvaguardas = data.get('salvaguardas', {})
        self.ban = data.get('ban', None)
        print("✅ Cache cargado:", data)

    def _mark_pick_ui(self, lane, champ):
        lbl = getattr(self, f"{lane.lower()}_pick_lbl")
        lbl.configure(text=f"Pick: {champ.capitalize()}")
        btn = self.champ_buttons[lane][champ]
        btn.configure(border_width=2, border_color='green')
        self.pick_confirm_buttons[lane].configure(state='disabled')

    def _mark_salv_ui(self, lane, champ):
        lbl = getattr(self, f"{lane.lower()}_salv_lbl")
        lbl.configure(text=f"Salv: {champ.capitalize()}")
        btn = self.champ_buttons[lane][champ]
        btn.configure(border_width=2, border_color='yellow')
        self.salv_confirm_buttons[lane].configure(state='disabled')

    def _mark_ban_ui(self, champ):
        self.ban_lbl.configure(text=f"Ban: {champ.capitalize()}")
        btn = self.ban_buttons[champ]
        btn.configure(border_width=2, border_color='red')
        self.ban_confirm_btn.configure(state='disabled')

    def _save_last_selection(self):
        data = {
            'picks'       : self.picks,
            'salvaguardas': self.salvaguardas,
            'ban'         : self.ban
        }
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("⚠️ no pude guardar cache:", e)
    def _precargar_imagenes(self):
        imgs = {}
        for fn in sorted(os.listdir(CAMPEONES_DIR)):
            if fn.lower().endswith('.png'):
                key = fn[:-4].lower()
                try:
                    img = Image.open(os.path.join(CAMPEONES_DIR, fn))
                    img.thumbnail((80, 80))
                    imgs[key] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error cargando {fn}: {e}")
        return imgs

    def _create_tabs(self):
        # ——— Si ya había un tabview, lo destruyo para evitar duplicados ———
        if hasattr(self, "tabview"):
            self.tabview.destroy()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)

        for lane in self.lanes:
            self.tabview.add(lane)
            frame = self.tabview.tab(lane)

            # Scrollable frame de campeones
            champ_frame = ctk.CTkScrollableFrame(frame, fg_color="#2A2B38")
            champ_frame.pack(fill="both", expand=True, padx=10, pady=10)
            self.champ_frames[lane] = champ_frame
            self.champ_buttons[lane] = {}
            # Carga inicial sin filtro
            self._load_champions(champ_frame, lane, filter_text=self.search_var.get().lower())

            # Botones de confirmación y guardado de referencias
            confirm_frame = ctk.CTkFrame(frame, fg_color="transparent")
            confirm_frame.pack(fill="x", padx=10, pady=(0,10))
            pick_btn = ctk.CTkButton(
                confirm_frame,
                text=f"✅ Confirmar Pick {lane}",
                command=lambda l=lane: self._confirm_pick(l),
                font=("Roboto",14,"bold"), corner_radius=8, height=40
            )
            pick_btn.grid(row=0, column=0, padx=5, sticky="ew")
            salv_btn = ctk.CTkButton(
                confirm_frame,
                text=f"🛟 Confirmar Salv {lane}",
                command=lambda l=lane: self._confirm_salv(l),
                font=("Roboto",14,"bold"), corner_radius=8, height=40
            )
            salv_btn.grid(row=0, column=1, padx=5, sticky="ew")
            confirm_frame.grid_columnconfigure(0, weight=1)
            confirm_frame.grid_columnconfigure(1, weight=1)
            self.pick_confirm_buttons[lane] = pick_btn
            self.salv_confirm_buttons[lane] = salv_btn

            # … etiquetas de Pick/Salv …
            info_frame = ctk.CTkFrame(frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=10)
            pick_lbl = ctk.CTkLabel(info_frame, text="Pick: ---", font=("Roboto",14))
            pick_lbl.grid(row=0, column=0, padx=10)
            salv_lbl = ctk.CTkLabel(info_frame, text="Salv: ---", font=("Roboto",14))
            salv_lbl.grid(row=0, column=1, padx=10)
            info_frame.grid_columnconfigure(0, weight=1)
            info_frame.grid_columnconfigure(1, weight=1)
            setattr(self, f"{lane.lower()}_pick_lbl", pick_lbl)
            setattr(self, f"{lane.lower()}_salv_lbl", salv_lbl)

        # Pestaña BAN (igual, guardando champ_frame y ban_confirm_btn)
        self.tabview.add("BAN")
        ban_frame = self.tabview.tab("BAN")
        ban_scroll = ctk.CTkScrollableFrame(ban_frame, fg_color="#2A2B38")
        ban_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.champ_frames["BAN"] = ban_scroll
        self._load_champions(ban_scroll, "BAN", filter_text=self.search_var.get().lower())

        ban_confirm = ctk.CTkButton(
            ban_frame,
            text="🚫 Confirmar Ban",
            command=self._confirm_ban,
            font=("Roboto",14,"bold"), corner_radius=8, height=40
        )
        ban_confirm.pack(pady=(0,10), padx=10, fill="x")
        self.ban_confirm_btn = ban_confirm
        self.ban_lbl = ctk.CTkLabel(ban_frame, text="Ban: ---", font=("Roboto",14))
        self.ban_lbl.pack(pady=(0,10))

    def _load_champions(self, container, lane, filter_text=""):
        container.update_idletasks()
        if container.winfo_width() <= 1:
            self.after(50, lambda: self._load_champions(container, lane, filter_text))
            return

        # Limpio todo
        for w in container.winfo_children():
            w.destroy()

        files = sorted(f for f in os.listdir(CAMPEONES_DIR) if f.lower().endswith('.png'))
        cols = max(4, container.winfo_width() // 120)
        idx = 0

        for fn in files:
            champ = fn[:-4].lower()
            # Filtrado por texto
            if filter_text and filter_text not in champ:
                continue
            img = self.imagenes.get(champ)
            if not img:
                continue

            box = ctk.CTkFrame(container, fg_color='transparent')
            r, c = divmod(idx, cols)
            box.grid(row=r, column=c, padx=5, pady=5)
            btn = ctk.CTkButton(
                box, image=img, text='', width=80, height=80,
                corner_radius=10, fg_color='#3A3B4B', hover_color='#555',
                command=lambda c=champ, l=lane: self._on_champ_click(c, l)
            )
            btn.pack()
            ctk.CTkLabel(box, text=champ.capitalize(), font=('Roboto',11,'bold'), text_color='white').pack()
            # guardar referencia
            if lane == 'BAN':
                self.ban_buttons[champ] = btn
            else:
                self.champ_buttons[lane][champ] = btn

            idx += 1

        for i in range(cols):
            container.grid_columnconfigure(i, weight=1)

    def _on_champ_click(self, champ, lane):
        # marca la selección temporal
        self.temp_selection[lane] = champ

        # limpieza de bordes en esa pestaña
        target = self.ban_buttons if lane == 'BAN' else self.champ_buttons[lane]
        for b in target.values():
            b.configure(border_width=0)

        # borde cyan al seleccionado
        target[champ].configure(border_width=2, border_color='cyan')

        # habilita el confirm de pick/salv o ban
        if lane == 'BAN':
            self.ban_confirm_btn.configure(state='normal')
        else:
            self.pick_confirm_buttons[lane].configure(state='normal')
            self.salv_confirm_buttons[lane].configure(state='normal')

    def _confirm_pick(self, lane):
        champ = self.temp_selection[lane]
        if not champ:
            mbox.showwarning('Error', f'Selecciona un campeón en {lane}')
            return
        # guarda pick
        self.picks[lane] = champ
        # actualiza etiqueta
        lbl = getattr(self, f'{lane.lower()}_pick_lbl')
        lbl.configure(text=f'Pick: {champ.capitalize()}')
        # actualiza borde a verde
        btn = self.champ_buttons[lane][champ]
        btn.configure(border_width=2, border_color='green')
        # deshabilita este confirm
        self.pick_confirm_buttons[lane].configure(state='disabled')

        # limpia la selección temporal
        self.temp_selection[lane] = None
        self._save_last_selection()   # <— guarda cache aquí
        

    def _confirm_salv(self, lane):
        champ = self.temp_selection[lane]
        if not champ:
            mbox.showwarning('Error', f'Selecciona un campeón en {lane}')
            return
        self.salvaguardas[lane] = champ
        lbl = getattr(self, f'{lane.lower()}_salv_lbl')
        lbl.configure(text=f'Salv: {champ.capitalize()}')
        btn = self.champ_buttons[lane][champ]
        btn.configure(border_width=2, border_color='yellow')
        self.salv_confirm_buttons[lane].configure(state='disabled')

        self.temp_selection[lane] = None
        self._save_last_selection()   # <— guarda cache aquí

    def _confirm_ban(self):
        champ = self.temp_selection['BAN']
        if not champ:
            mbox.showwarning('Error', 'Selecciona un campeón para ban')
            return
        self.ban = champ
        self.ban_lbl.configure(text=f'Ban: {champ.capitalize()}')
        btn = self.ban_buttons[champ]
        btn.configure(border_width=2, border_color='red')
        self.ban_confirm_btn.configure(state='disabled')
        self.temp_selection['BAN'] = None
        self._save_last_selection()   # <— guarda cache aquí

    def _create_controls(self):
        ctrl = ctk.CTkFrame(self, fg_color='#1E1F29')
        ctrl.pack(fill='x', pady=5, padx=10)
        self.start_btn = ctk.CTkButton(ctrl, text='🤖 Iniciar', command=self._on_start, font=('Roboto',14,'bold'))
        self.start_btn.grid(row=0, column=0, padx=5, sticky='ew')
        self.reset_btn = ctk.CTkButton(ctrl, text='♻️ Reiniciar', command=self._on_reset, font=('Roboto',14,'bold'))
        self.reset_btn.grid(row=0, column=1, padx=5, sticky='ew')
        ctrl.grid_columnconfigure(0, weight=1)
        ctrl.grid_columnconfigure(1, weight=1)

    def _on_start(self):
        self.status_label.configure(text='Estado: Ejecutando')
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run_selection, daemon=True)
        self.thread.start()
 

    def _run_selection(self):
        # 1) Leer desde el archivo JSON
        cache_file = "last_selection.json"
        if not os.path.exists(cache_file):
            self.after(0, lambda: mbox.showerror("Error", "No se encontró configuración guardada."))
            return

        try:
            with open(cache_file, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print("❌ Error leyendo archivo cache:", e)
            self.after(0, lambda: mbox.showerror("Error", "No se pudo leer el archivo de configuración."))
            return

        # 2) Extraer picks, salvaguardas y ban
        picks = data.get("picks", {})
        salvaguardas = data.get("salvaguardas", {})
        ban = data.get("ban", None)

        if not picks or not salvaguardas or not ban:
            self.after(0, lambda: mbox.showerror("Error", "Falta información en el archivo de selección guardado."))
            return

        # 3) Mostrar en consola
        print("🔗 [GUI] Llamando a ejecutar_seleccion con:")
        print("    picks:       ", picks)
        print("    salvaguardas:", salvaguardas)
        print("    ban:         ", ban)
        
        print("JSON crudo leído:")
        print(json.dumps(data, indent=2))
        # 4) Ejecutar backend (que detecta la línea y decide qué pickear)
        success = ejecutar_seleccion(
            picks=picks,
            campeon_ban=ban,
            salvaguardas=salvaguardas,
            stop_event=self.stop_event
        )

        # 5) Mostrar resultado
        self.after(0, lambda: self._finish(success))
    def _finish(self, success):
            if success: mbox.showinfo('Éxito', 'Automatización completada')
            else: mbox.showerror('Error', 'Falló o fue cancelado')
            self._on_reset()

    def _on_reset(self):
        """
        Reinicia todas las selecciones y reconstruye las pestañas sin duplicar la UI.
        """
        # Limpia estado interno
        for lane in self.lanes:
            self.picks[lane] = None
            self.salvaguardas[lane] = None
            self.temp_selection[lane] = None
        self.ban = None
        self.temp_selection['BAN'] = None

        # Destruye viejas pestañas y botones de ban
        self.tabview.destroy()
        # Reconstruye pestañas con botones completos
        self._create_tabs()
        # Restaurar estado visual
        self.status_label.configure(text='Estado: Esperando selecciones')

        # Asegura que el botón de ban esté activo
        try:
            self.ban_confirm_btn.configure(state='normal')
        except AttributeError:
            pass

        # Opcional: restablecer botones de inicio/reiniciar si cambian estado
        try:
            self.start_btn.configure(state='normal')
        except AttributeError:
            pass
    def _on_search(self):
        """
        Se dispara cada vez que cambia el contenido de search_var.
        Recarga la grilla del tab activo con el filtro actual.
        """
        texto = self.search_var.get().lower().strip()
        tab = self.tabview.get()  # devuelve el nombre de la pestaña activa
        frame = self.champ_frames.get(tab)
        if frame:
            self._load_champions(frame, tab, filter_text=texto)
if __name__ == "__main__":
    app = LoLAutoPicker()
    app.mainloop()