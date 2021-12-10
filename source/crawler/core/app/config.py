from flask import Flask, jsonify, request
from decouple import AutoConfig
import redis

app = Flask(__name__)

config = AutoConfig(search_path='../../init/.env')

MY_PASSWORD = config('MY_PASSWORD')
MY_HOST = config('MY_HOST')
MY_PORT = config('MY_PORT')

redis_mem_capacity = redis.Redis(host=MY_HOST, port=MY_PORT, password=MY_PASSWORD, db=1)