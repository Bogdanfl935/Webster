from flask import Flask
from app.parser_controller import parser
from app.crawler_controller import crawler
from app.config.persistence_config import db
from app.config.env_config import DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_CONTAINER_NAME, DB_PORT

flask_app = Flask(__name__)

flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_CONTAINER_NAME}:{DB_PORT}/{DB_DATABASE}"
db.init_app(flask_app)

blueprints = (parser, crawler)
for blueprint in blueprints:
    flask_app.register_blueprint(blueprint)
