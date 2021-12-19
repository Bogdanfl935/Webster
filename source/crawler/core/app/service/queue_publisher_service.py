from app.config.queue_config import channel, AMQP_QUEUE
from app.dto.queue_dto import ParserTaskDto


def dispatch_message(authenticated_user, content):
    message_content = ParserTaskDto(authenticated_user, content)
    channel.basic_publish(exchange='', routing_key=AMQP_QUEUE, body=message_content)
