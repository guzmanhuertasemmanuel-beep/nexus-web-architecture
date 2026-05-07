from flask import Flask, request, jsonify, render_template
# Importamos ambos servicios
from services import ContactService, AdminService 

app = Flask(__name__)

ContactService.init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    result, status_code = ContactService.process_submission(data)
    return jsonify(result), status_code

# NUEVA RUTA: Endpoint protegido para el Command Center
@app.route('/api/admin/messages', methods=['GET'])
def get_admin_messages():
    # Extraemos el token personalizado de los headers
    auth_token = request.headers.get('X-Nexus-Auth')
    result, status_code = AdminService.get_messages(auth_token)
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True)