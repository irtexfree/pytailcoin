from app import bot, sql

@bot.message_handler(content_types=['text'])
def function_name(message):
	print(message)
	sql.Dialog(text=message.text).save()