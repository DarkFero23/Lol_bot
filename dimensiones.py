from PIL import Image

# Cargar la imagen
imagen = Image.open('C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/aceptar_gozu.png')

# Obtener las dimensiones
ancho, alto = imagen.size

print(f"Dimensiones de la imagen: {ancho}x{alto} píxeles")