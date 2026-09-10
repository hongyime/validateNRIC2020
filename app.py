from flask import Flask, render_template, request, jsonify
from utils import validate_nric, generate_barcode_base64
import os

app = Flask(__name__)

# Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(valid=False, message='Request must contain a JSON object.',
                       barcode=None, expected=None), 400

    nric = data.get('nric', '')
    if not isinstance(nric, str):
        return jsonify(valid=False, message='NRIC must be a string.',
                       barcode=None, expected=None), 400
    nric = nric.upper()
    
    validation_result = validate_nric(nric)
    
    response = {
        'valid': validation_result['valid'],
        'message': validation_result['message'],
        'barcode': None,
        'expected': validation_result.get('expected') 
    }
    
    if validation_result['valid']:
        barcode_b64 = generate_barcode_base64(nric)
        if barcode_b64:
            response['barcode'] = f"data:image/png;base64,{barcode_b64}"
            
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
