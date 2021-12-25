from flask import Flask
from app.parser_controller import parser
from app.crawler_controller import crawler

flask_app = Flask(__name__)

blueprints = (parser, crawler)
for blueprint in blueprints:
    flask_app.register_blueprint(blueprint)
