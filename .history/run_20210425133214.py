import threaded
from app import app, bot

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
from flask.ext.cors import CORS, cross_origin
@threaded.ThreadPooled
def polling():
    bot.polling()

polling()
app.run(threaded=True, debug=True, port=5002)
