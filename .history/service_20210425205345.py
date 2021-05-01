from lbcapi import api

conn = api.hmac("", "")
print(conn.call('GET', '/buy-bitcoins-online/.json').json())