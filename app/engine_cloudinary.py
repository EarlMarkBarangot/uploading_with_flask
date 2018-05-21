import os
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import controller
from flask_login import current_user
import shutil
from sqlalchemy import and_
from werkzeug import secure_filename
from app import db
from models import Users, Anonymous, Audio, Images, Profile, Type

#the idea is that the cloudinary upload() function might not be able to find the file, so to be safe
#the file must be temporarily save somewhere inside the app folder and then be the one for the upload function
#then after the upload is successful, the temporary directory that was made will be remove from the app folder

def cloudinary_upload(file, name, typpe, allowed_func, curr_folder, modelClass, resource):
	cloudinary.config(
		cloud_name = 'silverly',
		api_key = '393882568386968',
		api_secret = 'RlS1MEq2NDzByGKDuVobeRTCYvY'
	)

	#to handle files that are not image by  default
	options = {"resource_type":"raw"}

	file_rename = ""
	msg = "not ok"
	if file and allowed_func(file.filename):
		#we need to secure the filename first
		filename = secure_filename(file.filename)
	
		#make a current path
		curr_path = curr_folder+'/'+str(current_user.id)

		#check that path
		if os.path.isdir(curr_path)==False:
			os.makedirs(curr_path)

		#save the file somewhere on our app
		file.save(os.path.join(curr_path, filename))

		#the upload function - upload(file, **options)
		uploading = upload(curr_path+'/'+filename, **options)

		#check the type
		lc = Type.query.filter_by(name=str(typpe)).first()

		if uploading:
			#if the uploaded file is for profile picture
			if resource=='profile':
				proft = Profile.query.filter(and_(Profile.userid==current_user.id, Profile.typeID==lc.id)).all()
				for p in proft:
					p.status = 0
					db.session.add(p)
					db.session.commit()

				instance_ = modelClass(link=str(uploading['url']), userid=current_user.id, typeID=lc.id)
				db.session.add(instance_)
				db.session.commit()

			else:
				instance_ = modelClass(link=str(uploading['url']), userid=current_user.id, name=name, typeID=lc.id)
				db.session.add(instance_)
				db.session.commit()
			msg = "ok"
		#remove the directory we have created
		shutil.rmtree(curr_path)

		#returns the cloudinary url and msg
		return uploading['url'], msg
	return None, msg
