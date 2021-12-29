from app.constants import sql_ddl_constants
from app.config.persistence_config import db
import enum

class UrlState(enum.Enum):
    READY = enum.auto()
    PENDING = enum.auto()
    VISITED = enum.auto()

class User(db.Model):
    __tablename__ = sql_ddl_constants.USER_RECORD

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False)

class ParsedUrl(db.Model):
    __tablename__ = sql_ddl_constants.PARSED_URL

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    url = db.Column(db.String, nullable=False)
    state = db.Column(db.Enum(UrlState), nullable=False)


class ParsedContent(db.Model):
    __tablename__ = sql_ddl_constants.PARSED_CONTENT

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    tag = db.Column(db.String, nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)

class ParsedImage(db.Model):
    __tablename__ = sql_ddl_constants.PARSED_IMAGE

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    extension = db.Column(db.String, nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)

class MemoryLimit(db.Model):
    __tablename__ = sql_ddl_constants.MEMORY_LIMIT

    singleton_key = db.Column(db.Boolean, primary_key=True)
    capacity = db.Column(db.BigInteger, nullable=False)