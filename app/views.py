from flask import render_template, request
from app import app, db
from models import *

@app.route('/')
@app.route('/login')
@app.route('/login/')
def login():
	return render_template('login.html')

@app.route('/signup')
@app.route('/signup/')
def register():
	return render_template('register.html')

@app.route('/home')
@app.route('/home/')
def home():
	return render_template('home.html')