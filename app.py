from flask import Flask, request, jsonify
from datetime import datetime
import socket

app = Flask(__name__)

registros = {
    "servidor": "portuguez-server",
    "hora_servidor": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "inventario": [
        {"placa": "ABC123", "modelo": "Yamaha FZ", "color": "Negro"},
        {"placa": "XYZ789", "modelo": "Honda CB190R", "color": "Rojo"}
    ]
}

peritajes = [{"placa": "NSRS3057"}]

@app.route('/api/registros', methods=['GET'])
def obtener_registros():
    return jsonify(registros)

@app.route('/api/peritajes', methods=['GET'])
def obtener_peritajes():
    return jsonify(peritajes)

@app.route('/api/inventario', methods=['GET'])
def inventario():
    return jsonify({
        "mensaje": "Inventario en desarrollo",
        "repuestos": ["Aceite", "Bujias", "Filtros"]
    })

@app.route('/api/peritajes', methods=['POST'])
def registrar_peritaje():
    data = request.json
    nueva_moto = {"placa": data["placa"].upper()}
    peritajes.append(nueva_moto)
    return jsonify({"mensaje": "Peritaje registrado con éxito", "moto": nueva_moto}), 201

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
