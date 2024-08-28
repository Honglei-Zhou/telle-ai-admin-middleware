from flask_socketio import emit
import json


def mute_bot(msg):
    '''
    Push user mute status to chatbot
    :param msg:
    :return:
    '''
    msg['type'] = 'MUTE_STATUS'
    room = msg['groupId']
    emit('MUTE_STATE', json.dumps(msg), room=room, namespace='/')


def unmute_bot(msg):
    '''
    Push user mute status to chatbot
    :param msg:
    :return:
    '''
    msg['type'] = 'MUTE_STATUS'
    room = msg['groupId']
    emit('MUTE_STATE', json.dumps(msg), room=room, namespace='/')


def close_chat(msg):
    '''
    Push user online status to chatbot
    :param msg:
    :return:
    '''
    msg['type'] = 'CLOSE_CHAT'
    room = msg['groupId']
    emit('CLOSE_CHAT', json.dumps(msg), room=room, namespace='/')


def update_msg(msg):
    '''
    Push user/admin/bot msg to chatbot
    :param msg:
    :return:
    '''
    msg['type'] = 'CHAT_MSG'
    room = msg['groupId']
    emit('CHAT_MESSAGE', json.dumps(msg), room=room, namespace='/')


