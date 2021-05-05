import time
from json import loads

import time
from json import loads

import pydash
from lbcapi3 import api
from money import Money

from app import sql, bot_me
from app.notification import notification_emitter
from app.toast import toast_emitter
from run import Config
from service.binance import get_ticker

conn = False

def get_change(current, previous):
    if current == previous:
        return 0.0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


def connect(key=False, secret=False):
    global conn
    conn = api.hmac(key or Config.get('integrate-account-lb', 'hapi_key'),
                    secret or Config.get('integrate-account-lb', 'hapi_secret'))


def save_ad(ad_id, price, max_amount_available, online_provider, city, public_view):
    sql.Adventure.insert(id=ad_id, price=price,
                         amount=max_amount_available,
                         provider=online_provider, city=city,
                         url=public_view, hash=f"{ad_id}:{price}").on_conflict('replace').execute()


def confirm_ad(ad_id, amount, currency, contact_id, created_at):
    sql.ConfirmAdventure.insert(id=ad_id, amount=amount, status="A-created",
                         currency=currency, contact_id=contact_id, created_at=created_at,hash=f"{ad_id}:{currency}").on_conflict('replace').execute()



def find_ad(ad_id):
    ads = []
    for ad in sql.Adventure.select().where(sql.Adventure.id == ad_id).dicts().execute():
        ads.append(ad)

    return ads


def contact_info(contact_id):
    response = conn.call('GET', f'/api/contact_info/{contact_id}/')
    if response:
        json = response.json()

        return json

    return {}

def chat(contact_id):
    response = conn.call('GET', f'/api/contact_messages/{contact_id}/')
    if response:
        json = response.json()

        return json

    return {}

def chat_send(contact_id, msg):
    response = conn.call('POST', f'/api/contact_message_post/{contact_id}/', params={"msg": msg})
    if response:
        json = response.json()

        return json

    return {}

def cancel(contact_id):
    response = conn.call('POST', f'/api/contact_cancel/{contact_id}/')
    if response:
        json = response.json()

        return json

    return {}

def buy_ad(ad_id, amount, message):
    response = conn.call('POST', f'/api/contact_create/{ad_id}/', params={
        "amount": amount,
        "message": message
    })
    if response:
        json = response.json()

        return json

    return {}


def payment_methods():
    response = conn.call('GET', '/api/payment_methods/')
    if response:
        json = response.json().get('data').get('methods')

        return json

    return {}


def get_ads():
    ads = []
    response = conn.call('GET', '/buy-bitcoins-online/RUB/.json')
    if response:
        json = response.json().get('data').get('ad_list')

        price = get_ticker('BTCRUB').get('lastPrice')

        for ad in json:
            data = ad.get('data')

            ads.append({
                "binance_price": float(price),
                "city": data.get('city'),
                "online_provider": data.get('online_provider'),
                "max_amount_available": data.get('max_amount_available'),
                "ad_id": data.get('ad_id'),
                "temp_price": float(data.get('temp_price')),
                "username": data.get('profile').get('username'),
                "public_view": ad.get('actions').get('public_view')
            })

    return ads


def filter(x, y):
    if (x == True):
        return y


def notify(ad):
    necessary_min = float(Config.get('integrate-account-lb-notify', 'min_percent_min'))
    necessary_max = float(Config.get('integrate-account-lb-notify', 'min_percent_max'))
    chat_id = float(Config.get('integrate-account-lb', 'chat_id'))

    delta = get_change(ad.get('binance_price'), ad.get('temp_price'))

    if necessary_min <= delta <= necessary_max:

        VOLUME = True
        PROVIDER = True

        providers = pydash.compact(
            pydash.map_(loads(Config.get('integrate-account-lb-notify', 'payment_methods')), filter))

        if not Config.get('integrate-account-lb-notify', 'payment_method') == "False" and len(providers) > 0:
            if not ad.get('online_provider') in providers:
                PROVIDER = False

        if not Config.get('integrate-account-lb-notify', 'min_volume') == "False":
            if not float(Config.get('integrate-account-lb-notify', 'min_volume_min')) <= float(
                    ad.get('max_amount_available')) <= float(
                Config.get('integrate-account-lb-notify', 'min_volume_max')):
                VOLUME = False

        if not Config.get('integrate-account-lb-notify', 'get_notifications') == "False" and VOLUME and PROVIDER:

            toast_emitter.emit('create', {
                "title": "Новое объявление",
                "text": f"Отловлено объявление #{ad.get('ad_id')}"
            })

            for id in str(chat_id).split(','):
                bot_me.send_message(id,
                                    f"<b>Новое объявление</b>\n👤 Пользователь: {ad.get('username')}\n💳 Провайдер: {ad.get('online_provider')}\n💵 Стоимость: {Money(amount=ad.get('temp_price'), currency='RUB')}\n💰 Максимальный выкуп: {Money(amount=ad.get('max_amount_available'), currency='RUB')}\n⚖️ Дельта: {round(delta, 2)}\n\n<a href='{ad.get('public_view')}'>Открыть в браузере</a>".strip().rstrip().lstrip())
                time.sleep(2)


