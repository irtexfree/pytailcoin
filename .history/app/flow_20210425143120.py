from app import bot, sql

@bot.message_handler(content_types=['text'])
def function_name(message):
	sql.Dialog(text=message.text, chat_id=messamessage.from_user.idge.from_user.id, first_name=message.from_user.first_name, time=-1, sender=f"customer:{message.from_user.id}").save()