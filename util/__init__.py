from .redis_msg_handler import *

handler = {
    'MUTE_BOT': mute_bot,
    'UNMUTE_BOT': unmute_bot,
    'CLOSE_CHAT': close_chat,
    'UPDATE_MSG': update_msg
}
