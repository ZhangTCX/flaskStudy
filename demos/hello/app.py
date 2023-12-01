from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'

@app.route('/hi')
@app.route('/hello')
def sqy_hello():
    return '<h1>Hi Flask!</h1>'

@app.route('/greet', defaults={'name':'游客'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello %s!</h1>'%name
