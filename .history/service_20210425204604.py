from lbcapi import api

conn = api.hmac("hmac_key", "hmac_secret")
conn.call('GET', '/api/myself/').json()