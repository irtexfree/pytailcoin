from flask import render_template, request, redirect, make_response
from app import app, sql, bot
import secrets


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

@app.route('/api/ads/<limit>', methods=["GET"])
def adventures(limit):
    ads = []
    query = sql.Adventure.select().order_by(sql.Adventure.id.desc()).limit(int(limit)).dicts().execute()
    
    for i in query:
        ads.append(i)
    
    return {
        "ads": ads
    }
    
    
@app.route('/api/telegram/sendAction/<chat_id>/<action>', methods=["GET"])
def sendAction(chat_id, action):
    return {"action": action, "chat_id": chat_id} if bot.send_chat_action(chat_id, action) else {"action": False, "chat_id": chat_id}
    
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