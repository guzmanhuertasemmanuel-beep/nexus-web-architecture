from flask import Flask, request, jsonify, render_template, redirect
# IMPORTANTE: Importar el nuevo servicio
from services import ContactService, AdminService, NexusNodeService 

app = Flask(__name__)

# Inicializamos ambas tablas en la base de datos
ContactService.init_db()
NexusNodeService.init_nodes_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    result, status_code = ContactService.process_submission(data)
    return jsonify(result), status_code

@app.route('/api/admin/messages', methods=['GET'])
def get_admin_messages():
    auth_token = request.headers.get('X-Nexus-Auth')
    result, status_code = AdminService.get_messages(auth_token)
    return jsonify(result), status_code

# --- NUEVOS ENDPOINTS: SISTEMA DE NODOS ALEATORIOS ---

@app.route('/explore/random')
def random_node():
    """Redirige al usuario a un nodo aleatorio del ecosistema Nexus."""
    node_url = NexusNodeService.get_random_node_url()
    return redirect(node_url)

@app.route('/node/<node_id>')
def view_node(node_id):
    """Renderiza el nodo en formato JSON o Vista (Para el proyecto escolar, retornamos JSON para probar que funciona)."""
    node_data = NexusNodeService.get_node_data(node_id)
    if not node_data:
        return jsonify({"error": "Error 404: Nodo no encontrado en la red Nexus."}), 404
    
    # Nota académica: Aquí normalmente usarías render_template('node.html', data=node_data)
    return jsonify({"status": "Conexión Establecida", "node_data": node_data}), 200

if __name__ == '__main__':
    app.run(debug=True)