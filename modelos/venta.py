"""Módulo que contiene la clase Venta."""

from datetime import datetime
from typing import Dict, Any


class Venta:
    """Clase que representa una venta del restaurante."""
    
    def __init__(
        self,
        codigo: str,
        identificacion_usuario: str,
        codigo_producto: str,
        cantidad: int = 1,
        fecha: str = None
    ) -> None:
        """Inicializa una nueva venta."""
        self.codigo = self._validar_codigo(codigo)
        self.identificacion_usuario = self._validar_usuario(identificacion_usuario)
        self.codigo_producto = self._validar_producto(codigo_producto)
        self.cantidad = self._validar_cantidad(cantidad)
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _validar_codigo(self, codigo: str) -> str:
        if not codigo or not codigo.strip():
            raise ValueError("El código de venta no puede estar vacío")
        return codigo.strip().upper()
    
    def _validar_usuario(self, identificacion: str) -> str:
        if not identificacion or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía")
        return identificacion.strip()
    
    def _validar_producto(self, codigo: str) -> str:
        if not codigo or not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío")
        return codigo.strip().upper()
    
    def _validar_cantidad(self, cantidad: int) -> int:
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            raise ValueError("La cantidad debe ser un número entero")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return cantidad
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la venta a diccionario."""
        return {
            "codigo": self.codigo,
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad,
            "fecha": self.fecha
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Venta":
        """Crea una venta desde un diccionario."""
        return cls(
            codigo=data.get("codigo", ""),
            identificacion_usuario=data.get("identificacion_usuario", ""),
            codigo_producto=data.get("codigo_producto", ""),
            cantidad=data.get("cantidad", 1),
            fecha=data.get("fecha")
        )
    
    def __str__(self) -> str:
        return (
            f"Venta {self.codigo} - Usuario: {self.identificacion_usuario} "
            f"- Producto: {self.codigo_producto} - Cantidad: {self.cantidad} "
            f"- Fecha: {self.fecha}"
        )