from flask import jsonify, request, session
from app import app, db
from models import Users, Anonymous, Audio, Images, Profile
from flask.ext.cors import cross_origin
from controller import img_folder, audio_folder, profile_folder, available_extension, audio_available_extension, allowed_file, audio_allowed_file, app_dump
from sqlalchemy import and_
import os
from werkzeug import secure_filename
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from gdrive import upload_
import shutil

#user request.args.get() to get 1 or 2 items
#user request.form.get() to get 3 or more items

#api version 1
@app.route('/api/upload/image', methods=['POST'])
@cross_origin('*')
def upload_images():
	file = request.files['image']
	name = request.form['name']

	print file

	file_rename = ""
	msg = "not ok"
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		print filename
		file_rename = filename
		file.save(os.path.join(img_folder, filename))
		msg = "ok"

		image_ = Images(link='/static/js/uploads/img/'+file_rename, userid=current_user.id, name=name)
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

		profile_ = Audio(link='/static/js/uploads/audio/'+file_rename, userid=current_user.id, name=name)
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

		proft = Profile.query.filter_by(userid=current_user.id).all()
		for p in proft:
			p.status = 0
			db.session.add(p)
		db.session.commit()

		audio_ = Profile(link='/static/js/uploads/profile/'+file_rename, userid=current_user.id)
		db.session.add(audio_)
		db.session.commit()


	file_flash = '/static/js/uploads/profile/'+file_rename

	return jsonify({'msg': msg, 'name': current_user.username, 'filename': file_flash, 'next_node':'/home'})


@app.route('/api/user/data', methods=['GET', 'POST'])
def load():
	if current_user.is_active():
		profile = Profile.query.filter(and_(Profile.userid==current_user.id, Profile.status==1)).first()
		audio = Audio.query.filter_by(userid=current_user.id).all()
		image = Images.query.filter_by(userid=current_user.id).all()

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


@app.route('/api/login', methods=['GET', 'POST'])
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


@app.route('/api/signup', methods=['GET', 'POST'])
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


@app.route('/api/logout', methods=['GET', 'POST'])
@cross_origin('*')
def api_logout():
	logout_user()
	return jsonify({'msg': 'logged out', 'next_node': '/'})



#api version 2
#here instead of uploading files to our local app, we will upload it to google drive
@app.route('/api2/upload/image', methods=['POST'])
@cross_origin('*')
def upload_images_2():
	file = request.files['image']
	name = request.form['name']

	file_rename = ""
	msg = "not ok"
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)

		curr_path = app_dump+'/'+str(current_user.id)

		if os.path.isdir(curr_path)==False:
			os.makedirs(curr_path)

		file.save(os.path.join(curr_path, filename))
		uploading = upload_((curr_path+'/'+filename, None))

		if uploading:
			image_ = Images(link=str(uploading), userid=current_user.id, name=name)
			db.session.add(image_)
			db.session.commit()
			msg = "ok"
		shutil.rmtree(curr_path)

		return jsonify({'msg': msg, 'name': name, 'filename': str(uploading), 'next_node':'/home2'})
	return jsonify({'msg': 'not ok'})


@app.route('/api2/upload/audio', methods=['GET', 'POST'])
@cross_origin('*')
def upload_audio_2():
	file = request.files['song']
	name = request.form['name']

	file_rename = ""
	msg = "not ok"
	if file and audio_allowed_file(file.filename):
		filename = secure_filename(file.filename)

		curr_path = app_dump+'/'+str(current_user.id)

		if os.path.isdir(curr_path)==False:
			os.makedirs(curr_path)

		file.save(os.path.join(curr_path, filename))
		uploading = upload_((curr_path+'/'+filename, None))

		if uploading:
			profile_ = Audio(link=str(uploading), userid=current_user.id, name=name)
			db.session.add(profile_)
			db.session.commit()
			msg = "ok"
		shutil.rmtree(curr_path)

		return jsonify({'msg': msg, 'name': name, 'filename': str(uploading), 'next_node':'/home2'})
	return jsonify({'msg': 'not ok'})


@app.route('/api2/profilepic', methods=['GET', 'POST'])
@cross_origin('*')
def upload_profile_pic_2():
	file = request.files['avatar']

	file_rename = ""
	msg = "not ok"
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)

		curr_path = app_dump+'/'+str(current_user.id)

		if os.path.isdir(curr_path)==False:
			os.makedirs(curr_path)

		file.save(os.path.join(curr_path, filename))

		uploading = upload_((curr_path+'/'+filename, None))

		if uploading:		
			proft = Profile.query.filter_by(userid=current_user.id).all()
			for p in proft:
				p.status = 0
				db.session.add(p)
			db.session.commit()

			audio_ = Profile(link=str(uploading), userid=current_user.id)
			db.session.add(audio_)
			db.session.commit()

			msg = "ok"
		shutil.rmtree(curr_path)

		return jsonify({'msg': msg, 'name': current_user.username, 'filename': uploading, 'next_node':'/home2'})
	return jsonify({'msg': 'not ok'})