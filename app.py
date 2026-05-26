import json
import os
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

RUTA_JSON = '/var/www/html/peritajes.json'


def cargar_datos():
    if not os.path.exists(RUTA_JSON):
        return []
    with open(RUTA_JSON, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_datos(datos):
    with open(RUTA_JSON, 'w') as f:
        json.dump(datos, f, indent=4)

@app.route('/api/peritajes', methods=['GET'])
def listar_peritajes():
    datos = cargar_datos()
    return jsonify(datos), 200


@app.route('/api/peritajes', methods=['POST'])
def registrar_peritaje():
    nueva_moto = request.get_json()
    if not nueva_moto or 'placa' not in nueva_moto:
        return jsonify({"error": "Formato inválido"}), 400
    
    datos = cargar_datos()
    datos.append(nueva_moto)
    guardar_datos(datos)
    
    return jsonify({
        "message": f"Vehículo {nueva_moto['placa']} registrado con éxito",
        "datos": nueva_moto
    }), 201


@app.route('/api/peritajes/<placa>', methods=['DELETE'])
def eliminar_peritaje(placa):
    datos = cargar_datos()
    nueva_lista = [m for m in datos if m['placa'] != placa]
    
    if len(nueva_lista) == len(datos):
        return jsonify({"error": "Placa no encontrada"}), 404
    
    guardar_datos(nueva_lista)
    
    return jsonify({
        "message": f"Vehículo {placa} entregado al cliente con éxito",
        "moto_removida": {"placa": placa}
    }), 200


@app.route('/api/registros', methods=['GET'])
def obtener_registros():
    return jsonify({
        "servidor": "Servidor-TuApellido",
        "fecha_hora_servidor": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
