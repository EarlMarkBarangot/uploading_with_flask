from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<username {}>'.format(self.username)

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500))
    status = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, link, userid):
        self.link = link
        self.userid = userid
        self.status = 1

    def __repr__(self):
        return '<userid {}>'.format(self.userid)

class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key= True)
    link = db.Column(db.String(500))
    name = db.Column(db.String(500))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, link, userid, name):
        self.link = link
        self.userid = userid
        self.name = name

    def __repr__(self):
        return '<userid {}>'.format(self.userid)

class Audio(db.Model):
    __tablename__ = "audio"
    id = db.Column(db.Integer, primary_key= True)
    link = db.Column(db.String(500))
    name = db.Column(db.String(500))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, link, userid, name):
        self.link = link
        self.userid = userid
        self.name = name

    def __repr__(self):
        return '<userid {}>'.format(self.userid)