def buy(ad):
    necessary_min = float(Config.get('integrate-account-lb-buy', 'min_percent_min'))
    necessary_max = float(Config.get('integrate-account-lb-buy', 'min_percent_max'))
    chat_id = float(Config.get('integrate-account-lb', 'chat_id'))

    delta = get_change(ad.get('binance_price'), ad.get('temp_price'))

    if necessary_min <= delta <= necessary_max:
        VOLUME = True
        PROVIDER = True

        providers = pydash.compact(
            pydash.map_(loads(Config.get('integrate-account-lb-buy', 'payment_methods')), filter))

        if not Config.get('integrate-account-lb-buy', 'payment_method') == "False" and len(providers) > 0:
            if not ad.get('online_provider') in providers:
                PROVIDER = False

        if not Config.get('integrate-account-lb-buy', 'min_volume') == "False":
            if not float(Config.get('integrate-account-lb-buy', 'min_volume_min')) <= float(
                    ad.get('max_amount_available')) <= float(
                Config.get('integrate-account-lb-buy', 'min_volume_max')):
                VOLUME = False

        if not Config.get('integrate-account-lb-buy', 'buy') == "False" and VOLUME and PROVIDER:
            text = Config.get('integrate-account-lb-buy', 'text').replace("{АВТОР}", ad.get('username')).replace(
                "{ОБЪЕМ}", ad.get('max_amount_available'))
            if text:
                contact = buy_ad(ad.get('ad_id'), float(ad.get('max_amount_available')), text)
                if 'data' in contact and 'contact_id' in contact.get('data'):
                    contact = contact.get('data', {}).get('contact_id')
                    info = contact_info(contact)

                    if 'actions' in info:
                        confirm_ad(ad.get('ad_id'), float(info.get('data').get('amount')), info.get('data').get('currency'), info.get('data').get('contact_id'), info.get('data').get('created_at'))
                        print(info.get('actions'))

                    else:
                        toast_emitter.emit("create", {
                            "title": "ОБЪЯВЛЕНИЕ НЕ ВЫКУПЛЕНО",
                            "text": f"Объявление #{ad.get('ad_id')} не было выкуплено"
                        })

                        if not Config.get('integrate-account-lb-buy', 'get_notifications') == "False":
                            for id in str(chat_id).split(','):
                                bot_me.send_message(id,
                                                    f"<b>🛑🛑🛑 НЕ ВЫКУПЛЕНО ОБЪЯВЛЕНИЕ 🛑🛑🛑</b>\n👤 Пользователь: {ad.get('username')}\n💳 Провайдер: {ad.get('online_provider')}\n💵 Стоимость: {Money(amount=ad.get('temp_price'), currency='RUB')}\n💰 Максимальный выкуп: {Money(amount=ad.get('max_amount_available'), currency='RUB')}\n⚖️ Дельта: {round(delta, 2)}\n\n<a href='{ad.get('public_view')}'>Открыть в браузере</a>".strip().rstrip().lstrip())

                else:
                    toast_emitter.emit("create", {
                        "title": "ОБЪЯВЛЕНИЕ НЕ ВЫКУПЛЕНО",
                        "text": f"Объявление #{ad.get('ad_id')} не было выкуплено"
                    })

                    if not Config.get('integrate-account-lb-buy', 'get_notifications') == "False":
                        for id in str(chat_id).split(','):
                            bot_me.send_message(id,
                                                f"<b>🛑🛑🛑 НЕ ВЫКУПЛЕНО ОБЪЯВЛЕНИЕ 🛑🛑🛑</b>\n👤 Пользователь: {ad.get('username')}\n💳 Провайдер: {ad.get('online_provider')}\n💵 Стоимость: {Money(amount=ad.get('temp_price'), currency='RUB')}\n💰 Максимальный выкуп: {Money(amount=ad.get('max_amount_available'), currency='RUB')}\n⚖️ Дельта: {round(delta, 2)}\n\n<a href='{ad.get('public_view')}'>Открыть в браузере</a>".strip().rstrip().lstrip())


        if not Config.get('integrate-account-lb-buy', 'get_notifications') == "False" and VOLUME and PROVIDER:

            if not Config.get('integrate-account-lb-buy', 'buy') == "False":
                notification_emitter.emit('create', {
                    "title": f"Выкуплено объявление #{ad.get('ad_id')}",
                    "text": f"На сумму {Money(amount=ad.get('max_amount_available'), currency='RUB')}"
                })

            else:
                notification_emitter.emit('create', {
                    "title": f"Может быть выкуплено #{ad.get('ad_id')}",
                    "text": f"На сумму {Money(amount=ad.get('max_amount_available'), currency='RUB')}"
                })

            for id in str(chat_id).split(','):
                bot_me.send_message(id,
                                    f"<b>Новый выкуп</b>\n👤 Пользователь: {ad.get('username')}\n💳 Провайдер: {ad.get('online_provider')}\n💵 Стоимость: {Money(amount=ad.get('temp_price'), currency='RUB')}\n💰 Максимальный выкуп: {Money(amount=ad.get('max_amount_available'), currency='RUB')}\n⚖️ Дельта: {round(delta, 2)}\n\n<a href='{ad.get('public_view')}'>Открыть в браузере</a>".strip().rstrip().lstrip())
                time.sleep(2)


def detected(ad):
    buy(ad)
    notify(ad)


def loop():
    connect()

    while True:
        for ad in get_ads():
            storage_ad = find_ad(ad.get('ad_id'))

            if storage_ad:
                storage_ad = storage_ad[0]
                if not float(storage_ad.get('price', 0)) == float(ad.get('temp_price')):
                    detected(ad)
                    save_ad(ad.get('ad_id'), ad.get('temp_price'), ad.get('max_amount_available'),
                            ad.get('online_provider'),
                            ad.get('city') or "По всей стране или онлайн", ad.get('public_view'))

            else:
                detected(ad)
                save_ad(ad.get('ad_id'), ad.get('temp_price'), ad.get('max_amount_available'),
                        ad.get('online_provider'),
                        ad.get('city') or "По всей стране или онлайн", ad.get('public_view'))

        time.sleep(8)


