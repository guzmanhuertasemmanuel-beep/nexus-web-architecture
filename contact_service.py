# --- contact_service.py ---
# Responsabilidad: Lógica de negocio y validación de datos.

class ContactService:
    @staticmethod
    def process_contact_message(data):
        # 1. Validación básica
        if not data or not data.get('email') or not data.get('message'):
            return {"success": False, "error": "Faltan datos requeridos."}, 400
            
        # Aquí aislaríamos la capa de persistencia en el futuro (ej. guardar en SQLite)
        # db_repository.save(data)
        
        # 2. Procesamiento (Simulado)
        print(f"Mensaje procesado de: {data.get('email')}")
        
        return {"success": True, "message": "Mensaje recibido correctamente."}, 200


# --- app.py ---
# Responsabilidad: Capa de presentación (Enrutamiento HTTP).

from flask import Flask, request, jsonify
from contact_service import ContactService

app = Flask(__name__)

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    
    # Delegamos la lógica al servicio externo para no saturar el controlador
    response, status_code = ContactService.process_contact_message(data)
    
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)