from flask import render_template, request
from app import app, db
from models import *
from flask_login import login_user, login_required, logout_user, LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route('/')
@app.route('/login')
@app.route('/login/')
def login():
	if current_user.is_active():
		return render_template('home.html')
	return render_template('login.html')

@app.route('/signup')
@app.route('/signup/')
def register():
	if current_user.is_active():
		return render_template('home.html')
	return render_template('register.html')

@app.route('/home')
@app.route('/home/')
@login_required
def home():
	return render_template('home.html')

@app.route('/home2')
@app.route('/home2/')
@login_required
def home2():
	return render_template('home2.html')