from flask import jsonify, request
from app import app, db
from models import *
from flask.ext.cors import cross_origin
from controller import img_folder, audio_folder, profile_folder, available_extension, audio_available_extension, allowed_file, audio_allowed_file
from sqlalchemy import and_
import os
from werkzeug import secure_filename

#user request.args.get() to get 1 or 2 items
#user request.form.get() to get 3 or more items

reg_user_username = None

def return_id():
	global reg_user_username
	namee = reg_user_username

	user = Users.query.filter_by(username=namee).first()
	return user.id


@app.route('/api/upload/image', methods=['POST'])
@cross_origin('*')
def upload_images():
	file = request.files['image']
	name = request.form['name']

	file_rename = ""
	msg = "not ok"
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file_rename = filename
		file.save(os.path.join(img_folder, filename))
		msg = "ok"

		image_ = Images(link='/static/js/uploads/img/'+file_rename, userid=return_id(), name=name)
		db.session.add(image_)
		db.session.commit()

	file_flash = '/static/js/uploads/img/'+file_rename
	return jsonify({'msg': msg, 'name': name, 'filename': file_flash, 'next_node':'/home'})


@app.route('/api/upload/audio', methods=['GET', 'POST'])
@cross_origin('*')
def upload_audio():
	file = request.files['song']
	name = request.form['name']

	file_rename = ""
	msg = "not ok"
	if file and audio_allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file_rename = filename
		file.save(os.path.join(audio_folder, filename))
		msg = "ok"

		profile_ = Audio(link='/static/js/uploads/audio/'+file_rename, userid=return_id(), name=name)
		db.session.add(profile_)
		db.session.commit()

	file_flash = '/static/js/uploads/audio/'+file_rename
	return jsonify({'msg': msg, 'name': name, 'filename': file_flash, 'next_node':'/home'})


@app.route('/api/profilepic', methods=['GET', 'POST'])
@cross_origin('*')
def upload_profile_pic():
	file = request.files['avatar']

	file_rename = ""
	msg = "not ok"
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file_rename = filename
		file.save(os.path.join(profile_folder, filename))
		msg = "ok"

		proft = Profile.query.filter_by(userid=return_id()).all()
		for p in proft:
			p.status = 0
			db.session.add(p)
		db.session.commit()

		audio_ = Profile(link='/static/js/uploads/profile/'+file_rename, userid=return_id())
		db.session.add(audio_)
		db.session.commit()


	file_flash = '/static/js/uploads/profile/'+file_rename
	global reg_user_username
	name = reg_user_username
	return jsonify({'msg': msg, 'name': name, 'filename': file_flash, 'next_node':'/home'})


@app.route('/api/user/data', methods=['GET', 'POST'])
def load():
	if return_id():
		profile = Profile.query.filter(and_(Profile.userid==return_id(), Profile.status==1)).first()
		audio = Audio.query.filter_by(userid=return_id()).all()
		image = Images.query.filter_by(userid=return_id()).all()

		#audio
		audio__ = []
		if audio:
			for au in audio:
				audio__.append((au.link, au.name))

		#image
		image__ = []
		if image:
			for im in image:
				image__.append((im.link, im.name))

		global reg_user_username
		usedname = reg_user_username

		vertus = ""
		if profile:
			vertus = profile.link

		return jsonify({'msg': 'ok', 'profimg': vertus, 'username': usedname, 'audioN': audio__, 'imageN': image__, 'audioCount': len(audio__), 'imageCount': len(image__)})
	return jsonify({'msg': 'failed'})


@app.route('/api/login', methods=['GET', 'POST'])
@cross_origin('*')
def api_login():
	uname, pw = request.args.get('username'), request.args.get('password')

	if uname and pw:
		user = Users.query.filter_by(username=uname).first()
		if user:
			if pw==user.password:
				global reg_user_username
				reg_user_username = user.username
				return jsonify({'msg': 'ok', 'next_node':'/home'})

	return jsonify({'msg': 'login failed!'})


@app.route('/api/signup', methods=['GET', 'POST'])
@cross_origin('*')
def api_signup():
	uname = request.form.get('username')
	pw = request.form.get('password')
	email = request.form.get('email')
	#uname, pw, email = request.args.get('username'), request.args.get('password'), request.args.get('email')
	print uname

	if uname and pw and email:
		if (uname!="") and (pw!="") and (email!=""):
			print 'dfdf'
			user = Users(username=uname, email=email, password=pw)
			db.session.add(user)
			db.session.commit()
			return jsonify({'msg': 'ok', 'next_node': '/login'})

	return jsonify({'msg': 'something went wrong!'})


@app.route('/api/logout', methods=['GET', 'POST'])
@cross_origin('*')
def api_logout():
	global reg_user_username
	reg_user_username = None
	return jsonify({'msg': 'logged out', 'next_node': '/'})