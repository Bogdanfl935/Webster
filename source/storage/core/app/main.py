from flask import Flask, json, jsonify, request
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import AutoConfig
import endpoint_constants
import app_constants
import sql_ddl_constants


config = AutoConfig(search_path='../../init/.env')

MY_USER = config('MY_USER')
MY_PASSWORD = config('MY_PASSWORD')
MY_HOST = config('MY_HOST')
MY_PORT = config('MY_PORT')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{MY_USER}:{MY_PASSWORD}@{MY_HOST}:{MY_PORT}/{MY_USER}"
# app.config[""]
db = SQLAlchemy(app)


class NextLinks(db.Model):
    __tablename__ = sql_ddl_constants.NEXT_LINKS

    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(2083), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.url_site

class VisitedLinks(db.Model):
    __tablename__ = sql_ddl_constants.VISITED_LINKS

    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(2083), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.url_site

# users = User.query.all()
    
@app.route(endpoint_constants.STORAGE, methods=['POST'])
def handle_storage_post() -> str:
    links = request.get_json()
    json_links = links["links"]

    for link in json_links:
        db.session.add(NextLinks(url_site=link))

    db.session.commit()

    return jsonify({"success": "True"})

@app.route(endpoint_constants.NEXT_LINK, methods=['POST'])
def handle_next_link_post() -> str:
    json_resp = request.get_json('json_resp')

    next_link_db_resp = NextLinks.query.limit(int(json_resp["quantity"])).all()

    dict_next_url = dict()
    dict_next_url["urls"] = []
    for el in next_link_db_resp:
        dict_next_url["urls"].append(el.url_site)

    return dict_next_url

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)