from app import socketio
from flask_socketio import send, emit

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('stream_pending_support')
def handle_stream_pending_support(json):
    print('received json: ' + str(json))
    emit('stream_chat', {})