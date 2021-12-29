from flask import Flask
from decouple import AutoConfig
from app.parser_controller import parser
from app.crawler_controller import crawler
from app.config.persistence_config import db

flask_app = Flask(__name__)

config = AutoConfig(search_path='../init/.env')

DB_USERNAME = config('DB_USERNAME')
DB_PASSWORD = config('DB_PASSWORD')
DB_DATABASE = config('DB_DATABASE')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
db.init_app(flask_app)

blueprints = (parser, crawler)
for blueprint in blueprints:
    flask_app.register_blueprint(blueprint)
