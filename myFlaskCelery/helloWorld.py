# coding=utf-8
import os
from flask import Flask, make_response
from flask import render_template
from flask import session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell, Manager
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import uuid

# basedir = os.path.abspath(os.path.dirname('/Users/shikeyue/Documents/pythonWorkspace/myFlaskCelery/myFlaskCelery'))
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/parking_car'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
# 程序实例传入构造方法进行初始化
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)


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
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash('Looks like you have changed your name!')
        # session['name'] = form.name.data
        # return redirect(url_for('user'))
        one_user = User.query.filter_by(user_name=form.name.data).first()
        if one_user is None:
            one_user = User(user_id=uuid.uuid4().urn[9:], user_name=form.name.data)
            db.session.add(one_user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('user'))

    return render_template('user.html', form=form, name=session.get('name'), known=session.get('known'))


@app.route('/index_response')
def index_response():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/index_redirect')
def index_redirect():
    return redirect('http://www.example.com')


@app.route('/init_db')
def init_db():
    # db.create_all()
    # print "db create now!"
    # admin_role1 = Role(role_id='001', role_name='Admin1')
    # mod_role = Role(role_id=uuid.uuid4().urn[9:], role_name='Moderator')
    # user_role = Role(role_name='User')
    #
    # user_john = User(user_id=uuid.uuid4().urn[9:], user_name='john', role=admin_role)
    # user_susan = User(user_id=uuid.uuid4().urn[9:], user_name='susan', role=user_role)
    # user_david = User(user_id=uuid.uuid4().urn[9:], user_name='david', role=user_role)
    #
    # db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])
    # db.session.add(admin_role1)
    # db.session.commit()

    # admin_role1.role_name = 'Administrator'
    # db.session(admin_role1)
    # db.session.commit()
    # print Role.query.all()
    # print User.query.filter_by(role=user_role).all()
    # print str(User.query.filter_by(role=user_role).all())

    one_user = User.query.filter_by(user_name='shikeyue').first()
    print one_user.user_name
    return render_template('index.html', current_time=datetime.utcnow())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])  # Should use DataRequired in WTF3.0 now it's 2.1
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.String(64), primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.role_name


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(64), primary_key=True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.String, db.ForeignKey('roles.role_id'))

    def __repr__(self):
        return '<User %r>' % self.user_name


if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()
    # print "db create now!"
    manager.run()
