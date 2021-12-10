from flask import Flask, jsonify, request
from decouple import AutoConfig
import redis

app = Flask(__name__)

config = AutoConfig(search_path='../../init/.env')

REDIS_PASSWORD = config('REDIS_PASSWORD')
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')

redis_parsed_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=2)