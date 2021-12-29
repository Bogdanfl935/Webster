from decouple import AutoConfig
import pika


config = AutoConfig(search_path='../init/.env')

AMQP_USERNAME = config("AMQP_USERNAME")
AMQP_PASSWORD = config("AMQP_PASSWORD")
AMQP_HOST = config("AMQP_HOST")
AMQP_PORT = config("AMQP_PORT")
AMQP_QUEUE = config("AMQP_QUEUE")


__credentials = pika.PlainCredentials(AMQP_USERNAME, AMQP_PASSWORD)
__parameters = pika.ConnectionParameters(AMQP_HOST, AMQP_PORT, '/', __credentials)
amqp_connection = pika.BlockingConnection(__parameters)

channel = amqp_connection.channel()
channel.queue_declare(queue=AMQP_QUEUE)