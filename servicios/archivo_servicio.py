"""Módulo que maneja la persistencia de datos en archivos JSON."""

import json
import os
from typing import List
from modelos import Producto, Usuario, Venta


class ArchivoServicio:
    """Servicio encargado de leer y escribir datos en archivos JSON."""
    
    RUTA_PRODUCTOS: str = "datos/productos.json"
    RUTA_USUARIOS: str = "datos/usuarios.json"
    RUTA_VENTAS: str = "datos/ventas.json"
    
    def __init__(self) -> None:
        os.makedirs("datos", exist_ok=True)
    
    # ---------- PRODUCTOS ----------
    def cargar_productos(self) -> List[Producto]:
        return self._cargar_lista(self.RUTA_PRODUCTOS, Producto)
    
    def guardar_productos(self, productos: List[Producto]) -> bool:
        return self._guardar_lista(self.RUTA_PRODUCTOS, productos)
    
    # ---------- USUARIOS ----------
    def cargar_usuarios(self) -> List[Usuario]:
        return self._cargar_lista(self.RUTA_USUARIOS, Usuario)
    
    def guardar_usuarios(self, usuarios: List[Usuario]) -> bool:
        return self._guardar_lista(self.RUTA_USUARIOS, usuarios)
    
    # ---------- VENTAS ----------
    def cargar_ventas(self) -> List[Venta]:
        return self._cargar_lista(self.RUTA_VENTAS, Venta)
    
    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        return self._guardar_lista(self.RUTA_VENTAS, ventas)
    
    # ---------- MÉTODOS PRIVADOS ----------
    def _cargar_lista(self, ruta: str, clase) -> list:
        if not os.path.exists(ruta):
            return []
        
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                if not contenido.strip():
                    return []
                datos = json.loads(contenido)
            
            if not isinstance(datos, list):
                print(f"⚠ {ruta} no contiene una lista válida")
                return []
            
            objetos = []
            for i, item in enumerate(datos):
                try:
                    if not isinstance(item, dict):
                        continue
                    objetos.append(clase.from_dict(item))
                except (KeyError, ValueError, TypeError) as error:
                    print(f"⚠ Error en elemento {i} de {ruta}: {error}")
                    continue
            
            return objetos
            
        except json.JSONDecodeError as error:
            print(f"⚠ {ruta} no contiene JSON válido: {error}")
            return []
        except PermissionError as error:
            print(f"⚠ Error de permisos al leer {ruta}: {error}")
            return []
        except OSError as error:
            print(f"⚠ Error al leer {ruta}: {error}")
            return []
    
    def _guardar_lista(self, ruta: str, objetos: list) -> bool:
        try:
            datos = [obj.to_dict() for obj in objetos]
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
        except PermissionError as error:
            print(f"⚠ Error de permisos al escribir {ruta}: {error}")
            return False
        except OSError as error:
            print(f"⚠ Error al escribir {ruta}: {error}")
            return False