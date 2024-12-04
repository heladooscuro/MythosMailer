import sys
import os
import json
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch, MagicMock
from email_utils import render_template, save_email_record, send_email



# Ruta base para las pruebas
BASE_DIR = os.path.dirname(__file__)

@pytest.fixture
def test_data():
    """Datos de prueba para las funciones."""
    return {
        "recipient": "test@example.com",
        "subject": "Test Subject",
        "template_name": "welcome.html",
        "variables": {
            "name": "Tester",
            "welcome_message": "Welcome to the test system!",
            "footer": "Thank you for using MythosMailer."
        },
        "language": "en"
    }

def test_render_template(test_data):
    """
    Prueba la función render_template para verificar que las plantillas
    se rendericen correctamente con los datos proporcionados.
    """
    rendered = render_template(
        template_name=test_data["template_name"],
        variables=test_data["variables"],
        language=test_data["language"]
    )
    assert "Welcome, Tester!" in rendered
    assert "Welcome to the test system!" in rendered
    assert "Thank you for using MythosMailer." in rendered

def test_save_email_record():
    """
    Prueba la función save_email_record para guardar un archivo JSON.
    """
    # Datos de prueba
    recipient = "test@example.com"
    subject = "Test Subject"
    html_content = "<html><body>Test Email</body></html>"
    variables = {"name": "Tester", "welcome_message": "Welcome!", "footer": "Thank you."}
    language = "en"
    mode = "test"

    # Ruta esperada del archivo
    sanitized_subject = subject.replace(" ", "_").replace("/", "-")
    expected_filename = f"{recipient}_{sanitized_subject}.json"
    expected_filepath = os.path.join("test_emails", expected_filename)

    # Llama a la función para guardar el registro
    filepath = save_email_record(recipient, subject, html_content, variables, language, mode)

    # Verifica que el archivo se creó
    assert os.path.exists(filepath), f"El archivo {filepath} no fue creado."

    # Verifica el contenido del archivo
    with open(filepath, "r", encoding="utf-8") as f:
        content = json.load(f)

    assert content["recipient"] == recipient
    assert content["subject"] == subject
    assert content["html_content"] == html_content
    assert content["variables"] == variables
    assert content["language"] == language
    assert content["mode"] == mode

    # Limpia el archivo después de la prueba
    os.remove(filepath)

@patch("os.environ", {
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": "587",
    "SMTP_USERNAME": "your_email@gmail.com",
    "SMTP_PASSWORD": "your__2__password"
})
@patch("email_utils.SMTP_SERVER", "mock.smtp.server")
@patch("email_utils.SMTP_PORT", 587)
@patch("email_utils.SMTP_USERNAME", "mock_user@example.com")
@patch("email_utils.SMTP_PASSWORD", "mock_password")
@patch("email_utils.smtplib.SMTP")  # Asegúrate de que la ruta es correcta
def test_send_email_real(mock_smtp, test_data):
    """
    Prueba la función send_email para enviar un correo real.
    """
    # Configura el mock del servidor SMTP
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server

    # Llama a la función send_email
    send_email(
        recipient=test_data["recipient"],
        subject=test_data["subject"],
        template_name=test_data["template_name"],
        variables=test_data["variables"],
        language=test_data["language"],
        test_mode=False  # Modo real
    )

    # Verifica que smtplib.SMTP fue llamado correctamente
    mock_smtp.assert_called_with("mock.smtp.server", 587)  # Cambia estos valores si son diferentes

    # Verifica que las funciones dentro de SMTP fueron llamadas
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("mock_user@example.com", "mock_password")
    mock_server.sendmail.assert_called_once_with(
        "mock_user@example.com",
        "test@example.com",
        ANY  # Si no verificas el contenido exacto del mensaje
    )

@patch("email_utils.save_email_record")
def test_send_email_test_mode(mock_save_record, test_data):
    """
    Prueba la función send_email en modo prueba.
    Verifica que el correo no se envíe y se guarde localmente.
    """
    send_email(
        recipient=test_data["recipient"],
        subject=test_data["subject"],
        template_name=test_data["template_name"],
        variables=test_data["variables"],
        language=test_data["language"],
        test_mode=True
    )

    # Verificar que save_email_record fue llamado
    mock_save_record.assert_called_once()
