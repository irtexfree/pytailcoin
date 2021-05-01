from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import telebot

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

sockets = Sockets(app)

bot = telebot.TeleBot(
    "1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-Ao5so4", parse_mode="MARKDOWN")


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message[::-1])


from app import routes
from app import flow

if __name__ == '__main__':
    app.run()
