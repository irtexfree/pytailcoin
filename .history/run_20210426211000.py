import threaded
import service
from app import app, bot, socketio
from flask_cors import CORS

CORS(app)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':

    @threaded.ThreadPooled
    def polling():
        bot.polling()

    polling()

    socketio.run(app)

# app.run(threaded=True, debug=True, port=5003)
