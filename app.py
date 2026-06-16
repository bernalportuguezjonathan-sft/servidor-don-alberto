from flask import Flask, jsonify, request 
from datetime import datetime
import json, os

app = Flask(__name__)
DB = 'peritajes.json'

def handle_db(data=None):
    if data is None:
        return json.load(open(DB)) if os.path.exists(DB) else []
    with open(DB, 'w') as f:
        json.dump(data, f)

@app.route('/api/peritajes', methods=['GET','POST'])
def peritajes():

    datos = handle_db()

    if request.method == 'POST':

        nuevo = request.get_json()

        # HOTFIX DE PRODUCCION
        if 'placa' in nuevo:
            nuevo['placa'] = nuevo['placa'].upper()

        nuevo['fecha'] = datetime.now().strftime("%H:%M:%S")

        datos.append(nuevo)

        handle_db(datos)

        return jsonify({"msj": "OK"}), 201

    return jsonify(datos)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)