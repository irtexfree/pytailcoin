from app import socketio, sql, bot
from flask_socketio import send, emit
import secrets

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
    sql.Dialog(text=json['text'], chat_id=json['chat_id'], first_name=json['user'], time=-1, sender=f"admin:{json['user']}").save()
    
    emit('stream_send_message', {
        "chat_id": json['chat_id'],
        "sent": True if bot.send_message(json['chat_id'], json['text']) else False
    })
    
    
@socketio.on('stream_close_chat')
def handle_stream_close_chat(json):
    sql.Customer.update({sql.Customer.link: "!"}).where(sql.Customer.chat_id == json['chat_id']).execute()
    bot.send_message(json['chat_id'], 'Вы завершили диалог с оператором')
    
    emit('stream_close_chat', {
        "chat_id": json['chat_id'],
    })
    
@socketio.on('stream_wallets')
def handle_stream_wallets(json):
    users = []
    wallets = []
    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (sql.Person.PASSPORT_SECRET== json['passport']['secret_key'])).dicts().execute()
    
    for user in query:
        users.append(user)
    
    if users:
        query = sql.Wallet.select().dicts().execute()
        
        for wallet in query:
            wallets.append(wallet)
            
        emit('stream_wallets', {
            "wallets": wallets,
        })
    
    
@socketio.on('stream_create_wallet')
def handle_stream_create_wallet(json):
    users = []
    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (sql.Person.PASSPORT_SECRET== json['passport']['secret_key'])).dicts().execute()
    
    for user in query:
        users.append(user)
    
    if users:
        id = secrets.token_urlsafe(6);
        
        sql.Wallet.insert(
            id = id, 
            currency = json['form']['currency'], 
            value= json['form']['value'], 
            address = json['form']['address'], 
            name= json['form']["name"]
        ).execute()
        
        emit('stream_create_wallet', {
            "id": id,
            "name":  json['form']["name"]
        })




@socketio.on('stream_localbitcoins_history')
def handle_stream_localbitcoins_history(json):
    users = []
    ads = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (sql.Person.PASSPORT_SECRET== json['passport']['secret_key'])).dicts().execute()    
    
    for user in query:
        users.append(user)
    
    if users:

        query = sql.Adventure.select().order_by(sql.Adventure.id.desc()).limit(int(3)).dicts().execute()
        
        for i in query:
            ads.append(i)
        

        emit('stream_localbitcoins_history', {
            'history': ads
        })




