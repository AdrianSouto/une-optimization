from flask import Flask, request, jsonify
from flask_cors import CORS

from main import execute_optimization
from schedule import schedule

app = Flask(__name__)
CORS(app)

@app.route('/api/execute', methods=['POST'])
def execute_script():
    data = request.json
    result = execute_optimization(data['provincesDemand'], data['termoelectricas'], data["blockDemand"])
    print(result)
    return jsonify(result)


@app.route('/api/schedule', methods=['POST'])
def schedule_optimization():
    data = request.json
    province_demand = data.get('provinceDemand', {})
    blocks_quantity = data.get('blocksQuantity', 0)

    # Extraer powerCutHours del diccionario province_demand
    power_cut_hours = province_demand.get('powerCutHours', 0)

    # Llamar a generate_power_cut_schedule con el valor correcto
    result = schedule(power_cut_hours, blocks_quantity)
    return jsonify(result)

if __name__ == '__main__':
    app.run()

