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
        self._icon_ref = photo  # evita que el GC lo elimine

        # ——— Ventana principal ———
        self.title("LoL AutoPicker")
        self.geometry("1000x800")   # ▲ Ventana más grande
        self.resizable(True, True)

        # ——— Estado interno ———
        self.stage         = 'pick'   # 'pick', 'ban', 'salv', 'done'
        self.pick          = None
        self.ban           = None
        self.salvaguarda   = None
        self.thread        = None
        self.stop_event    = None

        self.pick_buttons  = {}
        self.ban_buttons   = {}
        self.salv_buttons  = {}

        # ——— Labels de estado ———
        self.pick_label = ctk.CTkLabel(self, text="Pick: Ninguno", font=LABEL_FONT)
        self.pick_label.pack(pady=(20,5))
        self.ban_label  = ctk.CTkLabel(self, text="Ban: Ninguno", font=LABEL_FONT)
        self.ban_label.pack(pady=(0,5))
        self.salv_label = ctk.CTkLabel(self, text="Salvaguarda: Ninguno", font=LABEL_FONT)
        self.salv_label.pack(pady=(0,20))

        # ——— Contenedor de frames ———
        self.container = ctk.CTkFrame(self)
        self.container.pack(padx=20, pady=5, fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # ——— Frames scrollables ———
        self.pick_frame = ctk.CTkScrollableFrame(self.container, width=760, height=400)
        self.pick_frame.grid(row=0, column=0, sticky="nsew")
        self.ban_frame  = ctk.CTkScrollableFrame(self.container, width=760, height=400)
        self.ban_frame.grid(row=0, column=0, sticky="nsew")
        self.salv_frame = ctk.CTkScrollableFrame(self.container, width=760, height=400)
        self.salv_frame.grid(row=0, column=0, sticky="nsew")

        # Arranque: solo pick visible
        self.ban_frame.grid_remove()
        self.salv_frame.grid_remove()

        # ——— Botones de control ———
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=20)
        self.confirm_pick_btn  = ctk.CTkButton(btn_frame, text="Confirmar Pick",
                                               font=BUTTON_FONT,
                                               command=self.confirm_pick,
                                               state="disabled")
        self.confirm_pick_btn.grid(row=0, column=0, padx=5)

        self.back_btn  = ctk.CTkButton(btn_frame, text="Volver",
                                       font=BUTTON_FONT,
                                       command=self.back_to_pick,
                                       state="disabled")
        self.back_btn.grid(row=0, column=1, padx=5)

        self.confirm_ban_btn = ctk.CTkButton(btn_frame, text="Confirmar Ban",
                                             font=BUTTON_FONT,
                                             command=self.confirm_ban,
                                             state="disabled")
        self.confirm_ban_btn.grid(row=0, column=2, padx=5)

        self.confirm_salv_btn = ctk.CTkButton(btn_frame, text="Confirmar Salvaguarda",
                                              font=BUTTON_FONT,
                                              command=self.confirm_salvaguarda,
                                              state="disabled")
        self.confirm_salv_btn.grid(row=0, column=3, padx=5)

        self.start_btn = ctk.CTkButton(btn_frame, text="Iniciar Automatización",
                                       font=BUTTON_FONT,
                                       command=self.on_start,
                                       state="disabled")
        self.start_btn.grid(row=0, column=4, padx=5)

        self.reset_btn = ctk.CTkButton(btn_frame, text="Reiniciar",
                                       font=BUTTON_FONT,
                                       command=self.reset_all)
        self.reset_btn.grid(row=0, column=5, padx=5)

        # ——— Cargo inicialmente los picks ———
        self.load_champions(mode='pick')

    def load_champions(self, mode='pick', exclude=None):
        """
        Carga thumbnails en pick_frame, ban_frame o salv_frame según mode.
        exclude: lista de campeones a omitir.
        """
        exclude = exclude or []
        if mode == 'pick':
            frame, buttons = self.pick_frame, self.pick_buttons
        elif mode == 'ban':
            frame, buttons = self.ban_frame, self.ban_buttons
        else:
            frame, buttons = self.salv_frame, self.salv_buttons
        buttons.clear()

        # Limpia el frame
        for w in frame.winfo_children():
            w.destroy()

        files = sorted(f for f in os.listdir(CAMPEONES_DIR) if f.lower().endswith('.png'))
        cols, idx = 6, 0
        for fn in files:
            champ = fn[:-4].lower()
            if champ in exclude:
                continue
            img = Image.open(os.path.join(CAMPEONES_DIR, fn))
            img.thumbnail(THUMBNAIL_SIZE)
            photo = ImageTk.PhotoImage(img)

            btn = ctk.CTkButton(frame, image=photo, text="",
                                width=100, height=100, corner_radius=8,
                                fg_color="#4A4A4A", hover_color="#6A6A6A",
                                command=lambda c=champ, m=mode: self.on_champ_click(c, m))
            btn.image = photo
            r, c = divmod(idx, cols)
            btn.grid(row=r, column=c, padx=5, pady=5)
            buttons[champ] = btn
            idx += 1

    def on_champ_click(self, champ, mode):
        if mode == 'pick' and self.stage == 'pick':
            self.pick = champ
            self.pick_label.configure(text=f"Pick: {champ}")
            for b in self.pick_buttons.values(): b.configure(border_width=0)
            self.pick_buttons[champ].configure(border_width=2, border_color="green")
            self.confirm_pick_btn.configure(state="normal")

        elif mode == 'ban' and self.stage == 'ban':
            self.ban = champ
            self.ban_label.configure(text=f"Ban: {champ}")
            for b in self.ban_buttons.values(): b.configure(border_width=0)
            self.ban_buttons[champ].configure(border_width=2, border_color="red")
            self.confirm_ban_btn.configure(state="normal")

        elif mode == 'salv' and self.stage == 'salv':
            self.salvaguarda = champ
            self.salv_label.configure(text=f"Salvaguarda: {champ}")
            for b in self.salv_buttons.values(): b.configure(border_width=0)
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

    def confirm_salvaguarda(self):
        """Finaliza selección de salvaguarda y habilita inicio."""
        self.stage = 'done'
        self.confirm_salv_btn.configure(state="disabled")
        self.salv_frame.grid_remove()
        self.start_btn.configure(state="normal")

    def reset_all(self):
        """Cancela el flujo y vuelve a estado inicial de pick."""
        if self.thread and self.thread.is_alive() and self.stop_event:
            self.stop_event.set()

        self.stage = 'pick'
        self.pick = None
        self.ban = None
        self.salvaguarda = None

        self.pick_label.configure(text="Pick: Ninguno")
        self.ban_label.configure(text="Ban: Ninguno")
        self.salv_label.configure(text="Salvaguarda: Ninguno")

        self.confirm_pick_btn.configure(state="disabled")
        self.confirm_ban_btn.configure(state="disabled")
        self.confirm_salv_btn.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        self.back_btn.configure(state="disabled")

        self.salv_frame.grid_remove()
        self.ban_frame.grid_remove()
        self.pick_frame.grid()

        for d in (self.pick_buttons, self.ban_buttons, self.salv_buttons):
            for b in d.values():
                b.configure(border_width=0)

        self.load_champions(mode='pick')

    def on_start(self):
        """Inicia la automatización en un hilo."""
        if not (self.pick and self.ban):
            mbox.showwarning("Faltan datos", "Selecciona pick y ban antes.")
            return

        if self.thread and self.thread.is_alive() and self.stop_event:
            self.stop_event.set()

        self.stop_event = threading.Event()
        self.pick_label.configure(text="Procesando...")
        self.ban_label.configure(text="Procesando...")
        self.salv_label.configure(text="Procesando...")
        # ▲ Indicamos que estamos a la espera de que aparezca "Aceptar"
        self.pick_label.configure(text="Esperando...")
        self.ban_label.configure(text="Esperando...")
        self.salv_label.configure(text="Esperando...")
        self.start_btn.configure(state="disabled")

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
        msg = f"Pick: {self.pick}\nBan: {self.ban}"
        if self.salvaguarda:
            msg += f"\nSalvaguarda: {self.salvaguarda}"

        if success:
            mbox.showinfo(title, msg)
        else:
            mbox.showerror(title, msg or "La automatización falló o fue cancelada.")

        self.reset_all()

if __name__ == "__main__":
    app = LoLAutoPicker()
    app.mainloop()
