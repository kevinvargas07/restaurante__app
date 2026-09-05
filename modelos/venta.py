from datetime import datetime
from typing import List, Dict

class Venta:
    def __init__(self, codigo_venta: str, identificacion_usuario: str, items: List[Dict], total: float, fecha: str = None):
        self.codigo_venta = codigo_venta
        self.identificacion_usuario = identificacion_usuario
        self.items = items  # Lista de diccionarios: {"codigo_producto": str, "cantidad": int}
        self.total = total
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"Venta {self.codigo_venta} - Usuario: {self.identificacion_usuario} - Total: ${self.total:.2f} - Fecha: {self.fecha}"