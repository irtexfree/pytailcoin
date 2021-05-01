from app import socketio, sql
from flask_socketio import send, emit

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('stream_pending_support')
def handle_stream_pending_support(json):    
    users = []
    query = sql.Customer.select().where((sql.Customer.link == '~' & sql.Customer.link != json.user)).dicts().execute()

    for i in query:
        users.append(i)

    # Auto-link customer with operator
    sql.Customer.update({sql.Customer.link: json.user}).where(sql.Customer.chat_id== user[0].caht_id).execute()
    bot.send_message(chat_id, 'Оператор на связи! Вы можете начать диалог с ним прямо сейчас')
    

    # emit('stream_chat', {"chat": [], "chatId": 0})
    emit('stream_request_support', {
        "users": users
    })