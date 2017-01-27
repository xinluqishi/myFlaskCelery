# coding=utf-8
import sys
from flask import Flask, make_response, redirect
from flask import render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)  #程序实例传入构造方法进行初始化


@app.route('/')
def home():
    return '<h1>Hello World!</h1>'


@app.route('/index')
def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
