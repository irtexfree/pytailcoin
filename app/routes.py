from flask import render_template, request, redirect, make_response
from app import app, sql, bot
import secrets


@app.route('/api/login', methods=["POST"])
def api_login():
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()

    for user in query:
        if user['login'] == request.form['login'] and user['password'] == request.form['password']:
            resp = make_response(redirect("/", code=302))
            resp.set_cookie('login', request.form['login'])
            resp.set_cookie('first_name', user['first_name'])
            resp.set_cookie('last_name', user['last_name'])
            resp.set_cookie('PASSPORT_ID', user['PASSPORT_ID'])
            resp.set_cookie('PASSPORT_SECRET', user['PASSPORT_SECRET'])
            
            return resp

    resp = make_response(redirect("/login?error=password-not-valid", code=302))

    return resp

@app.route('/api/signup', methods=["POST"])
def api_signup():
    sql.Person(
        PASSPORT_ID=secrets.token_urlsafe(6), 
        PASSPORT_SECRET=secrets.token_urlsafe(16), 
        
        login=request.form['login'],
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        password=request.form['password']
    ).save()
    return redirect("/", code=302)
    
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
    if 'login' in request.cookies and 'PASSPORT_ID' in request.cookies and 'PASSPORT_SECRET' in request.cookies :
        return render_template('dashboard.html', title='Рабочая область', login=request.cookies['login'])
    else:
        return redirect("/login", code=302)
