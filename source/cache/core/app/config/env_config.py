import os

APP_HOST = os.environ['CACHE_HOST']
APP_PORT = os.environ['CACHE_PORT']

REDIS_CONTAINER_NAME = os.environ['CACHE_REDIS_CONTAINER_NAME']
REDIS_PORT = os.environ['CACHE_REDIS_PORT']
REDIS_PASSWORD = os.environ['CACHE_REDIS_PASSWORD']