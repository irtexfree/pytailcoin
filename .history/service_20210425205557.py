from lbcapi import api
import requests

x = requests.get('https://localbitcoins.com/buy-bitcoins-online/.json')

conn = api.hmac("", "")
print(conn.call('GET', '/buy-bitcoins-online/.json').json())