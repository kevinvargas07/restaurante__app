"""Módulo que contiene la clase Usuario."""

from typing import Dict, Any


class Usuario:
    """Clase que representa un usuario del restaurante."""
    
    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str = "1234"
    ) -> None:
        self.identificacion = self._validar_identificacion(identificacion)
        self.nombre = self._validar_nombre(nombre)
        self.correo = self._validar_correo(correo)
        self.contrasena = contrasena
    
    def _validar_identificacion(self, identificacion: str) -> str:
        if not identificacion or not identificacion.strip():
            raise ValueError("La identificación no puede estar vacía")
        return identificacion.strip()
    
    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        return nombre.strip()
    
    def _validar_correo(self, correo: str) -> str:
        correo = correo.strip()
        if not correo or "@" not in correo:
            raise ValueError("El correo no tiene un formato válido")
        return correo
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el usuario a diccionario."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        """Crea un usuario desde un diccionario."""
        return cls(
            identificacion=data.get("identificacion", ""),
            nombre=data.get("nombre", ""),
            correo=data.get("correo", ""),
            contrasena=data.get("contrasena", "1234")
        )
    
    def __str__(self) -> str:
        return f"{self.identificacion} - {self.nombre} ({self.correo})"