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
from engine_gdrive import gdrive_upload

#user request.args.get() to get 1 or 2 items
#user request.form.get() to get 3 or more items
#api version 2 uses google drive
#here instead of uploading files to our local app, we will upload it to google drive
@app.route('/api/v2/upload/image', methods=['POST'])
@cross_origin('*')
def upload_images_2():
	file = request.files['image']
	name = request.form['name']
	typpe = request.form['type']

	t,msg = gdrive_upload(file, name, typpe, allowed_file, app_dump, Images, 'image')

	return jsonify({'msg': msg, 'name': name, 'filename': str(t), 'next_node':'/home2'})

@app.route('/api/v2/upload/audio', methods=['GET', 'POST'])
@cross_origin('*')
def upload_audio_2():
	file = request.files['song']
	name = request.form['name']
	typpe = request.form['type']

	t,msg = gdrive_upload(file, name, typpe, audio_allowed_file, app_dump, Audio, 'audio')

	return jsonify({'msg': msg, 'name': name, 'filename': str(t), 'next_node':'/home2'})


@app.route('/api/v2/profilepic', methods=['GET', 'POST'])
@cross_origin('*')
def upload_profile_pic_2():
	file = request.files['avatar']
	typpe = request.form['type']

	t,msg = gdrive_upload(file, None, typpe, allowed_file, app_dump, Profile, 'profile')

	return jsonify({'msg': msg, 'name': current_user.username, 'filename': str(t), 'next_node':'/home2'})