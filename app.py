from flask import Flask, request, jsonify
from flask_cors import CORS
from faker import Faker
import logging

app = Flask(__name__)
CORS(app)  # Habilitar CORS

fake = Faker()

logging.basicConfig(level=logging.DEBUG)

def generate_json(fields, num_entries=10):
    logging.debug("Generando JSON con %d entradas...", num_entries)
    data = []
    for i in range(num_entries):
        entry = {}
        for field in fields:
            name = field.get("name")
            field_type = field.get("type")

            if field_type == "id":
                entry[name] = i + 1  # Genera IDs incrementales 1,2,3...
            elif field_type == "str":
                entry[name] = fake.name()
            elif field_type == "int":
                entry[name] = fake.random_int(min=0, max=100)
            elif field_type == "float":
                entry[name] = round(fake.random_number(digits=5, fix_len=True) / 100, 2)
            elif field_type == "email":
                entry[name] = fake.email()
            elif field_type == "bool":
                entry[name] = fake.boolean()
            elif field_type == "date":
                entry[name] = fake.date()
            elif field_type == "address":
                entry[name] = fake.address()
            elif field_type == "phone_number":
                entry[name] = fake.phone_number()
            elif field_type == "text":
                entry[name] = fake.text()
            elif field_type == "url":
                entry[name] = fake.url()   
            else:
                entry[name] = None
        data.append(entry)
    logging.debug("JSON generado: %s", data)
    return data

@app.route('/generate', methods=['POST'])
def generate():
    try:
        logging.debug("Solicitud recibida para generar JSON")
        # Parsear datos del cuerpo de la solicitud
        request_data = request.get_json()
        logging.debug("Datos recibidos: %s", request_data)
        fields = request_data.get("schema", [])  # Lista de campos
        num_entries = request_data.get("num_entries", 10)
        
        # Validar si el número de entradas es excesivo
        MAX_ENTRIES = 1000  # Define el límite máximo de entradas permitidas
        if num_entries > MAX_ENTRIES:
            return jsonify({"error": "Número de entradas excesivo"}), 400

        # Validar datos de entrada
        if not isinstance(fields, list) or not all("name" in field and "type" in field for field in fields):
            logging.error("Esquema inválido: %s", fields)
            return jsonify({"error": "El esquema debe ser una lista de campos con propiedades 'name' y 'type'"}), 400

        # Generar JSON de prueba
        generated_data = generate_json(fields, num_entries)
        logging.debug("Datos generados correctamente")
        return jsonify(generated_data)

    except Exception as e:
        logging.error("Error al generar JSON: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.debug("Iniciando aplicación Flask")
    app.run(debug=True)
