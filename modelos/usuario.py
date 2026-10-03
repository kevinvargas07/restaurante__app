"""Módulo que contiene la clase Usuario."""

from typing import Dict, Any

ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")


class Usuario:
    """Clase que representa un usuario del restaurante."""
    
    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str = "1234",
        rol: str = "Cliente"
    ) -> None:
        self.identificacion = self._validar_identificacion(identificacion)
        self.nombre = self._validar_nombre(nombre)
        self.correo = self._validar_correo(correo)
        self.contrasena = contrasena
        self.rol = self._validar_rol(rol)
    
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
    
    def _validar_rol(self, rol: str) -> str:
        if rol not in ROLES_VALIDOS:
            raise ValueError(
                f"Rol inválido. Debe ser uno de: {', '.join(ROLES_VALIDOS)}"
            )
        return rol
    
    def es_administrador(self) -> bool:
        """Retorna True si el usuario es Administrador."""
        return self.rol == "Administrador"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        return cls(
            identificacion=data.get("identificacion", ""),
            nombre=data.get("nombre", ""),
            correo=data.get("correo", ""),
            contrasena=data.get("contrasena", "1234"),
            rol=data.get("rol", "Cliente")
        )
    
    def __str__(self) -> str:
        return f"{self.identificacion} - {self.nombre} ({self.correo}) [{self.rol}]"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Usuario):
            return False
        return self.identificacion == other.identificacion
    
    def __hash__(self) -> int:
        return hash(self.identificacion)