from PIL import Image

def redimensionar_imagen_manteniendo_aspecto(ruta_imagen_original, ruta_imagen_redimensionada, max_ancho, max_alto):
    # Abrir la imagen original
    imagen = Image.open(ruta_imagen_original)
    
    # Redimensionar manteniendo la relación de aspecto
    imagen.thumbnail((max_ancho, max_alto), Image.LANCZOS)
    
    # Guardar la imagen redimensionada
    imagen.save(ruta_imagen_redimensionada)
    print(f"Imagen redimensionada guardada en: {ruta_imagen_redimensionada}")

# Ejemplo de uso
ruta_original = 'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscar.png'
ruta_redimensionada = 'C:/Users/Luis/Downloads/Lol_bot/Lol_bot/Launcher/buscars.png'
max_ancho = 700  # Ajusta el tamaño según sea necesario
max_alto = 300   # Ajusta el tamaño según sea necesario

redimensionar_imagen_manteniendo_aspecto(ruta_original, ruta_redimensionada, max_ancho, max_alto)
