import sqlite3
from datetime import datetime


class ContactService:
    @staticmethod
    def init_db():
        """Inicializa la base de datos y la tabla si no existen."""
        with sqlite3.connect('nexus.db') as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')

    @staticmethod
    def process_submission(data):
        """Procesa la petición, valida y guarda en base de datos."""
        email = data.get('email')
        message = data.get('message')

        # Validación modular
        if not email or "@" not in email:
            return {"error": "Formato de email inválido"}, 400

        if not message or len(message.strip()) == 0:
            return {"error": "El mensaje no puede estar vacío"}, 400

        # Persistencia en SQLite
        try:
            with sqlite3.connect('nexus.db') as conn:
                conn.execute(
                    "INSERT INTO messages (email, message, date) VALUES (?, ?, ?)",
                    (email.strip(), message.strip(), datetime.now().isoformat())
                )
            print(f"Log Profesional: Mensaje de {email} guardado en SQLite.")
            return {"success": "Datos transmitidos y guardados con éxito."}, 200
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return {"error": "Error interno al procesar los datos."}, 500