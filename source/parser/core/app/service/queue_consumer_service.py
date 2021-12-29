from app.config.queue_config import channel, amqp_connection
from app.constants import serialization_constants, parsing_constants
from app.service import parsing_service
from app.service.executor_service import executor
import json

def _process_message(*args):
    (_, _, _, body) = args # Unpack only the body content
    serialized_message = json.loads(body.decode(encoding=parsing_constants.ENCODING, errors="replace"))
    authenticated_user = serialized_message.get(serialization_constants.USERNAME_KEY)
    html_content = serialized_message.get(serialization_constants.CONTENT_KEY)
    page_url = serialized_message.get(serialization_constants.URL_KEY)
    executor.submit(lambda: parsing_service.init_parsing(authenticated_user, html_content, page_url))
    

def subscribe(queue: str):
    channel.basic_consume(queue, _process_message, auto_ack=True)
    return executor.submit(lambda: channel.start_consuming())

def shutdown():
    channel.cancel()
    channel.close()
    amqp_connection.close()
