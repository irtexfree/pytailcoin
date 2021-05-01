from flask import render_template, request, redirect, make_response
from app import app, sql

@app.route('/api/login', methods=["POST"])
def login():
    sql.Person(login=request.form['login'], password=request.form['password']).save()
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)
   
    return resp

    return redirect("/", code=302)

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

