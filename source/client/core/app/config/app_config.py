from flask import Flask
from app.auth import auth
import secrets
import os

STATIC_DIRECTORY_PATH = os.path.join(os.pardir, "static")
TEMPLATES_DIRECTORY_PATH = os.path.join(os.pardir, "templates")

app = Flask(__name__, static_folder=STATIC_DIRECTORY_PATH, template_folder=TEMPLATES_DIRECTORY_PATH)
app.register_blueprint(auth)
app.secret_key = secrets.token_urlsafe(32)