from marshmallow import Schema, fields, ValidationError, validates, post_load, INCLUDE
from flask import request, abort
from app.config.app_config import flask_app
from functools import wraps
from itertools import chain


def validate_schema(schema):
    def validate_schema_inner(wrapped_function):
        @wraps(wrapped_function)
        def inside_func(*args, **kwargs):
            try:
                result = schema().load(request.json, unknown=INCLUDE)
            except ValidationError as e:
                error_nested_list = ([dict(fieldName=key, errorMessage=message) for message in e.messages[key]] for key
                                     in e.messages)
                error_list = list(chain.from_iterable(error_nested_list))
                abort(400, error_list)

            return wrapped_function(*args, **kwargs)

        return inside_func

    return validate_schema_inner
