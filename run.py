import threading
import configparser
import pretty_errors
from requests import get

from app import app, bot, socketio
from flask_cors import CORS
from termcolor import colored

CORS(app)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

Config = configparser.ConfigParser()
Config.read("config.ini")

if __name__ == '__main__':
    print(colored('Инициализация продукта', 'yellow'))

    print(colored('Загрузка потока Telegram бот', 'yellow'))
    my_thread = threading.Thread(target=bot.polling)
    my_thread.start()

    print(colored('Загрузка потока HTTP сервера Flask', 'yellow'))
    socketio.run(app, host=Config.get("http-server", "host"), port=int(Config.get("http-server", "port")))
