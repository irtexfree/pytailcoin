from flask import render_template, request, redirect, make_response
from app import app, sql
import secrets

app.secret_key = 'any random string';

@app.route('/api/login', methods=["POST"])
def api_login():
    # sql.Person(login=request.form['login'], password=request.form['password']).save()
    
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()

    for i in query:
        if i['login'] == request.form['login'] and i['password'] == request.form['password']:
            resp = make_response(redirect("/", code=302))
            resp.set_cookie('login', request.form['login'])

            return resp

    resp = make_response(redirect("/login?error=password-not-valid", code=302))

    return resp

@app.route('/api/signup', methods=["POST"])
def api_login():
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()
    return redirect("/", code=302)


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
    
