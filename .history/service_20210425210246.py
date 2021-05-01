from lbcapi import api
from app import sql

import requests

x = requests.get('https://localbitcoins.com/buy-bitcoins-online/.json')

# conn = api.hmac("", "")
# print(conn.call('GET', '/buy-bitcoins-online/.json').json())

for adventure in x.json()['data']['ad_list']:
    print(adventure['data'])
	sql.Adventure().save()
