"""Punto de entrada principal del sistema restaurante_app."""

from typing import Optional
from servicios.restaurante import Restaurante
from servicios.archivo_servicio import ArchivoServicio
from modelos.producto import Producto


def mostrar_menu() -> None:
    """Muestra el menú principal del sistema."""
    print("\n" + "=" * 50)
    print("SISTEMA DE ADMINISTRACIÓN DEL RESTAURANTE")
    print("=" * 50)
    print("1. Registrar producto")
    print("2. Buscar producto")
    print("3. Listar todos los productos")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Buscar productos por categoría")
    print("0. Salir")
    print("=" * 50)


def registrar_producto_menu(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    """
    Maneja el registro de un nuevo producto.
    
    Args:
        restaurante: Instancia del servicio Restaurante
        archivo: Instancia del servicio ArchivoServicio
    """
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    
    try:
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            return
        
        try:
            precio = float(input("Precio del producto: ").strip())
            if precio <= 0:
                print("Error: El precio debe ser mayor a 0")
                return
        except ValueError:
            print("Error: Ingrese un precio válido (número)")
            return
        
        categoria = input("Categoría del producto: ").strip()
        if not categoria:
            print("Error: La categoría no puede estar vacía")
            return
        
        descripcion = input("Descripción (opcional): ").strip()
        descripcion = descripcion if descripcion else None
        
        producto = Producto(nombre, precio, categoria, descripcion)
        
        if restaurante.registrar_producto(producto):
            if archivo.guardar_productos(restaurante.obtener_productos()):
                print(f"✓ Producto '{nombre}' registrado correctamente")
            else:
                print("⚠ Producto registrado pero no se pudo guardar en el archivo")
        else:
            print(f"Error: Ya existe un producto con el nombre '{nombre}'")
            
    except ValueError as error:
        print(f"Error de validación: {error}")
    except Exception as error:
        print(f"Error inesperado: {error}")


def buscar_producto_menu(restaurante: Restaurante) -> None:
    """
    Maneja la búsqueda de un producto por nombre.
    
    Args:
        restaurante: Instancia del servicio Restaurante
    """
    print("\n--- BUSCAR PRODUCTO ---")
    
    nombre = input("Nombre del producto a buscar: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío")
        return
    
    producto = restaurante.buscar_producto(nombre)
    if producto:
        print(f"\n✓ Producto encontrado:")
        print(f"  {producto}")
    else:
        print(f"No se encontró un producto con el nombre '{nombre}'")


def listar_productos_menu(restaurante: Restaurante) -> None:
    """
    Muestra todos los productos registrados.
    
    Args:
        restaurante: Instancia del servicio Restaurante
    """
    print("\n" + restaurante.listar_productos())


def actualizar_producto_menu(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    """
    Maneja la actualización de un producto.
    
    Args:
        restaurante: Instancia del servicio Restaurante
        archivo: Instancia del servicio ArchivoServicio
    """
    print("\n--- ACTUALIZAR PRODUCTO ---")
    
    nombre_actual = input("Nombre del producto a actualizar: ").strip()
    if not nombre_actual:
        print("Error: El nombre no puede estar vacío")
        return
    
    producto = restaurante.buscar_producto(nombre_actual)
    if not producto:
        print(f"No se encontró un producto con el nombre '{nombre_actual}'")
        return
    
    print(f"\nProducto actual: {producto}")
    print("Deje en blanco los campos que no desee modificar")
    
    nuevo_nombre = input("Nuevo nombre: ").strip()
    nuevo_nombre = nuevo_nombre if nuevo_nombre else None
    
    try:
        nuevo_precio_input = input("Nuevo precio: ").strip()
        nuevo_precio = float(nuevo_precio_input) if nuevo_precio_input else None
        if nuevo_precio is not None and nuevo_precio <= 0:
            print("Error: El precio debe ser mayor a 0")
            return
    except ValueError:
        print("Error: Ingrese un precio válido")
        return
    
    nueva_categoria = input("Nueva categoría: ").strip()
    nueva_categoria = nueva_categoria if nueva_categoria else None
    
    nueva_descripcion = input("Nueva descripción: ").strip()
    nueva_descripcion = nueva_descripcion if nueva_descripcion else None
    
    try:
        if restaurante.actualizar_producto(
            nombre_actual,
            nuevo_nombre,
            nuevo_precio,
            nueva_categoria,
            nueva_descripcion
        ):
            if archivo.guardar_productos(restaurante.obtener_productos()):
                print("✓ Producto actualizado correctamente")
            else:
                print("⚠ Producto actualizado pero no se pudo guardar en el archivo")
        else:
            print(f"No se encontró un producto con el nombre '{nombre_actual}'")
            
    except ValueError as error:
        print(f"Error de validación: {error}")
    except Exception as error:
        print(f"Error inesperado: {error}")


def eliminar_producto_menu(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    """
    Maneja la eliminación de un producto.
    
    Args:
        restaurante: Instancia del servicio Restaurante
        archivo: Instancia del servicio ArchivoServicio
    """
    print("\n--- ELIMINAR PRODUCTO ---")
    
    nombre = input("Nombre del producto a eliminar: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío")
        return
    
    producto = restaurante.buscar_producto(nombre)
    if not producto:
        print(f"No se encontró un producto con el nombre '{nombre}'")
        return
    
    print(f"Producto a eliminar: {producto}")
    confirmar = input("¿Está seguro de eliminar este producto? (s/N): ").strip().lower()
    
    if confirmar == 's':
        if restaurante.eliminar_producto(nombre):
            if archivo.guardar_productos(restaurante.obtener_productos()):
                print(f"✓ Producto '{nombre}' eliminado correctamente")
            else:
                print("⚠ Producto eliminado pero no se pudo guardar el cambio en el archivo")
        else:
            print(f"No se encontró un producto con el nombre '{nombre}'")
    else:
        print("Operación cancelada")


def buscar_por_categoria_menu(restaurante: Restaurante) -> None:
    """
    Maneja la búsqueda de productos por categoría.
    
    Args:
        restaurante: Instancia del servicio Restaurante
    """
    print("\n--- BUSCAR POR CATEGORÍA ---")
    
    categoria = input("Categoría a buscar: ").strip()
    if not categoria:
        print("Error: La categoría no puede estar vacía")
        return
    
    productos = restaurante.buscar_productos_por_categoria(categoria)
    
    if productos:
        print(f"\n✓ Productos encontrados en la categoría '{categoria}':")
        print("-" * 40)
        for i, producto in enumerate(productos, 1):
            print(f"{i}. {producto}")
        print("-" * 40)
        print(f"Total: {len(productos)} productos")
    else:
        print(f"No se encontraron productos en la categoría '{categoria}'")


def main() -> None:
    """Función principal del programa."""
    print("=== INICIANDO SISTEMA RESTAURANTE APP ===")
    
    # Crear servicios
    restaurante = Restaurante()
    archivo_servicio = ArchivoServicio()
    
    # Cargar productos desde el archivo
    print("\nCargando productos desde el archivo...")
    productos_cargados = archivo_servicio.cargar_productos()
    
    if productos_cargados:
        restaurante.cargar_productos(productos_cargados)
        print(f"✓ Se cargaron {len(productos_cargados)} productos")
    else:
        print("No se encontraron productos guardados. Comenzando con lista vacía")
    
    # Loop principal
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            registrar_producto_menu(restaurante, archivo_servicio)
        
        elif opcion == "2":
            buscar_producto_menu(restaurante)
        
        elif opcion == "3":
            listar_productos_menu(restaurante)
        
        elif opcion == "4":
            actualizar_producto_menu(restaurante, archivo_servicio)
        
        elif opcion == "5":
            eliminar_producto_menu(restaurante, archivo_servicio)
        
        elif opcion == "6":
            buscar_por_categoria_menu(restaurante)
        
        elif opcion == "0":
            print("\nGuardando cambios...")
            if archivo_servicio.guardar_productos(restaurante.obtener_productos()):
                print("✓ Cambios guardados correctamente")
            else:
                print("⚠ No se pudieron guardar todos los cambios")
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()