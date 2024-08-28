from PIL import Image

def redimensionar_imagen(ruta_imagen_original, ruta_imagen_redimensionada, nuevo_ancho, nuevo_alto):
    # Abrir la imagen original
    imagen = Image.open(ruta_imagen_original)
    
    # Redimensionar la imagen
    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    
    # Guardar la imagen redimensionada
    imagen_redimensionada.save(ruta_imagen_redimensionada)
    print(f"Imagen redimensionada guardada en: {ruta_imagen_redimensionada}")

# Ejemplo de uso
ruta_original = 'D:/Chente/Lolblot/Lol_bot/Launcher/aceptar.png'
ruta_redimensionada = 'D:/Chente/Lolblot/Lol_bot/Launcher/aceptar_redimensionada.png'
nuevo_ancho = 100  # Ajusta el tamaño según sea necesario
nuevo_alto = 32    # Ajusta el tamaño según sea necesario

redimensionar_imagen(ruta_original, ruta_redimensionada, nuevo_ancho, nuevo_alto)



def verificar_dimensiones_imagen(ruta_imagen):
    with Image.open(ruta_imagen) as img:
        print(f"Dimensiones de la imagen: {img.size}")

verificar_dimensiones_imagen(ruta_redimensionada)