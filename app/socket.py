import os
import pydash
import secrets

from json import loads, dumps
from app import socketio, sql, bot
from flask_socketio import emit

from app.flow import service_message
from app.notification import notification_emitter
from app.toast import toast_emitter
from run import Config

from service.binance import get_all_tickers
from service.lbapi import payment_methods, chat, chat_send, cancel

q_toasts = []
q_notifications = []

@notification_emitter.on('create')
def handle_emit_notification_create(json):
    global q_notifications

    q_notifications.append(json)

@toast_emitter.on('create')
def handle_emit_toast_create(json):
    global q_toasts

    q_toasts.append(json)


@socketio.on('stream_toastnotify_transfer')
def handle_stream_toastnotify_transfer(json):
    global q_toasts
    global q_notifications

    for json in q_notifications:
        emit("emit_new_notification", {
            "hash": secrets.token_urlsafe(12),
            "title": json.get('title', "Без заголовка"),
            "text": json.get('text', "Без текста")
        }, broadcast=True)

    for json in q_toasts:
        emit("emit_new_toast", {
            "hash": secrets.token_urlsafe(12),
            "title": json.get('title', "Без заголовка"),
            "text": json.get('text', "Без текста")
        }, broadcast=True)

    q_toasts = []
    q_notifications = []


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

        return

    users = []
    query = sql.Customer.select().where(
        ((sql.Customer.link == '~') & ~(sql.Customer.link == json['user']))).dicts().execute()

    for i in query:
        users.append(i)

    # Auto-link customer with operator
    if users != []:
        sql.Customer.update({sql.Customer.link: json['user']}).where(
            sql.Customer.chat_id == users[0]['chat_id']).execute()
        bot.send_message(users[0]['chat_id'], 'Оператор на связи! Вы можете начать диалог с ним прямо сейчас')

        service_message(f'Чат с клиентом {users[0]["first_name"]} назначен оператору @{json["user"]}', users[0]['chat_id'])

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
    sql.Dialog(text=json['text'], chat_id=json['chat_id'], first_name=json['user'], time=-1,
               sender=f"admin:{json['user']}").save()

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
    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

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
    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        id = secrets.token_urlsafe(6);

        sql.Wallet.insert(
            id=id,
            currency=json['form']['currency'],
            value=json['form']['value'],
            address=json['form']['address'],
            name=json['form']["name"]
        ).execute()

        emit('stream_create_wallet', {
            "id": id,
            "name": json['form']["name"]
        })


@socketio.on('stream_integrate_binance_auth')
def handle_stream_integrate_binance_auth(json):
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        Config.set("integrate-account-binance", 'api_key', json['form'].get('apikey'))
        Config.set("integrate-account-binance", 'api_secret', json['form'].get('apisecret'))

        with open('config.ini', 'w') as configfile:
            Config.write(configfile)

        emit('stream_request_reboot', {
            'message': "Недавно вы обновили системные параметры аккаунта Binance и сейчас вам необходимо перезапустить програмное обеспечение"
        })


@socketio.on('stream_integrate_lb_auth')
def handle_stream_integrate_lb_auth(json):
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        Config.set("integrate-account-lb", 'hapi_key', json['form'].get('hapikey'))
        Config.set("integrate-account-lb", 'hapi_secret', json['form'].get('hapisecret'))

        with open('config.ini', 'w') as configfile:
            Config.write(configfile)

        emit('stream_request_reboot', {
            'message': "Недавно вы обновили системные параметры аккаунта LocalBitсoins и сейчас вам необходимо перезапустить програмное обеспечение"
        })


@socketio.on('stream_accept_reboot')
def handle_stream_accept_reboot(json):
    print("Принят запрос на перезапуск ПО")
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        emit('stream_rebooted', {})
        print("Принудительная остановка процесса", os.getpid())
        os.kill(os.getpid(), 9)


@socketio.on('stream_localbitcoins_history')
def handle_stream_localbitcoins_history(json):
    users = []
    ads = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:

        query = sql.Adventure.select().dicts().execute()

        for i in reversed(query[-9:]):
            ads.append(i)

        emit('stream_localbitcoins_history', {
            'history': ads
        })

@socketio.on('stream_localbitcoins_orders')
def handle_stream_localbitcoins_orders(json):
    users = []
    ads = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:

        query = sql.ConfirmAdventure.select().order_by(sql.ConfirmAdventure.status.asc()).limit(int(8)).dicts().execute()

        for i in query:
            ads.append(i)

        emit('stream_localbitcoins_orders', {
            'orders': ads
        })

