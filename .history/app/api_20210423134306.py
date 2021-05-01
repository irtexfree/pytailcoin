from app import app
from sqlobject import *

@app.route('/api/login', methods=["POST"])
def login():
    return request.form;