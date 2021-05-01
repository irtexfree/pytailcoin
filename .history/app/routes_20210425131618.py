from flask import render_template, request, redirect, make_response
from app import app, sql, bot
import secrets

app.secret_key = 'any random string';

@app.route('/api/login', methods=["POST"])
def api_login():
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()

    for i in query:
        if i['login'] == request.form['login'] and i['password'] == request.form['password']:
            resp = make_response(redirect("/", code=302))
            resp.set_cookie('login', request.form['login'])

            return resp

    resp = make_response(redirect("/login?error=password-not-valid", code=302))

    return resp

@app.route('/api/signup', methods=["POST"])
def api_signup():
    sql.Person(login=request.form['login'], password=request.form['password']).save()
    return redirect("/", code=302)

@app.route('/api/telegram/sendMessage/<chat_id>/<text>', methods=["GET"])
def sendMessage(chat_id, text):
    return {"sent": True, "chat_id": chat_id} if bot.send_message(chat_id, text) else {"sent": False, "chat_id": chat_id}

@app.route('/api/telegram/chat/<chat_id>', methods=["GET"])
def chat(chat_id):
    chat = []
    query = sql.Dialog.select().where(sql.Dialog.chat_id == chat_id).dicts().execute()

    for i in query:
        chat.append(i)

    return {
        "chat_id": chat_id,
        "chat": chat
    }

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@app.route('/login')
def route_login():
    return render_template('login.html', title='Вход в систему')

@app.route('/signup')
def route_signup():
    return render_template('signup.html', title='Регистрация в системе')

@app.route('/')
def route_dashboard():
    if 'login' in request.cookies:
        return render_template('dashboard.html', title='Рабочая область', login=request.cookies['login'])
    else:
        return redirect("/login", code=302)