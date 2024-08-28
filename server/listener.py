import threading
import logging
import json
from util import handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listener(threading.Thread):
    def __init__(self, r, channels, app):
        threading.Thread.__init__(self)
        self.daemon = True
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)
        self.app = app

    def work(self, item):
        with self.app.app_context():
            if isinstance(item['data'], bytes):
                try:
                    msg = item['data'].decode('utf-8')
                    decode_msg = json.loads(msg)
                    print(decode_msg)
                    func_name = decode_msg['type']
                    if func_name in handler:
                        handler[func_name](decode_msg)
                    # if decode_msg['type'] == 'UPDATE_MESSAGE':
                    #     if decode_msg['tag'] == 'bot':
                    #         emit('CHAT_MESSAGE', json.dumps(decode_msg), room=decode_msg['sid'], namespace='/')
                except ValueError as e:
                    raise ValueError("Error decoding msg to microservice: %s", str(e))

    def run(self):
        for item in self.pubsub.listen():
            try:
                # print(item)
                self.work(item)
            except ValueError as e:
                print(e)
                continue
