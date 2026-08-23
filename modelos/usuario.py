"""Módulo que contiene la clase Usuario."""

from typing import Optional


class Usuario:
    """Clase que representa un usuario del restaurante."""
    
    def __init__(
        self,
        nombre: str,
        email: str,
        telefono: Optional[str] = None
    ) -> None:
        """
        Inicializa un nuevo usuario.
        
        Args:
            nombre: Nombre del usuario
            email: Email del usuario
            telefono: Teléfono opcional del usuario
            
        Raises:
            ValueError: Si los valores no son válidos
        """
        self.nombre = self._validar_nombre(nombre)
        self.email = self._validar_email(email)
        self.telefono = telefono
    
    def _validar_nombre(self, nombre: str) -> str:
        """Valida que el nombre no esté vacío."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío")
        return nombre.strip()
    
    def _validar_email(self, email: str) -> str:
        """Valida que el email tenga formato básico."""
        email = email.strip()
        if not email:
            raise ValueError("El email no puede estar vacío")
        if "@" not in email or "." not in email:
            raise ValueError("El email no tiene un formato válido")
        return email
    
    def __str__(self) -> str:
        """Representación en string del usuario."""
        telefono_str = f" - Tel: {self.telefono}" if self.telefono else ""
        return f"{self.nombre} ({self.email}){telefono_str}"