from flask import Flask, request, jsonify, render_template
from services import ContactService

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    # La ruta solo recibe el request y delega la lógica al servicio
    data = request.get_json()
    result, status = ContactService.validate_and_process(data)
    return jsonify(result), status

if __name__ == '__main__':
    app.run(debug=True)