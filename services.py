class ContactService:
    @staticmethod
    def process_submission(data):
        email = data.get('email')
        message = data.get('message')

        # Validación modular
        if not email or "@" not in email:
            return {"error": "Formato de email inválido"}, 400
        
        # Simulación de persistencia (Aquí iría tu lógica de SQL)
        print(f"Log Profesional: Mensaje de {email} recibido.")
        return {"success": "Datos transmitidos con éxito al servidor."}, 200