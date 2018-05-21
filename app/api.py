from flask import jsonify, request, session
from app import app, db
from models import Users, Anonymous, Audio, Images, Profile, Type
from flask.ext.cors import cross_origin
import controller 
from sqlalchemy import and_
import os
from werkzeug import secure_filename
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

##using the local upload function
from engine_local import local_upload

#user request.args.get() to get 1 or 2 items
#user request.form.get() to get 3 or more items
#uses local storage

#api version 1
@app.route('/api/v1/upload/image', methods=['POST'])
@cross_origin('*')
def upload_images():
	file = request.files['image']
	name = request.form['name']
	typpe = request.form['type']

	#getting results from engine_local.local_upload
	#local_upload(file, name, engine_type, the_allowed_file_extension_function, 
	#the_img_folder, the_img_saver_folder, the model class, upload_type)
	t,msg = local_upload(file, name, typpe, controller.allowed_file, 
		controller.img_folder, controller.img_folder_alter,Images, 'image')

	return jsonify({'msg': msg, 'name': name, 'filename': t, 'next_node':'/home'})


@app.route('/api/v1/upload/audio', methods=['GET', 'POST'])
@cross_origin('*')
def upload_audio():
	file = request.files['song']
	name = request.form['name']
	typpe = request.form['type']

	#getting results from engine_local.local_upload
	#local_upload(file, name, engine_type, the_allowed_file_extension_function, 
	#the_audio_folder, the_audio_saver_folder, the model class, upload_type)
	t,msg = local_upload(file, name, typpe, controller.audio_allowed_file, 
		controller.audio_folder, controller.audio_folder_alter,Audio, 'audio')

	return jsonify({'msg': msg, 'name': name, 'filename': t, 'next_node':'/home'})


@app.route('/api/v1/profilepic', methods=['GET', 'POST'])
@cross_origin('*')
def upload_profile_pic():
	file = request.files['avatar']
	typpe = request.form['type']

	#getting results from engine_local.local_upload
	#local_upload(file, name, engine_type, the_allowed_file_extension_function, 
	#the_profile_folder, the_profile_saver_folder, the model class, upload_type)
	t,msg = local_upload(file, None, typpe, controller.allowed_file, 
		controller.profile_folder, controller.profile_folder_alter,Profile, 'profile')

	return jsonify({'msg': msg, 'name': current_user.username, 'filename': t, 'next_node':'/home'})


@app.route('/api/v1/user/data', methods=['GET', 'POST'])
def load():
	if current_user.is_active():
		profile = Profile.query.filter(and_(and_(Profile.userid==current_user.id, Profile.status==1),Profile.typeID==int(request.args.get('type')))).first()
		audio = Audio.query.filter(and_(Audio.userid==current_user.id, Audio.typeID==int(request.args.get('type')))).all()
		image = Images.query.filter(and_(Images.userid==current_user.id, Audio.typeID==int(request.args.get('type')))).all()

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


		vertus = ""
		if profile:
			vertus = profile.link

		return jsonify({'msg': 'ok', 'profimg': vertus, 'username': current_user.username, 'audioN': audio__, 'imageN': image__, 'audioCount': len(audio__), 'imageCount': len(image__)})
	return jsonify({'msg': 'failed'})


@app.route('/api/v1/login', methods=['GET', 'POST'])
@cross_origin('*')
def api_login():
	if current_user.is_active():
		return jsonify({'msg': 'ok', 'next_node':'/home'})
	else:
		uname, pw = request.args.get('username'), request.args.get('password')
		print pw

		if uname and pw:
			user = Users.query.filter_by(username=uname).first()
			if user:
				print check_password_hash(user.password, pw)
				if check_password_hash(user.password, pw):
					login_user(user)
					return jsonify({'msg': 'ok', 'next_node':'/home'})

	return jsonify({'msg': 'login failed!'})


@app.route('/api/v1/signup', methods=['GET', 'POST'])
@cross_origin('*')
def api_signup():
	if current_user.is_active():
		return jsonify({'msg': 'ok', 'next_node':'/home'})
	else:
		uname = request.form.get('username')
		pw = request.form.get('password')
		email = request.form.get('email')

		if uname and pw and email:
			if (uname!="") and (pw!="") and (email!=""):
				user = Users(username=uname, email=email, password=pw)
				db.session.add(user)
				db.session.commit()
				return jsonify({'msg': 'ok', 'next_node': '/login'})

	return jsonify({'msg': 'something went wrong!'})


@app.route('/api/v1/logout', methods=['GET', 'POST'])
@cross_origin('*')
def api_logout():
	logout_user()
	return jsonify({'msg': 'logged out', 'next_node': '/'})



