import json
from typing import List, Dict, Any
from modelos import Producto, Usuario, Venta

class ArchivoServicio:
    @staticmethod
    def guardar_productos(productos: List[Producto], ruta: str = "datos/productos.json") -> None:
        data = [vars(p) for p in productos]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def cargar_productos(ruta: str = "datos/productos.json") -> List[Producto]:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Producto(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_usuarios(usuarios: List[Usuario], ruta: str = "datos/usuarios.json") -> None:
        data = [vars(u) for u in usuarios]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def cargar_usuarios(ruta: str = "datos/usuarios.json") -> List[Usuario]:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Usuario(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_ventas(ventas: List[Venta], ruta: str = "datos/ventas.json") -> None:
        data = [vars(v) for v in ventas]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def cargar_ventas(ruta: str = "datos/ventas.json") -> List[Venta]:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Venta(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []