import configparser

from flask import Flask
from flask_socketio import SocketIO
import telebot

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

app.secret_key = 'any random string'

socketio = SocketIO(app)

ConfigLocal = configparser.ConfigParser()
ConfigLocal.read("config.ini")

bot = telebot.TeleBot(ConfigLocal.get('telegram', 'global'), parse_mode="HTML")
bot_me = telebot.TeleBot(ConfigLocal.get('telegram', 'me'), parse_mode="HTML")

from app import routes
from app import socket
from app import flow
