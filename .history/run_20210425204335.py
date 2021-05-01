import threaded
import service
from app import app, bot
from flask_cors import CORS

CORS(app)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@threaded.ThreadPooled
def polling():
    bot.polling()

polling()
app.run(threaded=True, debug=True, port=5003)
