from app.constants import sql_ddl_constants
from app.config.persistence_config import db
from sqlalchemy import ForeignKey

class User(db.Model):
    __tablename__ = sql_ddl_constants.USER_RECORD

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False)

class ParserConfiguration(db.Model):
    __tablename__ = sql_ddl_constants.PARSER_CONFIGURATION

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    tag = db.Column(db.String, nullable=False)


class CrawlerOption(db.Model):
    __tablename__ = sql_ddl_constants.CRAWLER_OPTION

    id = db.Column(db.BigInteger, primary_key=True)
    keyword = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

class CrawlerConfiguration(db.Model):
    __tablename__ = sql_ddl_constants.CRAWLER_CONFIGURATION

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    option_id = db.Column(db.BigInteger, ForeignKey(CrawlerOption.id), nullable=False)