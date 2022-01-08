from flask import abort, Response
from http import HTTPStatus


def unpack_response(response: Response):
    return_content = dict()
    match response.status_code:
        case HTTPStatus.OK:
            if int(response.headers.get('Content-Length', '0')) > 0:
                return_content = response.json()
        case _:
            abort(response.status_code, response.json())
    return return_content, response.status_code