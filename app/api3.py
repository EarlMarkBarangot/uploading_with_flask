from flask import jsonify, request, session
from app import app, db
from models import Users, Anonymous, Audio, Images, Profile, Type
from flask.ext.cors import cross_origin
from controller import img_folder, audio_folder, profile_folder, available_extension, audio_available_extension, allowed_file, audio_allowed_file, app_dump
import os
from werkzeug import secure_filename
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#the upload
from engine_cloudinary import cloudinary_upload

#user request.args.get() to get 1 or 2 items
#user request.form.get() to get 3 or more items
#api version 3
#here instead of uploading files to our local app, we will upload it to cloudinary
@app.route('/api/v3/upload/image', methods=['POST'])
@cross_origin('*')
def upload_images_3():
	file = request.files['image']
	name = request.form['name']
	typpe = request.form['type']

	t,msg = cloudinary_upload(file, name, typpe, allowed_file, app_dump, Images, 'image')

	return jsonify({'msg': msg, 'name': name, 'filename': str(t), 'next_node':'/home3'})


@app.route('/api/v3/upload/audio', methods=['GET', 'POST'])
@cross_origin('*')
def upload_audio_3():
	file = request.files['song']
	name = request.form['name']
	typpe = request.form['type']

	t,msg = cloudinary_upload(file, name, typpe, audio_allowed_file, app_dump, Audio, 'audio')

	return jsonify({'msg': msg, 'name': name, 'filename': str(t), 'next_node':'/home3'})


@app.route('/api/v3/profilepic', methods=['GET', 'POST'])
@cross_origin('*')
def upload_profile_pic_3():
	file = request.files['avatar']
	typpe = request.form['type']

	t,msg = cloudinary_upload(file, None, typpe, allowed_file, app_dump, Profile, 'profile')

	return jsonify({'msg': msg, 'name': current_user.username, 'filename': str(t), 'next_node':'/home3'})