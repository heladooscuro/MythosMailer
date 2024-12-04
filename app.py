from flask import Flask, request, jsonify
from email_utils import send_email
from config import DEBUG

# Inicializar la aplicación Flask
app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    """
    Endpoint para enviar correos electrónicos dinámicos.
    En modo prueba, guarda el correo en un archivo HTML y JSON.
    """
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json

        # Validar parámetros requeridos
        required_fields = ['recipient', 'subject', 'template_name', 'variables', 'language']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' es requerido"}), 400

        # Parámetros de la solicitud
        recipient = data['recipient']
        subject = data['subject']
        template_name = data['template_name']
        variables = data['variables']
        language = data['language']
        test_mode = data.get('test_mode', False)  # Por defecto, no es modo prueba

        # Enviar el correo
        send_email(
            recipient=recipient,
            subject=subject,
            template_name=template_name,
            variables=variables,
            language=language,
            test_mode=test_mode
        )

        # Respuesta según el modo
        message = "Correo guardado para pruebas" if test_mode else "Correo enviado exitosamente"
        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=DEBUG, host="127.0.0.1", port=5000)
