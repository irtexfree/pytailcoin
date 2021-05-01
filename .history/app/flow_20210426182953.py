from app import bot, sql

@bot.message_handler(commands=['start', 'home'])
def home(message):
	bot.reply_to(message, "Добро пожаловать в обменник Tailcoin. Чтобы вызвать оператора, введите /operator")

@bot.message_handler(commands=['operator'])
def operator(message):
	sql.Customer.insert(chat_id=message.from_user.id, first_name=message.from_user.first_name, want_help='yes', link="~").on_conflict('replace').execute()
	bot.reply_to(message, "Ожидайте! Скоро с вами свяжется наш оператор")

@bot.message_handler(commands=['operator'])
def operator(message):
	sql.Customer.insert(chat_id=message.from_user.id, first_name=message.from_user.first_name, want_help='yes', link="~").on_conflict('replace').execute()
	bot.reply_to(message, "Ожидайте! Скоро с вами свяжется наш оператор")

@bot.message_handler(content_types=['text'])
def flow(message):
	sql.Dialog(text=message.text, chat_id=message.from_user.id, first_name=message.from_user.first_name, time=-1, sender=f"customer:{message.from_user.id}").save()