from PIL import Image

# Cargar la imagen
imagen = Image.open('D:/Chente/Lolblot/Lol_bot/Launcher/aceptar.png')

# Obtener las dimensiones
ancho, alto = imagen.size

print(f"Dimensiones de la imagen: {ancho}x{alto} píxeles")