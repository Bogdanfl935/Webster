from flask import Flask
import secrets
import os
from app.config.env_config import DB_USERNAME, DB_PASSWORD, DB_CONTAINER_NAME, DB_PORT, DB_DATABASE
from app.config.persistence_config import db

STATIC_DIRECTORY_PATH = os.path.join(os.pardir, "static")
TEMPLATES_DIRECTORY_PATH = os.path.join(os.pardir, "templates")

app = Flask(__name__, static_folder=STATIC_DIRECTORY_PATH, template_folder=TEMPLATES_DIRECTORY_PATH)
app.secret_key = secrets.token_urlsafe(32)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_CONTAINER_NAME}:{DB_PORT}/{DB_DATABASE}"
db.init_app(app)