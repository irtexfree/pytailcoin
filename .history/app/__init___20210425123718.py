from flask import Flask
import telebot

app = Flask(__name__, 
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)

bot = telebot.TeleBot("1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-Ao5so4", parse_mode="MARKDOWN")

from app import routes
from app import bot