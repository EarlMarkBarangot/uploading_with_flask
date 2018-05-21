from flask import jsonify, request, session
from app import app, db
from models import Users, Anonymous, Audio, Images, Profile, Type
from flask.ext.cors import cross_origin
from controller import img_folder, audio_folder, profile_folder, available_extension, audio_available_extension, allowed_file, audio_allowed_file, app_dump
from sqlalchemy import and_
import os
from werkzeug import secure_filename
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from engine_gdrive import upload_
import shutil

#user request.args.get() to get 1 or 2 items
#user request.form.get() to get 3 or more items
#api version 3
#here instead of uploading files to our local app, we will upload it to cloudinary
@app.route('/api/v3/upload/image', methods=['POST'])
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


@app.route('/api/v3/upload/audio', methods=['GET', 'POST'])
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


@app.route('/api/v3/profilepic', methods=['GET', 'POST'])
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