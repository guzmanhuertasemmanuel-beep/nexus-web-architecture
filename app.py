from flask import Flask, request, jsonify, render_template
from services import ContactService

app = Flask(__name__)

# Inicialización de la base de datos delegada al servicio
ContactService.init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    # Delegación estricta de responsabilidad al servicio SRP
    result, status_code = ContactService.process_submission(data)
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)