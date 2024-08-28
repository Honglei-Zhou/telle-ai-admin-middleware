from flask import Flask
from server.config import redis_host, redis_port
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import redis

path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

r = redis.Redis(host=redis_host, port=redis_port)
