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
        self._construir()
    
    def _construir(self) -> None:
        """Construye la vista con contenedores organizados."""
        # Contenedor principal centrado
        self.frame_principal = ttk.Frame(self.contenedor, padding=30)
        self.frame_principal.pack(expand=True)
        
        # --- Contenedor del título ---
        frame_titulo = ttk.Frame(self.frame_principal)
        frame_titulo.pack(pady=(0, 20))
        
        ttk.Label(
            frame_titulo,
            text="🍽️ Restaurante App",
            font=("Arial", 22, "bold")
        ).pack()
        
        ttk.Label(
            frame_titulo,
            text="Sistema de Administración - Semana 14",
            font=("Arial", 11, "italic"),
            foreground="gray"
        ).pack(pady=(5, 0))
        
        # --- Contenedor del formulario ---
        frame_form = ttk.LabelFrame(
            self.frame_principal,
            text="Iniciar Sesión",
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
        ttk.Label(frame_form, text="Contraseña:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_contrasena = ttk.Entry(frame_form, width=30, show="*")
        self.entry_contrasena.grid(row=1, column=1, pady=5, padx=5)
        
        # --- Contenedor de botones ---
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
        
        # --- Contenedor de ayuda ---
        frame_ayuda = ttk.LabelFrame(
            self.frame_principal,
            text="Usuarios de prueba",
            padding=10
        )
        frame_ayuda.pack(fill="x", pady=(15, 0))
        
        ttk.Label(
            frame_ayuda,
            text="ID: admin    |    Contraseña: 1234",
            font=("Consolas", 10)
        ).pack()
        
        # Enter para ingresar
        self.entry_contrasena.bind("<Return>", lambda e: self._ingresar())
        self.entry_usuario.focus_set()
    
    def _ingresar(self) -> None:
        """Valida las credenciales mediante el servicio."""
        identificacion = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        
        if not identificacion or not contrasena:
            messagebox.showwarning(
                "Campos vacíos",
                "Debe ingresar usuario y contraseña."
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