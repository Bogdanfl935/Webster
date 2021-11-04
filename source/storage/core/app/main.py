from flask import Flask, json, jsonify, request
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://user:password@localhost:5432/user"
# app.config[""]
db = SQLAlchemy(app)


class NextLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(2083), nullable=False)

    print(id)

    def __repr__(self):
        return '<Category %r>' % self.url_site

class VisitedLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(2083), nullable=False)

    print(id)

    def __repr__(self):
        return '<Category %r>' % self.url_site

# users = User.query.all()
    
@app.route("/storage", methods=['POST'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)