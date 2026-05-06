# Responsabilidad: Procesar y validar la información del contacto
class ContactService:
    @staticmethod
    def validate_and_process(data):
        email = data.get('email')
        message = data.get('message')

        if not email or "@" not in email:
            return {"error": "Email inválido"}, 400
        
        if not message or len(message) < 10:
            return {"error": "El mensaje es muy corto"}, 400

        # Aquí podrías integrar una DB o envío de correos en el futuro
        print(f"Log: Mensaje de {email} procesado con éxito.")
        return {"success": "Conexión establecida"}, 200