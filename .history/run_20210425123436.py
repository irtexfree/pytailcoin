from app import app

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.bot.polling()

app.run(debug=True, port=5002)