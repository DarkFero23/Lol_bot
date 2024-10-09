from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from .aceptar import ejecutar_seleccion, esperar_imagen , esperar_y_aceptar_partida , seleccionar_campeon_ban ,seleccionar_campeon_pick, limpiar_buscador , pre_pick_campeon,hacer_click_boton

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes desde el frontend

@app.route('/campeones', methods=['GET'])
def obtener_campeones():
    # Ruta de la carpeta donde están las imágenes de los campeones
    carpeta_campeones = './Personajes_pick'
    campeones = []

    # Obtener los nombres de los archivos de la carpeta
    for filename in os.listdir(carpeta_campeones):
        if filename.endswith('.png'):  # Verifica que sea una imagen
            campeon = filename[:-4]  # Eliminar la extensión .png
            campeones.append(campeon)

    return jsonify(campeones)


@app.route('/ejecutar_seleccion', methods=['POST'])
def ejecutar_seleccion_api():
    data = request.json
    campeon_pick = data['campeon_pick']
    campeon_ban = data['campeon_ban']
    print("El camepon para pickear es"+ campeon_pick)
    print("El camepon para banear es" + campeon_ban)
    # Llama a la función que ejecuta la lógica de selección
    resultado = ejecutar_seleccion(campeon_pick, campeon_ban)
    
    if resultado is False:
        return jsonify(message="Error al ejecutar la selección."), 500
    
    return jsonify(message=f"Seleccionaste {campeon_pick} y baneaste {campeon_ban}")


if __name__ == '__main__':
    app.run(debug=True)