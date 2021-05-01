from app import socketio, sql
from flask_socketio import send, emit

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('stream_pending_support')
def handle_stream_pending_support(json):
    # emit('stream_chat', {"chat": [], "chatId": 0})
    
    users = []
    query = sql.Customer.select().where(sql.Customer.want_help == 'yes').dicts().execute()

    for i in query:
        users.append(i)

    return {
        "users": users
    }