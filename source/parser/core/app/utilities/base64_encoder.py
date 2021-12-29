from app.constants import parsing_constants
import base64

def binary_to_base64_string(target: bytes):
    return base64.b64encode(target).decode(encoding=parsing_constants.ENCODING, errors="replace")