from flask import Flask, json, jsonify, request
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import AutoConfig
import endpoint_constants


config = AutoConfig(search_path='../../init/.env')

MY_USER = config('MY_USER')
MY_PASSWORD = config('MY_PASSWORD')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{MY_USER}:{MY_PASSWORD}@localhost:5432/{MY_USER}"
# app.config[""]
db = SQLAlchemy(app)


class NextLinks(db.Model):
    __tablename__ = 'next_links'

    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(2083), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.url_site

class VisitedLinks(db.Model):
    __tablename__ = 'visited_links'

    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(2083), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.url_site

# users = User.query.all()
    
@app.route(endpoint_constants.STORAGE, methods=['POST'])
def in_get_data() -> str:
    # db.session.add(NextLinks(url_site="example.org"))
    # db.session.commit()
    #
    # q = NextLinks.query.all()
    # print(q)
    #
    # nLink = NextLinks()
    # print(nLink)

    return jsonify({"ala": "bala"})

@app.route(endpoint_constants.NEXT_LINK, methods=['POST'])
def in_get_next_links() -> str:
    json_resp = request.get_json('json_resp')

    next_link_db_resp = NextLinks.query.limit(int(json_resp["quantity"])).all()

    dict_next_url = dict()
    dict_next_url["urls"] = []
    for el in next_link_db_resp:
        dict_next_url["urls"].append(el.url_site)

    return dict_next_url

if __name__ == '__main__':
    app.run(host='192.168.100.215', port=80, debug=True)