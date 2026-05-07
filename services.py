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


class AdminService:
    @staticmethod
    def get_messages(auth_token):
        """Obtiene los mensajes de contacto si el token es válido."""
        # Nota: En un entorno de producción, utiliza variables de entorno (os.getenv)
        if auth_token != "NEXUS_SECURE_2026":
            return {"error": "Acceso denegado. Token inválido."}, 401

        try:
            with sqlite3.connect('nexus.db') as conn:
                # row_factory permite transformar los resultados en diccionarios fácilmente
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, email, message, date FROM messages ORDER BY date DESC"
                )
                messages = [dict(row) for row in cursor.fetchall()]
            
            return {"messages": messages}, 200
            
        except sqlite3.Error as e:
            print(f"Error de lectura en DB: {e}")
            return {"error": "Error interno del servidor de datos."}, 500
        # Añadir esta clase al final de services.py

class NexusNodeService:
    """Servicio encargado de gestionar la recuperación de nodos temáticos (páginas random)."""
    
    @staticmethod
    def init_nodes_db():
        """Inicializa la tabla de nodos y la puebla con datos base si está vacía."""
        with sqlite3.connect('nexus.db') as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS nexus_nodes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    theme TEXT NOT NULL
                )
            ''')
            
            # Sembrar datos iniciales si la tabla está vacía
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM nexus_nodes")
            if cursor.fetchone()[0] == 0:
                nodes = [
                    ('dev-ops', 'DevOps & CI/CD', 'Automatización de despliegues y metodologías ágiles de integración continua.', 'black'),
                    ('cloud-computing', 'Cloud Computing', 'Diseño de sistemas distribuidos y arquitecturas elásticas en AWS y Azure.', 'blue'),
                    ('ai-ml', 'Inteligencia Artificial', 'Desarrollo de Modelos de Lenguaje, Redes Neuronales y Machine Learning.', 'slate')
                ]
                cursor.executemany("INSERT INTO nexus_nodes (id, title, description, theme) VALUES (?, ?, ?, ?)", nodes)
                print("Log Profesional: Tabla 'nexus_nodes' poblada con éxito.")

    @staticmethod
    def get_random_node_url():
        """Obtiene un ID aleatorio directo desde SQLite."""
        try:
            with sqlite3.connect('nexus.db') as conn:
                cursor = conn.cursor()
                # Función nativa de SQLite para aleatoriedad
                cursor.execute("SELECT id FROM nexus_nodes ORDER BY RANDOM() LIMIT 1")
                row = cursor.fetchone()
                selected_node = row[0] if row else 'dev-ops'
            return f"/node/{selected_node}"
        except sqlite3.Error as e:
            print(f"Error DB: {e}")
            return "/node/error"

    @staticmethod
    def get_node_data(node_id):
        """Obtiene la información de un nodo específico."""
        try:
            with sqlite3.connect('nexus.db') as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM nexus_nodes WHERE id = ?", (node_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error DB Nodes: {e}")
            return None