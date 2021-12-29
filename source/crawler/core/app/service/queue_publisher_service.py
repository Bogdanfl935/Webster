from app.config.queue_config import channel, AMQP_QUEUE
from app.constants import serialization_constants
import json

def dispatch_message(authenticated_user: str, content: str, page_url: str):
    message_content = {serialization_constants.USERNAME_KEY: authenticated_user,
                       serialization_constants.CONTENT_KEY: content,
                       serialization_constants.URL_KEY: page_url}
    channel.basic_publish(exchange='', routing_key=AMQP_QUEUE, body=json.dumps(message_content))
