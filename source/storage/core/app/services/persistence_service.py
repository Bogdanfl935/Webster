from app.config.persistence_config import db
from flask import abort
import sqlalchemy.exc as persistence_error
from http import HTTPStatus


def add(record: any, commit: bool = False):
    db.session.add(record)
    if commit is True:
        commit_session()


def delete(record: any, commit: bool = False):
    db.session.delete(record)
    if commit is True:
        commit_session()


def commit_session(supress_exceptions: bool = False):
    try:
        db.session.commit()
    except persistence_error.IntegrityError as exception:
        db.session.rollback()
        if supress_exceptions is False:
            abort(HTTPStatus.CONFLICT, exception.orig)


def query(query_func):
    return query_func(db.session)
