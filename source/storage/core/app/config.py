from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import AutoConfig
from app.constants import sql_ddl_constants

app = Flask(__name__)

config = AutoConfig(search_path='../../init/.env')

MY_USER = config('MY_USER')
MY_PASSWORD = config('MY_PASSWORD')
MY_HOST = config('MY_HOST')
MY_PORT = config('MY_PORT')

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{MY_USER}:{MY_PASSWORD}@{MY_HOST}:{MY_PORT}/{MY_USER}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config[""]
db = SQLAlchemy(app)


class ParsedUrls(db.Model):
    __tablename__ = sql_ddl_constants.NEXT_LINKS

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2083), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.url

class VisitedUrls(db.Model):
    __tablename__ = sql_ddl_constants.VISITED_LINKS

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2083), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.url

class Configuration(db.Model):
    __tablename__ = sql_ddl_constants.CONFIGURATION

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(16), nullable=False)
    value = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.key

class ParsedContent(db.Model):
    __tablename__ = sql_ddl_constants.PARSED_CONTENT

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    tag = db.Column(db.String(32), nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.content

class ParsedImages(db.Model):
    __tablename__ = sql_ddl_constants.PARSED_IMAGES

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    extension = db.Column(db.String(16), nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.content