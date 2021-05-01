from app import bot, sql
from telebot import types

@bot.message_handler(commands=['start', 'home'])
def home(message):
	markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	markup.add(
     	types.KeyboardButton('Создать заявку на обмен'),
     	types.KeyboardButton('Оператор')
    )

	bot.reply_to(message, "Добро пожаловать в обменник Tailcoin!. Чтобы вызвать оператора, введите /operator",  reply_markup=markup)

@bot.message_handler(regexp="Оператор")
def operator(message):
	sql.Customer.insert(chat_id=message.from_user.id, first_name=message.from_user.first_name, want_help='yes', link="~").on_conflict('replace').execute()
	bot.reply_to(message, "Ожидайте! Скоро с вами свяжется наш оператор")

@bot.message_handler(content_types=['text'])
def flow(message):
	sql.Dialog(text=message.text, chat_id=message.from_user.id, first_name=message.from_user.first_name, time=-1, sender=f"customer:{message.from_user.id}").save()