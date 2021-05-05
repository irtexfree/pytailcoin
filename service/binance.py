from run import Config
from binance.client import Client
from cachetools import TTLCache

cache = TTLCache(maxsize=128, ttl=2)
client = Client(Config.get("integrate-account-binance", "api_key"), Config.get("integrate-account-binance", "api_secret"))

def get_all_tickers():
    if 'get_all_tickers' in cache:
        return cache['get_all_tickers']
    else:
        cache['get_all_tickers'] = client.get_all_tickers()
        return cache['get_all_tickers']

def get_ticker(symbol):
    if 'get_ticker' in cache:
        return cache['get_ticker']
    else:
        cache['get_ticker'] = client.get_ticker(symbol=symbol)
        return cache['get_ticker']
