import threaded
from app import app, bot

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@threaded.ThreadPooled
def polling():
    bot.polling()

@threaded.ThreadPooled
def polling():
    app.run(debug=True, port=5002)