from marshmallow import ValidationError, INCLUDE
from flask import request, abort
from functools import wraps
from itertools import chain
from enum import Enum, auto


class ValidationTarget(Enum):
    REQUEST_BODY = auto()
    NAMED_URL_PARAMETERS = auto()


def validate_with_schema(schema, target: ValidationTarget = ValidationTarget.REQUEST_BODY):
    def validate_schema_inner(wrapped_function):
        @wraps(wrapped_function)
        def inside_func(*args, **kwargs):
            try:
                match target:
                    case ValidationTarget.REQUEST_BODY:
                        schema().load(request.json, unknown=INCLUDE)
                    case ValidationTarget.NAMED_URL_PARAMETERS:
                        schema().load(request.args)
            except ValidationError as e:
                error_nested_list = ([dict(fieldName=key, errorMessage=message) for message in e.messages[key]] for key
                                     in e.messages)
                error_list = list(chain.from_iterable(error_nested_list))
                abort(400, error_list)

            return wrapped_function(*args, **kwargs)

        return inside_func

    return validate_schema_inner
