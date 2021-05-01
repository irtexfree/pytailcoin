from flask import Flask
import telebot

app = Flask(__name__, 
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)

bot = telebot.TeleBot("1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-A

from app import routes