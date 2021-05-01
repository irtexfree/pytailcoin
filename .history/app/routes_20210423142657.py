from flask import render_template, request, redirect, make_response, session
from app import app, sql

@app.route('/api/login', methods=["POST"])
def login():
    # sql.Person(login=request.form['login'], password=request.form['password']).save()
    
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()

    for i in query:
        if i['login'] == request.form['login'] and i['password'] == request.form['password']:
            resp = make_response(redirect("/", code=302))
            resp.set_cookie('login', request.form['login'])
            resp.set_cookie('password', request.form['password'])
            session.pop('loginusername', request.form['login']);
            session.pop('password', request.form['password']);

            return resp

    resp = make_response(redirect("/login?error=password-not-valid", code=302))

    return resp

@app.route('/login')
def index():
    return render_template('index.html', title='Домашний экран')

@app.route('/')
def dashboard():
    print(session)
    return render_template('dashboard.html', title='Рабочая область')

