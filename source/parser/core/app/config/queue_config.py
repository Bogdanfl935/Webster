from app.config.env_config import AMQP_USERNAME, AMQP_PASSWORD, AMQP_CONTAINER_NAME, AMQP_PORT, AMQP_QUEUE
import pika, logging

logging.getLogger("pika").propagate = False

__credentials = pika.PlainCredentials(AMQP_USERNAME, AMQP_PASSWORD)
__parameters = pika.ConnectionParameters(AMQP_CONTAINER_NAME, AMQP_PORT, '/', __credentials)
amqp_connection = pika.BlockingConnection(__parameters)

channel = amqp_connection.channel()
channel.queue_declare(queue=AMQP_QUEUE)