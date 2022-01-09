from flask import Flask
from app.auth import auth
from app.nav import nav
from app.activity import activity
from app.configuration import configuration
from app.stats import stats
import secrets
import os

STATIC_DIRECTORY_PATH = os.path.join(os.pardir, "static")
TEMPLATES_DIRECTORY_PATH = os.path.join(os.pardir, "templates")

app = Flask(__name__, static_folder=STATIC_DIRECTORY_PATH, template_folder=TEMPLATES_DIRECTORY_PATH)
app.secret_key = secrets.token_urlsafe(32)

blueprints = (auth, nav, activity, configuration, stats)
for blueprint in blueprints:
    app.register_blueprint(blueprint)

