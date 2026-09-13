class Usuario:
    def __init__(self, identificacion: str, nombre: str, correo: str, contrasena: str = "1234"):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    def __str__(self) -> str:
        return f"{self.identificacion} - {self.nombre} ({self.correo})"