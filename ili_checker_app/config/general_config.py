import os
from dotenv import load_dotenv

load_dotenv()

FORMATS_SUPPORTED = ['application/zip', 'application/xtf']

# Keys Email
EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_SUBJECT = "Prueba de correo con adjunto"
SMTP = 'smtp-mail.outlook.com'
PORT = 587

# Storage
STORAGE_DIR = os.environ.get('STORAGE_DIR', "./local_storage")

# Create users
NAME_SU = os.environ.get('NAME_SU')
EMAIL_SU = os.environ.get('EMAIL_SU')
PASSWORD_SU = os.environ.get('PASSWORD_SU')

# Response consults SQL
TAG_RESPONSE_SQL = os.environ.get('TAG_RESPONSE_SQL', "total")

# Quality rules tags
QR_NAME = 'nombre'
QR_DESCRIPTION = 'descripcion'
QR_RESULT = 'resultado'
QR_ERROR = 'error'

# Paths Logos
NAME_LOGO_POSITION_LEFT = "logo_swisstierras.png"
NAME_LOGO_POSITION_RIGHT = "logo_ceicol.png"
