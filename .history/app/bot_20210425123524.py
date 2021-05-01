import telebot

bot = telebot.TeleBot("1769481990:AAG64HR9lYBU11JYflC3C4plU2Yb-Ao5so4", parse_mode="MARKDOWN")

@bot.message_handler(content_types=['text'])
def function_name(message):
	bot.reply_to(message, "This is a message handler")
