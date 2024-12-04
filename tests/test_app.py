import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture que proporciona un cliente de prueba para la aplicación Flask.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_send_email_success(client):
    """
    Prueba el endpoint /send-email en modo prueba con datos válidos.
    """
    response = client.post(
        "/send-email",
        json={
            "recipient": "test@example.com",
            "subject": "Test Email",
            "template_name": "welcome.html",
            "variables": {
                "name": "Tester",
                "welcome_message": "Welcome to the test system!",
                "footer": "Thank you for using our service."
            },
            "language": "en",
            "test_mode": True
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Correo guardado para pruebas"}

def test_missing_field(client):
    """
    Prueba el endpoint /send-email con datos incompletos (campo faltante).
    """
    response = client.post(
        "/send-email",
        json={
            "subject": "Test Email",
            "template_name": "welcome.html",
            "variables": {
                "name": "Tester"
            },
            "language": "en",
            "test_mode": True
        },
    )
    assert response.status_code == 400
    assert "recipient" in response.json["error"]

def test_invalid_language(client):
    """
    Prueba el endpoint /send-email con un idioma no soportado.
    """
    response = client.post(
        "/send-email",
        json={
            "recipient": "test@example.com",
            "subject": "Test Email",
            "template_name": "welcome.html",
            "variables": {
                "name": "Tester",
                "welcome_message": "Welcome to the test system!",
                "footer": "Thank you for using our service."
            },
            "language": "unknown_language",
            "test_mode": True
        },
    )
    assert response.status_code == 500
    assert "error" in response.json

# def test_real_email_mode(client):
#     """
#     Prueba el endpoint /send-email en modo real.
#     (Requiere que el sistema esté configurado correctamente para enviar correos reales.)
#     """
#     response = client.post(
#         "/send-email",
#         json={
#             "recipient": "realuser@example.com",
#             "subject": "Real Email Test",
#             "template_name": "welcome.html",
#             "variables": {
#                 "name": "Real User",
#                 "welcome_message": "This is a real email test!",
#                 "footer": "Best regards, MythosMailer Team."
#             },
#             "language": "en",
#             "test_mode": False
#         },
#     )
#     assert response.status_code == 200
#     assert response.json == {"message": "Correo enviado exitosamente"}
