from lbcapi import api
from app import sql
import threading

import requests

x = requests.get('https://localbitcoins.com/buy-bitcoins-online/RUB/.json')

# conn = api.hmac("", "")
# print(conn.call('GET', '/buy-bitcoins-online/.json').json())

for adventure in x.json()['data']['ad_list']:
    print(adventure['data'])
    sql.Adventure.insert(id=adventure['data']['ad_id'], price=adventure['data']['temp_price'], amount=adventure['data']['max_amount_available'],
                  provider=adventure['data']['online_provider'], city=adventure['data']['city'] or "~", url=adventure['actions']['public_view']).on_conflict('replace').execute()
def printit():
  threading.Timer(5.0, printit).start()
  print ("Hello, World!")

printit()