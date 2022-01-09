from flask import Flask
from app.config.env_config import DB_USERNAME, DB_PASSWORD, DB_CONTAINER_NAME, DB_PORT, DB_DATABASE
from app.config.persistence_config import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_CONTAINER_NAME}:{DB_PORT}/{DB_DATABASE}"
db.init_app(app)