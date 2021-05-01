from flask import render_template, request, redirect, make_response
from app import app, sql

@app.route('/api/login', methods=["POST"])
def login():
    # sql.Person(login=request.form['login'], password=request.form['password']).save()
    
    query = sql.Person.select().where(sql.Person.login == request.form['login']).dicts().execute()

    for i in query:
        if i['login'] == request.form['login'] and i['password'] == request.form['password']:
            resp = make_response(redirect("/?contine=login", code=302))
            resp.set_cookie('login', request.form['login'])
            resp.set_cookie('password', request.form['password'])

            return resp

    resp = make_response(redirect("/?error=password-not-valid", code=302))

    return resp

@app.route('/', methods=['POST', 'GET'])
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Домашний экран', user=user, posts=posts)