@socketio.on('stream_binance_price')
def handle_stream_binance_price(json):
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        tickers = get_all_tickers()

        emit('stream_binance_price', {
            'symbol': 'BTCRUB',
            'price': float(pydash.find(tickers, {'symbol': 'BTCRUB'}).get('price', -1))
        })

        emit('stream_binance_price', {
            'symbol': 'USDTRUB',
            'price': float(pydash.find(tickers, {'symbol': 'USDTRUB'}).get('price', -1))
        })

        emit('stream_binance_price', {
            'symbol': 'ETHRUB',
            'price': float(pydash.find(tickers, {'symbol': 'ETHRUB'}).get('price', -1))
        })

        emit('stream_binance_price', {
            'symbol': 'LTCRUB',
            'price': float(pydash.find(tickers, {'symbol': 'LTCRUB'}).get('price', -1))
        })


@socketio.on('stream_payment_methods')
def handle_stream_payment_methods(json):
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        methods = payment_methods()

        emit('stream_payment_methods', {
            "methods": methods
        })


@socketio.on('stream_lb_chat')
def handle_stream_lb_chat(json):
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        if 'form' in json:
            chat_history = chat(json['form']['contact_id']).get("data", {}).get('message_list', [])

            emit('stream_lb_chat', {
                "contact_id": json['form']['contact_id'],
                "chat_history": chat_history
            })


@socketio.on('stream_lb_chat_send')
def handle_stream_lb_chat_send(json):
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        if 'form' in json:
            sended = chat_send(json['form']['contact_id'], json['form']['msg'])
            chat_history = chat(json['form']['contact_id']).get("data", {}).get('message_list', [])

            emit('stream_lb_chat', {
                "contact_id": json['form']['contact_id'],
                "chat_history": chat_history,
                "sended": sended
            })


@socketio.on('stream_lb_cancel_order')
def handle_stream_lb_cancel_order(json):
    users = []
    ads = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        if 'form' in json:
            msg = cancel(json['form']['contact_id']).get('data', {}).get('message', '')

            if not msg:
                sql.ConfirmAdventure.update({sql.ConfirmAdventure.status: 'error'}).where(
                    sql.ConfirmAdventure.contact_id == json['form']['contact_id']).execute()

            if msg == 'Contact canceled.':

                sql.ConfirmAdventure.update({sql.ConfirmAdventure.status: 'canceled'}).where(
                    sql.ConfirmAdventure.contact_id == json['form']['contact_id']).execute()

                query = sql.ConfirmAdventure.select().order_by(sql.ConfirmAdventure.status.asc()).limit(
                    int(8)).dicts().execute()

                for i in query:
                    ads.append(i)

                emit('stream_localbitcoins_orders', {
                    'orders': ads
                })




@socketio.on('stream_localbitcoins_update_props')
def handle_stream_localbitcoins_update_props(json):
    users = []

    query = sql.Person.select().where((sql.Person.PASSPORT_ID == json['passport']['id']) & (
            sql.Person.PASSPORT_SECRET == json['passport']['secret_key'])).dicts().execute()

    for user in query:
        users.append(user)

    if users:
        if 'form' in json:

            for key in json['form']['notify']:
                if key == 'payment_methods':
                    Config.set('integrate-account-lb-notify', key, dumps(json['form']['notify'][key]))

                else:
                    Config.set('integrate-account-lb-notify', key, str(json['form']['notify'][key]))

            for key in json['form']['buy']:
                if key == 'payment_methods':
                    Config.set('integrate-account-lb-buy', key, dumps(json['form']['buy'][key]))

                else:
                    Config.set('integrate-account-lb-buy', key, str(json['form']['buy'][key]))


            with open('config.ini', 'w') as configfile:
                Config.write(configfile)

                emit('stream_request_reboot', {
                    'message': "Недавно вы обновили системные параметры Localbitcoins и сейчас вам необходимо перезапустить програмное обеспечение"
                })

        else:

            dict = {"notify": {}, "buy": {}}
            for key in Config.options('integrate-account-lb-notify'):
                if key == 'payment_methods':
                    dict['notify'][key] = loads(Config.get('integrate-account-lb-notify', key))
                else:
                    dict['notify'][key] = Config.get('integrate-account-lb-notify', key)

                    if dict['notify'][key] == "False": dict['notify'][key] = False
                    if dict['notify'][key] == "True": dict['notify'][key] = True

            for key in Config.options('integrate-account-lb-buy'):
                if key == 'payment_methods':
                    dict['buy'][key] = loads(Config.get('integrate-account-lb-buy', key))
                else:
                    dict['buy'][key] = Config.get('integrate-account-lb-buy', key)

                    if dict['buy'][key] == "False": dict['buy'][key] = False
                    if dict['buy'][key] == "True": dict['buy'][key] = True

            emit('stream_localbitcoins_update_props', dict)





