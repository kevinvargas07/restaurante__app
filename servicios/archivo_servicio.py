import json
from typing import List
from modelos import Producto, Usuario

class ArchivoServicio:
    @staticmethod
    def cargar_productos(ruta: str = "datos/productos.json") -> List[Producto]:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            productos = []
            for item in data:
                productos.append(Producto(
                    codigo=item.get("codigo", ""),
                    nombre=item.get("nombre", ""),
                    categoria=item.get("categoria", "comida"),
                    precio=item.get("precio", 0.0),
                    stock=item.get("stock", 0)
                ))
            return productos
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def cargar_usuarios(ruta: str = "datos/usuarios.json") -> List[Usuario]:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            usuarios = []
            for item in data:
                usuarios.append(Usuario(
                    identificacion=item.get("identificacion", ""),
                    nombre=item.get("nombre", ""),
                    correo=item.get("correo", ""),
                    contrasena=item.get("contrasena", "1234")
                ))
            return usuarios
        except (FileNotFoundError, json.JSONDecodeError):
            return []