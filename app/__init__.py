from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from flask.ext.cors import CORS
from config import *

app = Flask(__name__)
db = SQLAlchemy(app)
CORS(app, headers=['Content-Type'])

app.config['SQLALCHEMY_DATABASE_URI'] = app_sql_uri
app.config['CORS_HEADERS'] = app_headers
app.config['SECRET_KEY'] = app_secret_key

import models
db.create_all()

models.Type.uploader_types()

from app import views, api, api2, api3

app.debug = True