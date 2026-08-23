"""Módulo que maneja la persistencia de datos en archivos JSON."""

import json
import os
from typing import List, Dict, Any, Optional
from modelos.producto import Producto


class ArchivoServicio:
    """Servicio encargado de leer y escribir datos en archivos JSON."""
    
    RUTA_PRODUCTOS: str = "datos/productos.json"
    
    def __init__(self) -> None:
        """Inicializa el servicio creando el directorio si no existe."""
        self._crear_directorio()
    
    def _crear_directorio(self) -> None:
        """Crea el directorio datos/ si no existe."""
        directorio = os.path.dirname(self.RUTA_PRODUCTOS)
        if directorio and not os.path.exists(directorio):
            try:
                os.makedirs(directorio)
            except PermissionError as error:
                print(f"Error de permisos al crear el directorio: {error}")
    
    def guardar_productos(self, productos: List[Producto]) -> bool:
        """
        Guarda una lista de productos en el archivo JSON.
        
        Args:
            productos: Lista de productos a guardar
            
        Returns:
            True si se guardó correctamente, False en caso de error
        """
        try:
            # Convertir productos a diccionarios
            datos = [producto.to_dict() for producto in productos]
            
            # Guardar en archivo JSON con formato legible
            with open(self.RUTA_PRODUCTOS, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            
            return True
            
        except PermissionError as error:
            print(f"Error de permisos al guardar el archivo: {error}")
            return False
        except OSError as error:
            print(f"Error al escribir el archivo: {error}")
            return False
        except Exception as error:
            print(f"Error inesperado al guardar productos: {error}")
            return False
    
    def cargar_productos(self) -> List[Producto]:
        """
        Carga los productos desde el archivo JSON.
        
        Returns:
            Lista de productos cargados (vacía si hay error)
        """
        # Verificar si el archivo existe
        if not os.path.exists(self.RUTA_PRODUCTOS):
            return []
        
        try:
            with open(self.RUTA_PRODUCTOS, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                
                # Si el archivo está vacío, retornar lista vacía
                if not contenido.strip():
                    return []
                
                datos = json.loads(contenido)
            
            # Validar que los datos sean una lista
            if not isinstance(datos, list):
                print("El archivo no contiene una lista válida de productos")
                return []
            
            # Convertir cada diccionario a Producto
            productos = []
            for i, item in enumerate(datos):
                try:
                    if not isinstance(item, dict):
                        print(f"El elemento {i} no es un diccionario válido, omitido")
                        continue
                    
                    producto = Producto.from_dict(item)
                    productos.append(producto)
                    
                except KeyError as error:
                    print(f"Error en el elemento {i}: falta el campo {error}")
                    continue
                except ValueError as error:
                    print(f"Error en el elemento {i}: {error}")
                    continue
                except TypeError as error:
                    print(f"Error de tipo en el elemento {i}: {error}")
                    continue
            
            print(f"Se cargaron {len(productos)} productos desde el archivo")
            return productos
            
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as error:
            print(f"Error: El archivo no contiene un JSON válido: {error}")
            return []
        except PermissionError as error:
            print(f"Error de permisos al leer el archivo: {error}")
            return []
        except OSError as error:
            print(f"Error al leer el archivo: {error}")
            return []
        except Exception as error:
            print(f"Error inesperado al cargar productos: {error}")
            return []
    
    def archivo_existe(self) -> bool:
        """
        Verifica si el archivo de productos existe.
        
        Returns:
            True si el archivo existe, False en caso contrario
        """
        return os.path.exists(self.RUTA_PRODUCTOS)