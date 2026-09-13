import tkinter as tk
from tkinter import messagebox
from servicios import RestauranteServicio

class LoginView:
    def __init__(self, contenedor: tk.Frame, servicio: RestauranteServicio, al_ingresar):
        self.contenedor = contenedor
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self.frame = tk.Frame(contenedor)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        self._construir()

    def _construir(self) -> None:
        titulo = tk.Label(self.frame, text="🍽️ Restaurante App", font=("Arial", 20, "bold"))
        titulo.pack(pady=10)

        subtitulo = tk.Label(self.frame, text="Inicio de sesión", font=("Arial", 12))
        subtitulo.pack(pady=5)

        tk.Label(self.frame, text="Usuario:").pack(anchor="w", pady=(15, 0))
        self.entry_usuario = tk.Entry(self.frame, width=30)
        self.entry_usuario.pack(pady=5)

        tk.Label(self.frame, text="Contraseña:").pack(anchor="w", pady=(10, 0))
        self.entry_contrasena = tk.Entry(self.frame, width=30, show="*")
        self.entry_contrasena.pack(pady=5)

        boton = tk.Button(self.frame, text="Ingresar", command=self._ingresar,
                          bg="#4CAF50", fg="white", width=15)
        boton.pack(pady=20)

        tk.Label(self.frame, text="Usuarios de prueba:", font=("Arial", 9, "italic")).pack(pady=(20, 0))
        tk.Label(self.frame, text="ID: admin / Contraseña: 1234", font=("Arial", 9)).pack()

    def _ingresar(self) -> None:
        identificacion = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not identificacion or not contrasena:
            messagebox.showwarning("Campos vacíos", "Debe ingresar usuario y contraseña.")
            return

        usuario = self.servicio.validar_acceso(identificacion, contrasena)
        if usuario is None:
            messagebox.showerror("Acceso denegado", "Credenciales incorrectas.")
            return

        self.al_ingresar(usuario)