from flask import request
import logging
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, close_room
import json
from server.server import app, r
from datetime import datetime
from server.listener import Listener
from util.client import TelleClient


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


'''
room map format: 
{
room_key: {user: [session_id], bot: [session_id], admin: [session_id], muted: True}
}
'''

client = TelleClient(r)


@app.route('/hello')
def hello():
    r.publish('redis_test', json.dumps({'type': 'UPDATE_MESSAGE', 'sid': '123', 'message': 'test message', 'tag': 'bot'}))
    return 'hello world haha'


@socketio.on('connect')
def handle_connect():
    print('Client: {} connected. Rooms: {}'.format(request.sid, rooms()))
    logger.info('Client: {} connected. Rooms: {}'.format(request.sid, rooms()))
    emit('ON_CONNECTION', 'you have connected..........')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client: {} disconnected'.format(request.sid))
    logger.info('Client: {} disconnected'.format(request.sid))

    # close room
    sid = request.sid
    # Allow multiple users in the same room: mimic open multiple pages

    # Delete key in redis
    room = client.delete_user_from_user_map(client_id=sid)

    if 'room_id' in room and 'dealer_id' in room:
        close = client.delete_user_from_room_map(room['room_id'], room['dealer_id'], sid)

        dealer_id = room['dealer_id']
        room_id = room['room_id']

        if close:
            chat_data = json.dumps({'type': 'UPDATE_CHAT',
                                    'dealerId': dealer_id,
                                    'groupId': room_id,
                                    'user': 'customer',
                                    'online': False,
                                    'timestamp': str(datetime.utcnow())
                                    })
            r.publish('telle_ai_chat', chat_data)
            r.rpush('telle:queue:daemon', chat_data)
            r.rpush('telle:queue:bot', chat_data)

            close_room(room)


@socketio.on('client_join')
def customer_join(message):
    # print(message)
    print('Received message from: {}, content: {}'.format(request.sid, message))
    logger.info('Received message from: {}, content: {}'.format(request.sid, message))
    data = json.loads(message)
    room = data['groupId']
    dealer_id = data.get('dealerId', '201978945124789')

    flag = client.update_user_to_room_map(room, dealer_id, client_id=request.sid)

    client.update_user_to_user_map(room_id=room, dealer_id=dealer_id, client_id=request.sid)

    print(room)

    join_room(room)

    if flag:
        group_data = json.dumps({'type': 'UPDATE_GROUP',
                                 'dealerId': dealer_id,
                                 'groupId': room,
                                 'user': 'customer',
                                 'online': True,
                                 'timestamp': str(datetime.utcnow())
                                 })

        r.publish('telle_ai_chat', group_data)

        r.rpush('telle:queue:daemon', group_data)

    chat_data = json.dumps({'type': 'UPDATE_CHAT',
                            'dealerId': dealer_id,
                            'groupId': room,
                            'user': 'customer',
                            'online': True,
                            'timestamp': str(datetime.utcnow())
                            })

    r.publish('telle_ai_chat', chat_data)

    r.rpush('telle:queue:daemon', chat_data)
    #
    # r.publish('telle_ai_chat', json.dumps({
    #     'type': 'UPDATE_CHAT',
    #     'dealerId': dealer_id,
    #     'groupId': room,
    #     'online': True,
    #     'muted': False,
    #     'timestamp': str(datetime.utcnow())
    # }))


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)


@socketio.on('customer_message')
def handle_customer_message(message):
    '''
    :param message:
    :return:
    '''
    message = json.loads(message)
    print('Received Message from customer: {}, message: {}'.format(request.sid, message))

    logger.info('Received Message from customer: {}, message: {}'.format(request.sid, message))
    # to_room_id = message['groupId']
    #
    # if 'dealerId' not in message:
    #     dealer_id = '201978945124789'
    #     message['dealerId'] = '201978945124789'
    # else:
    #     dealer_id = message['dealerId']
    #
    # room_key = '{0}_{1}_{2}'.format(dealer_id, to_room_id, 'room_map')
    # room_map = client.redis.get(room_key)

    # message['message']['author'] = 'user'
    # message['type'] = 'UPDATE_MESSAGE'
    # message['muted'] = room_map.get('muted', False)
    # message['timestamp'] = str(datetime.utcnow())

    message['timestamp'] = str(datetime.utcnow())

    r.publish('telle_ai_chat', json.dumps(message))
    r.rpush('telle:queue:bot', json.dumps(message))
    r.rpush('telle:queue:daemon', json.dumps(message))
    # emit('CHAT_MESSAGE', json.dumps(message), room=to_room_id)


if __name__ == '__main__':
    client_listener = Listener(r, ['telle_ai_chat'], app)
    client_listener.start()
    socketio.run(app=app, host='0.0.0.0', port=5000, debug=True)
