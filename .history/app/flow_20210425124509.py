from app import bot, sql

@bot.message_handler(content_types=['text'])
def function_name(message):
	print(message)
	sql.Dialog(text=message.text, chat_id=message.from_user.id, first_name=message.from_user.first_name, time=-1).save()