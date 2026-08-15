from servicios import Restaurante

# TUPLA: opciones fijas del menú (nunca cambian)
OPCIONES_MENU = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "8. Mostrar categorías",
    "9. Salir"
)

def mostrar_menu() -> None:
    print("\n" + "=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    for opcion in OPCIONES_MENU:
        print(opcion)
    print("-" * 40)

def main() -> None:
    restaurante = Restaurante()

    # DICCIONARIO: asocia cada opción con una función
    acciones = {
        "1": lambda: registrar_producto(restaurante),
        "2": lambda: buscar_producto(restaurante),
        "3": lambda: actualizar_producto(restaurante),
        "4": lambda: eliminar_producto(restaurante),
        "5": lambda: listar_productos(restaurante),
        "6": lambda: registrar_usuario(restaurante),
        "7": lambda: listar_usuarios(restaurante),
        "8": lambda: mostrar_categorias(restaurante),
        "9": lambda: salir()
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion in acciones:
            if acciones[opcion]() is False:
                break
        else:
            print("❌ Opción no válida. Intente de nuevo.")

# --- Funciones auxiliares para manejo de entrada ---

def registrar_producto(restaurante: Restaurante) -> None:
    try:
        codigo = input("Código del producto: ").strip()
        nombre = input("Nombre: ").strip()
        categoria = input("Categoría: ").strip()
        precio = float(input("Precio: "))
        if restaurante.registrar_producto(codigo, nombre, categoria, precio):
            print("✅ Producto registrado correctamente.")
        else:
            print("❌ Código ya existente.")
    except ValueError:
        print("❌ Error: el precio debe ser un número.")

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
        if restaurante.actualizar_producto(codigo, nombre, categoria, precio):
            print("✅ Producto actualizado.")
        else:
            print("❌ Producto no encontrado.")
    except ValueError:
        print("❌ Error: el precio debe ser un número.")

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

def listar_usuarios(restaurante: Restaurante) -> None:
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("📭 No hay usuarios registrados.")
    else:
        print("\n📋 LISTA DE USUARIOS:")
        for u in usuarios:
            print(u)

def mostrar_categorias(restaurante: Restaurante) -> None:
    categorias = restaurante.obtener_categorias_unicas()
    if not categorias:
        print("📭 No hay productos registrados para mostrar categorías.")
    else:
        # CONJUNTO: mostramos categorías únicas
        print("\n🏷️ CATEGORÍAS ÚNICAS:")
        for cat in sorted(categorias):
            print(f"- {cat}")

def salir() -> bool:
    print("👋 ¡Hasta luego!")
    return False

if __name__ == "__main__":
    main()