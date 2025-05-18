# app.py

import sys
import os
import threading
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as mbox
from aceptar import ejecutar_seleccion

# ——— Helpers para PyInstaller ———
def resource_path(rel_path: str) -> str:
    """
    Devuelve la ruta absoluta correcta, tanto en desarrollo
    como dentro del .exe de PyInstaller.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

# ——— Configuración global de CustomTkinter ———
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ——— Constantes de UI ———
CAMPEONES_DIR   = resource_path('Personajes_pick')
THUMBNAIL_SIZE  = (80, 80)
BUTTON_FONT     = ("Roboto", 12, "bold")
LABEL_FONT      = ("Roboto", 16)

class LoLAutoPicker(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ——— Icono ——— 
        icon_path = resource_path('lol_autopicker.ico')
        img = Image.open(icon_path)
        photo = ImageTk.PhotoImage(img)
        self.iconphoto(True, photo)
        self._icon_ref = photo

        self.title("LoL AutoPicker")
        self.geometry("1200x750")
        self.resizable(True, True)

        # ——— Estado interno ———
        self.stage = 'pick'
        self.pick = None
        self.ban = None
        self.salvaguarda = None
        self.thread = None
        self.stop_event = None
        self.pick_buttons = {}
        self.ban_buttons = {}
        self.salv_buttons = {}
        
        # ——— Estado visual ———
        self.estado_actual = ctk.CTkLabel(self, text="Estado actual: PICK", font=("Roboto", 18, "bold"), text_color="skyblue")
        self.estado_actual.pack(pady=(10, 10))

        self.indicadores_frame = ctk.CTkFrame(self, fg_color="#1E1F29")
        self.indicadores_frame.pack(pady=10)
        self.pick_info = ctk.CTkLabel(self.indicadores_frame, text="✅ Pick: ---", font=("Roboto", 14))
        self.pick_info.grid(row=0, column=0, padx=20)
        self.ban_info = ctk.CTkLabel(self.indicadores_frame, text="⛔ Ban: ---", font=("Roboto", 14))
        self.ban_info.grid(row=0, column=1, padx=20)
        self.salv_info = ctk.CTkLabel(self.indicadores_frame, text="🛟 Salvaguarda: ---", font=("Roboto", 14))
        self.salv_info.grid(row=0, column=2, padx=20)

        # ——— Contenedor y Scroll ———
        self.container = ctk.CTkFrame(self)
        self.container.pack(padx=10, pady=10, fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pick_frame = ctk.CTkScrollableFrame(self.container,  height=450, fg_color="#2A2B38")
        self.pick_frame.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)  

        self.ban_frame = ctk.CTkScrollableFrame(self.container,  height=450, fg_color="#2A2B38")
        self.ban_frame.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)  

        self.salv_frame = ctk.CTkScrollableFrame(self.container,  height=450, fg_color="#2A2B38")
        self.salv_frame.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)  


        self.ban_frame.grid_remove()
        self.salv_frame.grid_remove()

        # ——— Aviso de precaución ———
        self.aviso_label = ctk.CTkLabel(
            self,
            text="⚠️ Es preferible tener todos los campeones.\nSi no se encuentra uno, puede fallar el pick o bugguearse.",
            text_color="orange",
            font=("Roboto", 13, "bold"),
            justify="center",
            wraplength=600
        )
        self.aviso_label.pack(pady=(5, 15))
        # ——— Botones de control ———
        self.btn_frame = ctk.CTkFrame(self, fg_color="#1E1F29")
        self.btn_frame.pack(fill="x", pady=20, padx=20)  
        
        for i in range(6):
            self.btn_frame.grid_columnconfigure(i, weight=1)  


        style_btn = dict(
        font=("Roboto", 14, "bold"),
        corner_radius=10,
        height=45,
        fg_color="#000000",
        text_color="white",
        hover_color="#000000",
)   
        
        
        self.confirm_pick_btn = ctk.CTkButton(
        self.btn_frame, text="✅ Confirmar Pick", command=self.confirm_pick, **style_btn
        )
        self.confirm_pick_btn.grid(row=0, column=0, padx=8, sticky="ew")

        self.back_btn = ctk.CTkButton(
            self.btn_frame, text="🔙 Volver", command=self.back_to_pick, **style_btn
        )
        self.back_btn.grid(row=0, column=1, padx=8, sticky="ew")

        self.confirm_ban_btn = ctk.CTkButton(
            self.btn_frame, text="🚫 Confirmar Ban", command=self.confirm_ban, **style_btn
        )
        self.confirm_ban_btn.grid(row=0, column=2, padx=8, sticky="ew")

        self.confirm_salv_btn = ctk.CTkButton(
            self.btn_frame, text="🛟 Confirmar Salvaguarda", command=self.confirm_salvaguarda, **style_btn
        )
        self.confirm_salv_btn.grid(row=0, column=3, padx=8, sticky="ew")

        self.start_btn = ctk.CTkButton(
            self.btn_frame, text="🤖 Iniciar Automatización", command=self.on_start, **style_btn
        )
        self.start_btn.grid(row=0, column=4, padx=8, sticky="ew")

        self.reset_btn = ctk.CTkButton(
            self.btn_frame, text="♻️ Reiniciar", command=self.reset_all, **style_btn
        )
        self.reset_btn.grid(row=0, column=5, padx=8, sticky="ew")
        # ——— Cargar campeones al iniciar ———
        self.load_champions(mode='pick')  # 🔥 Esto es crucial
        self.bind("<Configure>", self.on_resize)  # 🔁 Ajusta la grilla al cambiar tamaño
        self.imagenes_precargadas = self.precargar_imagenes()


    def precargar_imagenes(self):
        imagenes = {}
        for fn in sorted(os.listdir(CAMPEONES_DIR)):
            if fn.lower().endswith('.png'):
                champ = fn[:-4].lower()
                ruta = os.path.join(CAMPEONES_DIR, fn)
                try:
                    img = Image.open(ruta)
                    img.thumbnail((80, 80))
                    imagenes[champ] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error cargando imagen {fn}: {e}")
        return imagenes

    def on_resize(self, event=None):
        ancho_actual = self.container.winfo_width()
        if ancho_actual < 200:
            return

        campeones_por_fila = max(4, ancho_actual // 130)

        # 🔒 Solo si hay botones ya cargados
        if self.stage in ("pick", "ban", "salv"):
            botones_visibles = {
                'pick': self.pick_buttons,
                'ban': self.ban_buttons,
                'salv': self.salv_buttons
            }.get(self.stage, {})

            if botones_visibles:
                self.redibujar_campeones(campeones_por_fila)

    def redibujar_campeones(self, columnas=6):
        """Redibuja los campeones en el frame actual según la cantidad de columnas."""
        modo = self.stage if self.stage in ('pick', 'ban', 'salv') else 'pick'
        frame = {
            'pick': self.pick_frame,
            'ban': self.ban_frame,
            'salv': self.salv_frame
        }[modo]

        botones = {
            'pick': self.pick_buttons,
            'ban': self.ban_buttons,
            'salv': self.salv_buttons
        }[modo]

        for idx, (champ, btn) in enumerate(botones.items()):
            fila, col = divmod(idx, columnas)
            btn.grid(row=fila, column=col, padx=5, pady=5)

    def load_champions(self, mode='pick', exclude=None):
        exclude = exclude or []

        if mode == 'pick':
            frame = self.pick_frame
            buttons = self.pick_buttons
        elif mode == 'ban':
            frame = self.ban_frame
            buttons = self.ban_buttons
        else:
            frame = self.salv_frame
            buttons = self.salv_buttons

        buttons.clear()

        for w in frame.winfo_children():
            w.destroy()

        frame.update_idletasks()
        ancho_frame = frame.winfo_width()

        # 🔁 Si aún no tiene tamaño real, vuelve a intentar luego
        if ancho_frame <= 1:
            self.after(50, lambda: self.load_champions(mode, exclude))
            return

        button_size = 100
        spacing = 10
        cols = max(1, ancho_frame // (button_size + spacing))

        # 🔥 LIMPIA configuración previa
        for col in range(50):  # asumimos máximo 50 columnas posibles
            frame.grid_columnconfigure(col, weight=0)

        files = sorted(f for f in os.listdir(CAMPEONES_DIR) if f.lower().endswith('.png'))
        idx = 0

        for fn in files:
            champ = fn[:-4].lower()
            if champ in exclude:
                continue

            img_ctk = self.imagenes_precargadas.get(champ)
            if not img_ctk:
                continue

            champ_container = ctk.CTkFrame(frame, fg_color="transparent")  # 🔲 contenedor total

            btn = ctk.CTkButton(
                champ_container,
                image=img_ctk,
                text="",  # sin texto dentro del botón
                width=80,
                height=80,
                corner_radius=10,
                fg_color="#3A3B4B",
                hover_color="#555",
                command=lambda c=champ, m=mode: self.on_champ_click(c, m),
            )
            btn.image = img_ctk
            btn.pack(padx=2, pady=(5, 2))

            name_label = ctk.CTkLabel(
                champ_container,
                text=champ.capitalize(),
                font=("Roboto", 11, "bold"),
                text_color="white"
            )
            name_label.pack(pady=(0, 5))

            r, c = divmod(idx, cols)
            champ_container.grid(row=r, column=c, padx=5, pady=5)
            buttons[champ] = champ_container
            idx += 1

        for col in range(cols):
            frame.grid_columnconfigure(col, weight=1)


        

    def update_estado_ui(self, estado=None):
        self.estado_actual.configure(text=f"Estado actual: {estado or self.stage.upper()}")
        self.pick_info.configure(text=f"✅ Pick: {self.pick or '---'}")
        self.ban_info.configure(text=f"⛔ Ban: {self.ban or '---'}")
        self.salv_info.configure(text=f"🛟 Salvaguarda: {self.salvaguarda or '---'}")

    def on_champ_click(self, champ, mode):
        if mode == 'pick' and self.stage == 'pick':
            self.pick = champ
            self.pick_info.configure(text=f"✅ Pick: {champ}")
            for b in self.pick_buttons.values():
                b.configure(border_width=0)
            self.pick_buttons[champ].configure(border_width=2, border_color="green")
            self.confirm_pick_btn.configure(state="normal")

        elif mode == 'ban' and self.stage == 'ban':
            self.ban = champ
            self.ban_info.configure(text=f"⛔ Ban: {champ}")
            for b in self.ban_buttons.values():
                b.configure(border_width=0)
            self.ban_buttons[champ].configure(border_width=2, border_color="red")
            self.confirm_ban_btn.configure(state="normal")

        elif mode == 'salv' and self.stage == 'salv':
            self.salvaguarda = champ
            self.salv_info.configure(text=f"🛟 Salvaguarda: {champ}")
            for b in self.salv_buttons.values():
                b.configure(border_width=0)
            self.salv_buttons[champ].configure(border_width=2, border_color="yellow")
            self.confirm_salv_btn.configure(state="normal")


    def confirm_pick(self):
        """Pasa a ban y recarga excluyendo el pick."""
        self.stage = 'ban'
        self.confirm_pick_btn.configure(state="disabled")
        self.back_btn.configure(state="normal")
        self.load_champions(mode='ban', exclude=[self.pick])
        self.pick_frame.grid_remove()
        self.ban_frame.grid()
        self.update_estado_ui()

    def back_to_pick(self):
        """Vuelve a pick, reset total."""
        self.stage = 'pick'
        self.ban = None
        self.salvaguarda = None
        self.ban_label.configure(text="Ban: Ninguno")
        self.salv_label.configure(text="Salvaguarda: Ninguno")
        self.confirm_ban_btn.configure(state="disabled")
        self.back_btn.configure(state="disabled")
        self.confirm_salv_btn.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        self.ban_frame.grid_remove()
        self.salv_frame.grid_remove()
        self.pick_frame.grid()
        for b in self.pick_buttons.values():
            b.configure(border_width=0)

    def confirm_ban(self):
        """Pasa a salvaguarda tras ban."""
        self.stage = 'salv'
        self.confirm_ban_btn.configure(state="disabled")
        self.back_btn.configure(state="disabled")
        self.load_champions(mode='salv', exclude=[self.pick, self.ban])
        self.ban_frame.grid_remove()
        self.salv_frame.grid()
        self.update_estado_ui()

    def confirm_salvaguarda(self):
        """Finaliza selección de salvaguarda y habilita inicio."""
        self.stage = 'done'
        self.confirm_salv_btn.configure(state="disabled")
        self.salv_frame.grid_remove()
        self.start_btn.configure(state="normal")
        self.update_estado_ui()

    def reset_all(self):
        """Cancela el flujo y vuelve a estado inicial de pick."""

        # 🛑 Señal de parada al hilo si está activo
        if self.thread and self.thread.is_alive():
            if self.stop_event:
                print("⛔ Señalando al hilo que se detenga...")
                self.stop_event.set()
                self.thread.join(timeout=5)  

        # 🔄 Reinicio de variables de estado
        self.stage = 'pick'
        self.pick = None
        self.ban = None
        self.salvaguarda = None
        self.stop_event = None
        self.thread = None
        
        # 🔄 UI: limpiar labels
        self.estado_actual.configure(text="Estado actual: PICK")
        self.pick_info.configure(text="✅ Pick: ---")
        self.ban_info.configure(text="⛔ Ban: ---")
        self.salv_info.configure(text="🛟 Salvaguarda: ---")
        self.update_estado_ui()

        # 🔄 UI: desactivar botones
        self.confirm_pick_btn.configure(state="disabled")
        self.confirm_ban_btn.configure(state="disabled")
        self.confirm_salv_btn.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        self.back_btn.configure(state="disabled")

        # 🔄 UI: mostrar solo el frame de pick
        self.salv_frame.grid_remove()
        self.ban_frame.grid_remove()
        self.pick_frame.grid()

        # 🔄 UI: limpiar bordes
        for d in (self.pick_buttons, self.ban_buttons, self.salv_buttons):
            for b in d.values():
                b.configure(border_width=0)

        # 🔄 Volver a cargar imágenes
        self.load_champions(mode='pick')

    def on_start(self):
        self.estado_actual.configure(text="Estado actual: EN EJECUCIÓN")

        """Inicia la automatización en hilo."""
        if not (self.pick and self.ban):
            mbox.showwarning("Faltan datos", "Selecciona pick y ban antes.")
            return

        # Detiene hilo anterior si había
        if self.thread and self.thread.is_alive() and self.stop_event:
            self.stop_event.set()
            self.thread.join(timeout=5)

        # Nueva señal de control
        self.stop_event = threading.Event()
        self.estado_actual.configure(text="Estado actual: ESPERANDO")

        self.start_btn.configure(state="disabled")

        # Nuevo hilo
        self.thread = threading.Thread(target=self.run_selection, daemon=True)
        self.thread.start()
        
    def run_selection(self):
        success = ejecutar_seleccion(
            self.pick,
            self.ban,
            campeon_salvaguarda=self.salvaguarda,
            stop_event=self.stop_event
        )
        self.after(0, lambda: self.on_finish_selection(success))

    def on_finish_selection(self, success):
        title = "Éxito" if success else "Cancelado/Error"
        msg = (
            f"Pick: {self.pick}\nBan: {self.ban}\n"
            + (f"Salvaguarda: {self.salvaguarda}" if self.salvaguarda else "")
        )

        if success:
            print("✅ Finalización automática exitosa. Reiniciando para próxima partida...")
            self.reset_all()  
        else:
            mbox.showerror(title, msg or "La automatización fue cancelada o falló.")
            self.reset_all()

if __name__ == "__main__":
    app = LoLAutoPicker()
    app.mainloop()
