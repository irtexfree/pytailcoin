from lbcapi import api

conn = api.hmac("hmac_key", "hmac_secret")
print(conn.call('GET', '/buy-bitcoins-online/.json').json())