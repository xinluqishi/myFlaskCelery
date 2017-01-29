# coding=utf-8
import sys
from flask import Flask, make_response
from flask import render_template
from flask import session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
# 程序实例传入构造方法进行初始化
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def home():
    return '<h1>Hello World!</h1>'


@app.route('/index')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user', methods=['GET', 'POST'])
def user():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        # session['name'] = form.name.data
        # form.name.data = ''
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('user'))
    return render_template('user.html', form=form, name=session.get('name'))


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


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])  # Should use DataRequired in WTF3.0 now it's 2.1
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run(debug=True)
