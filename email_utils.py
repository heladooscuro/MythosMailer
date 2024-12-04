import json
import logging
import os
import smtplib

from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD


# Configuración de carpetas y logging
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
TEST_EMAILS_DIR = os.path.join(os.path.dirname(__file__), "test_emails")
SENT_EMAILS_DIR = os.path.join(os.path.dirname(__file__), "sent_emails")
LOG_FILE = os.path.join(os.path.dirname(__file__), "emails.log")

# Crear carpetas necesarias
os.makedirs(TEST_EMAILS_DIR, exist_ok=True)
os.makedirs(SENT_EMAILS_DIR, exist_ok=True)

# Configuración de Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Configuración de logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def render_template(template_name: str, variables: dict, language: str) -> str:
    """
    Renderiza una plantilla usando Jinja2, con soporte multilingüe.
    """
    template_path = os.path.join(language, template_name)
    template = env.get_template(template_path)
    return template.render(variables)

def save_email_record(recipient: str, subject: str, html_content: str, variables: dict, language: str, mode: str):
    """
    Guarda un registro del correo enviado o generado en un archivo JSON.
    """
    sanitized_subject = subject.replace(" ", "_").replace("/", "-")
    filename = f"{recipient}_{sanitized_subject}.json"
    filepath = os.path.join(SENT_EMAILS_DIR if mode == "real" else TEST_EMAILS_DIR, filename)

    record = {
        "recipient": recipient,
        "subject": subject,
        "variables": variables,
        "language": language,
        "html_content": html_content,
        "mode": mode,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=4)

    logging.info(f"Correo registrado: Destinatario={recipient}, Asunto={subject}, Archivo={filepath}")

    if mode == "test":
        print(f"Correo guardado en modo prueba: {filepath}")
    else:
        print(f"Correo enviado registrado: {filepath}")

    return filepath


def send_email(recipient: str, subject: str, template_name: str, variables: dict, language: str = "en", test_mode: bool = False):
    """
    Envía un correo electrónico con una plantilla dinámica.
    En modo prueba, guarda el correo en un archivo HTML y JSON.
    """
    # Renderizar el contenido del correo
    html_content = render_template(template_name, variables, language)

    # Guardar el registro del correo
    save_email_record(
        recipient=recipient,
        subject=subject,
        html_content=html_content,
        variables=variables,
        language=language,
        mode="test" if test_mode else "real"
    )

    if test_mode:
        return  # No envía el correo en modo prueba


    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = recipient
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, recipient, msg.as_string())
