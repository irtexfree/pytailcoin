from flask import Flask
from flask_socketio import SocketIO
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import telebot

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
app.debug = True
app.secret_key = 'any random string';

socketio = SocketIO(app)

bot = telebot.TeleBot(
    "1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-Ao5so4", parse_mode="MARKDOWN")

from app import routes
from app import socket
from app import flow
