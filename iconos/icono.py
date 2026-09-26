"""Script para generar íconos básicos con PIL (opcional)."""
# Requiere: pip install pillow
from PIL import Image, ImageDraw

def crear_icono(ruta, color, letra):
    img = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill=color)
    img.save(ruta)
    print(f"✓ Creado: {ruta}")

# Colores
crear_icono("assets/logo.png", (44, 62, 80, 255), "R")
crear_icono("assets/icono_producto.png", (39, 174, 96, 255), "P")
crear_icono("assets/icono_usuario.png", (41, 128, 185, 255), "U")
crear_icono("assets/icono_venta.png", (243, 156, 18, 255), "V")