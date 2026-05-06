from flask import Flask, request, jsonify, render_template
from services import ContactService

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    # Delegación de responsabilidad al servicio
    result, status_code = ContactService.process_submission(data)
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True)