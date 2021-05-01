from app import bot

@bot.message_handler(content_types=['text'])
def function_name(message):
	bot.reply_to(message, "This is a message handler")
