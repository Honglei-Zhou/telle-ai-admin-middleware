from app import app, socketio
from server.listener import Listener
from server.server import r

if __name__ == '__main__':
    client = Listener(r, ['telle_ai_chat'], app)
    client.start()
    socketio.run(app=app, host='0.0.0.0', port=5000, debug=True)
