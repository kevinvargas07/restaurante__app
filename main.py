from servicios import Restaurante
import os

# TUPLA: opciones fijas del menú
OPCIONES_MENU = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Buscar usuario",
    "8. Listar usuarios",
    "9. Realizar venta",
    "10. Consultar ventas por usuario",
    "11. Listar ventas",
    "12. Mostrar categorías",
    "13. Salir"
)

def mostrar_menu() -> None:
    print("\n" + "=" * 50)
    print("        SISTEMA DE RESTAURANTE - SEMANA 12")
    print("=" * 50)
    for opcion in OPCIONES_MENU:
        print(opcion)
    print("-" * 50)

def main() -> None:
    # Asegurar que el directorio datos existe
    os.makedirs("datos", exist_ok=True)
    
    restaurante = Restaurante()

    # DICCIONARIO: asocia cada opción con una función
    acciones = {
        "1": lambda: registrar_producto(restaurante),
        "2": lambda: buscar_producto(restaurante),
        "3": lambda: actualizar_producto(restaurante),
        "4": lambda: eliminar_producto(restaurante),
        "5": lambda: listar_productos(restaurante),
        "6": lambda: registrar_usuario(restaurante),
        "7": lambda: buscar_usuario(restaurante),
        "8": lambda: listar_usuarios(restaurante),
        "9": lambda: realizar_venta(restaurante),
        "10": lambda: consultar_ventas_usuario(restaurante),
        "11": lambda: listar_ventas(restaurante),
        "12": lambda: mostrar_categorias(restaurante),
        "13": lambda: salir()
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion in acciones:
            if acciones[opcion]() is False:
                break
        else:
            print("❌ Opción no válida. Intente de nuevo.")

# --- Funciones auxiliares ---

def registrar_producto(restaurante: Restaurante) -> None:
    try:
        codigo = input("Código del producto: ").strip()
        nombre = input("Nombre: ").strip()
        categoria = input("Categoría: ").strip()
        precio = float(input("Precio: "))
        stock = int(input("Stock inicial: ") or "0")
        if restaurante.registrar_producto(codigo, nombre, categoria, precio, stock):
            print("✅ Producto registrado correctamente.")
        else:
            print("❌ Código ya existente.")
    except ValueError:
        print("❌ Error: precio o stock deben ser números.")

def buscar_producto(restaurante: Restaurante) -> None:
    codigo = input("Código del producto a buscar: ").strip()
    producto = restaurante.buscar_producto(codigo)
    if producto:
        print(f"🔍 Producto encontrado: {producto}")
    else:
        print("❌ Producto no encontrado.")

def actualizar_producto(restaurante: Restaurante) -> None:
    try:
        codigo = input("Código del producto a actualizar: ").strip()
        nombre = input("Nuevo nombre: ").strip()
        categoria = input("Nueva categoría: ").strip()
        precio = float(input("Nuevo precio: "))
        stock = input("Nuevo stock (Enter para mantener): ").strip()
        stock_nuevo = int(stock) if stock else None
        if restaurante.actualizar_producto(codigo, nombre, categoria, precio, stock_nuevo):
            print("✅ Producto actualizado.")
        else:
            print("❌ Producto no encontrado.")
    except ValueError:
        print("❌ Error: precio o stock deben ser números.")

def eliminar_producto(restaurante: Restaurante) -> None:
    codigo = input("Código del producto a eliminar: ").strip()
    if restaurante.eliminar_producto(codigo):
        print("✅ Producto eliminado.")
    else:
        print("❌ Producto no encontrado.")

def listar_productos(restaurante: Restaurante) -> None:
    productos = restaurante.listar_productos()
    if not productos:
        print("📭 No hay productos registrados.")
    else:
        print("\n📋 LISTA DE PRODUCTOS:")
        for p in productos:
            print(p)

def registrar_usuario(restaurante: Restaurante) -> None:
    identificacion = input("Identificación: ").strip()
    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()
    if restaurante.registrar_usuario(identificacion, nombre, correo):
        print("✅ Usuario registrado correctamente.")
    else:
        print("❌ Identificación ya existente.")

def buscar_usuario(restaurante: Restaurante) -> None:
    identificacion = input("Identificación del usuario a buscar: ").strip()
    usuario = restaurante.buscar_usuario(identificacion)
    if usuario:
        print(f"🔍 Usuario encontrado: {usuario}")
    else:
        print("❌ Usuario no encontrado.")

def listar_usuarios(restaurante: Restaurante) -> None:
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("📭 No hay usuarios registrados.")
    else:
        print("\n📋 LISTA DE USUARIOS:")
        for u in usuarios:
            print(u)

def realizar_venta(restaurante: Restaurante) -> None:
    try:
        codigo_venta = input("Código de venta: ").strip()
        identificacion_usuario = input("Identificación del usuario: ").strip()
        
        if not restaurante.buscar_usuario(identificacion_usuario):
            print("❌ Usuario no encontrado.")
            return
        
        items = []
        while True:
            codigo_producto = input("Código del producto (Enter para terminar): ").strip()
            if not codigo_producto:
                break
            cantidad = int(input("Cantidad: "))
            items.append({"codigo_producto": codigo_producto, "cantidad": cantidad})
        
        if not items:
            print("❌ Debe agregar al menos un producto.")
            return
        
        if restaurante.registrar_venta(codigo_venta, identificacion_usuario, items):
            print("✅ Venta registrada correctamente.")
        else:
            print("❌ Error: stock insuficiente o producto no encontrado.")
    except ValueError:
        print("❌ Error: la cantidad debe ser un número.")

def consultar_ventas_usuario(restaurante: Restaurante) -> None:
    identificacion = input("Identificación del usuario: ").strip()
    ventas = restaurante.consultar_ventas_por_usuario(identificacion)
    if not ventas:
        print("📭 El usuario no tiene ventas registradas.")
    else:
        print(f"\n📋 VENTAS DEL USUARIO {identificacion}:")
        for v in ventas:
            print(v)

def listar_ventas(restaurante: Restaurante) -> None:
    ventas = restaurante.listar_ventas()
    if not ventas:
        print("📭 No hay ventas registradas.")
    else:
        print("\n📋 LISTA DE VENTAS:")
        for v in ventas:
            print(v)

def mostrar_categorias(restaurante: Restaurante) -> None:
    categorias = restaurante.obtener_categorias_unicas()
    if not categorias:
        print("📭 No hay productos registrados para mostrar categorías.")
    else:
        print("\n🏷️ CATEGORÍAS ÚNICAS:")
        for cat in sorted(categorias):
            print(f"- {cat}")

def salir() -> bool:
    print("👋 ¡Hasta luego!")
    return False

if __name__ == "__main__":
    main()