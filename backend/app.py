from flask import Flask, request, jsonify
from flask_cors import CORS

from main import execute_optimization

app = Flask(__name__)
CORS(app)

@app.route('/api/execute', methods=['POST'])
def execute_script():
    data = request.json
    result = execute_optimization(data['provincesDemand'], data['termoelectricas'])
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
