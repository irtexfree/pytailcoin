from app import sql

import requests
import threading

session = requests.session()
# Tor uses the 9050 port as the default socks port
session.proxies = {'http':  'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'}



def printit():
    threading.Timer(2.0, printit).start()
    x = session.get('https://localbitcoins.com/buy-bitcoins-online/RUB/.json')

    # conn = api.hmac("", "")
    # print(conn.call('GET', '/buy-bitcoins-online/.json').json())

    for adventure in x.json()['data']['ad_list']:
        sql.Adventure.insert(id=adventure['data']['ad_id'], price=adventure['data']['temp_price'], amount=adventure['data']['max_amount_available'],
                    provider=adventure['data']['online_provider'], city=adventure['data']['city'] or "~", url=adventure['actions']['public_view']).on_conflict('replace').execute()


printit()