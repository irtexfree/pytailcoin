from app import socketio, sql, bot
from flask_socketio import send, emit

@socketio.on('stream_pending_support')
def handle_stream_pending_support(json):
    users = []
    query = sql.Customer.select().where(((sql.Customer.link == json['user']))).dicts().execute()

    for i in query:
        users.append(i)

    if users:
        emit('stream_linked_support', {
            "user": users[0]
        })
        
        return;
    
    users = []
    query = sql.Customer.select().where(((sql.Customer.link == '~') & ~(sql.Customer.link == json['user']))).dicts().execute()

    for i in query:
        users.append(i)

    # Auto-link customer with operator
    if users != []:        
        sql.Customer.update({sql.Customer.link: json['user']}).where(sql.Customer.chat_id == users[0]['chat_id']).execute()
        bot.send_message(users[0]['chat_id'], 'Оператор на связи! Вы можете начать диалог с ним прямо сейчас')
        
        emit('stream_linked_support', {
            "user": users[0]
        })
            
    
@socketio.on('stream_chat')
def handle_stream_chat(json):    
    chat = []
    query = sql.Dialog.select().where(sql.Dialog.chat_id == json['chat_id']).dicts().execute()

    for i in query:
        chat.append(i)

    emit('stream_chat', {
        "chat_id": json['chat_id'],
        "chat": chat
    })
    
    
@socketio.on('stream_send_message')
def handle_stream_send_message(json):
    print(json)