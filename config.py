from dotenv import load_dotenv
import os

# Carga el archivo .env
load_dotenv()

# Leer las variables desde el entorno
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
DEBUG=os.getenv("DEBUG")
DEFAULT_LANGUAGE=os.getenv("DEFAULT_LANGUAGE")