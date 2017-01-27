# coding=utf-8
import sys
from flask import Flask, make_response, redirect
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime


app = Flask(__name__)
# 程序实例传入构造方法进行初始化
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def home():
    return '<h1>Hello World!</h1>'


@app.route('/index')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/index_response')
def index_response():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/index_redirect')
def index_redirect():
    return redirect('http://www.example.com')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
