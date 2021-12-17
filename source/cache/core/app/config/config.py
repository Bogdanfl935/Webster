from flask import Flask, jsonify, request
from decouple import AutoConfig
import constants
import redis

app = Flask(__name__)

config = AutoConfig(search_path='../../init/.env')

REDIS_PASSWORD = config('REDIS_PASSWORD')
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')

redis_mem_capacity = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=1)

schema = {
    "type": "object",
    "properties": {
        constants.START_LINK_KEY: {"type": "string",
                                   "format": "uri"}
    },
    "required": [constants.START_LINK_KEY]
}