"""Vista de inicio de sesión."""

import tkinter as tk
from tkinter import messagebox, ttk
from servicios import RestauranteServicio


class LoginView:
    """Vista de login usando componentes y contenedores."""
    
    def __init__(
        self,
        contenedor: tk.Frame,
        servicio: RestauranteServicio,
        al_ingresar
    ) -> None:
        self.contenedor = contenedor
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self._logo_img = None
        self._construir()
    
    def _construir(self) -> None:
        """Construye la vista con contenedores organizados."""
        self.frame_principal = ttk.Frame(self.contenedor, padding=30)
        self.frame_principal.pack(expand=True)
        
        # --- Logo ---
        self._cargar_logo()
        
        # --- Título ---
        frame_titulo = ttk.Frame(self.frame_principal)
        frame_titulo.pack(pady=(0, 20))
        
        ttk.Label(
            frame_titulo,
            text="Restaurante App",
            font=("Arial", 22, "bold")
        ).pack()
        
        ttk.Label(
            frame_titulo,
            text="Sistema de Administracion - Semana 15",
            font=("Arial", 11, "italic"),
            foreground="gray"
        ).pack(pady=(5, 0))
        
        # --- Formulario ---
        frame_form = ttk.LabelFrame(
            self.frame_principal,
            text="Iniciar Sesion",
            padding=20
        )
        frame_form.pack(fill="x", pady=10)
        
        # Campo: Usuario
        ttk.Label(frame_form, text="Usuario:").grid(
            row=0, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_usuario = ttk.Entry(frame_form, width=30)
        self.entry_usuario.grid(row=0, column=1, pady=5, padx=5)
        
        # Campo: Contraseña
        ttk.Label(frame_form, text="Contrasena:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_contrasena = ttk.Entry(frame_form, width=30, show="*")
        self.entry_contrasena.grid(row=1, column=1, pady=5, padx=5)
        
        # --- Botones ---
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.pack(pady=15)
        
        ttk.Button(
            frame_botones,
            text="Ingresar",
            command=self._ingresar,
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            frame_botones,
            text="Salir",
            command=self.contenedor.winfo_toplevel().destroy,
            width=15
        ).pack(side="left", padx=5)
        
        # --- Ayuda ---
        frame_ayuda = ttk.LabelFrame(
            self.frame_principal,
            text="Usuarios de prueba",
            padding=10
        )
        frame_ayuda.pack(fill="x", pady=(15, 0))
        
        ttk.Label(
            frame_ayuda,
            text="ID: admin    |    Contrasena: 1234",
            font=("Consolas", 10)
        ).pack()
        
        # Enter para ingresar
        self.entry_contrasena.bind("<Return>", lambda e: self._ingresar())
        self.entry_usuario.focus_set()
    
    def _cargar_logo(self) -> None:
        """Intenta cargar el logo desde assets/, si no usa emoji."""
        try:
            from PIL import Image, ImageTk
            imagen = Image.open("assets/logo.png")
            imagen = imagen.resize((80, 80), Image.LANCZOS)
            self._logo_img = ImageTk.PhotoImage(imagen)
            ttk.Label(
                self.frame_principal,
                image=self._logo_img
            ).pack(pady=(0, 10))
        except Exception:
            # Fallback si no hay PIL o no existe el logo
            ttk.Label(
                self.frame_principal,
                text="🍽️",
                font=("Arial", 40)
            ).pack(pady=(0, 10))
    
    def _ingresar(self) -> None:
        """Valida las credenciales mediante el servicio."""
        identificacion = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        
        if not identificacion or not contrasena:
            messagebox.showwarning(
                "Campos vacios",
                "Debe ingresar usuario y contrasena."
            )
            return
        
        usuario = self.servicio.validar_acceso(identificacion, contrasena)
        if usuario is None:
            messagebox.showerror(
                "Acceso denegado",
                "Credenciales incorrectas.\nIntente nuevamente."
            )
            self.entry_contrasena.delete(0, "end")
            return
        
        self.al_ingresar(usuario)