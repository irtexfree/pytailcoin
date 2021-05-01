from flask import render_template, request
from app import app, sql

@app.route('/api/login', methods=["POST"])
def login():
    sql.Person(login=request.form['name'], password=request.form['password'])
    return request.form;
    
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

