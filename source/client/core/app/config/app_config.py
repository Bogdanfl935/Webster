from flask import Flask
from app.auth import auth
from app.nav import nav
from app.activity import activity
from app.configuration import configuration
import secrets
import os

STATIC_DIRECTORY_PATH = os.path.join(os.pardir, "static")
TEMPLATES_DIRECTORY_PATH = os.path.join(os.pardir, "templates")

app = Flask(__name__, static_folder=STATIC_DIRECTORY_PATH, template_folder=TEMPLATES_DIRECTORY_PATH)
app.secret_key = secrets.token_urlsafe(32)

blueprints = (auth, nav, activity, configuration)
for blueprint in blueprints:
    app.register_blueprint(blueprint)

