from PIL import Image
imagen = Image.open('./Personajes_pick/sylas.png')
nuevo_tamano = (663, 215)  
imagen = imagen.resize(nuevo_tamano)
imagen.save('./Personajes_pick/sylasR.png')
