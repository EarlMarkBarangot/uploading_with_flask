from models import Users, Anonymous, Audio, Images, Profile, Type
import controller 
import os
from werkzeug import secure_filename
from flask_login import current_user
from app import db
from sqlalchemy import and_


def local_upload(file, name, typpe, allowed_func, curr_folder, curr_folder_alter, modelClass, resource):
	fileres = ""
	msg = "not ok"
	if file and allowed_func(file.filename):
		filename = secure_filename(file.filename)
		fileres = filename

		curr_path = curr_folder+str(current_user.id)
		if os.path.isdir(curr_path)==False:
			os.makedirs(curr_path)

		file.save(os.path.join(curr_path, filename))
		msg = "ok"

		lc = Type.query.filter_by(name=str(typpe)).first()
		print lc.id

		curr_path_alter = curr_folder_alter+str(current_user.id)


		if resource=='profile':
			proft = Profile.query.filter(and_(Profile.userid==current_user.id, Profile.typeID==lc.id)).all()
			for p in proft:
				p.status = 0
				db.session.add(p)
			db.session.commit()

			instance_ = modelClass(link=curr_path_alter+'/'+filename, userid=current_user.id, typeID=lc.id)
			db.session.add(instance_)
			db.session.commit()
		else:
			instance_ = modelClass(link=curr_path_alter+'/'+filename, userid=current_user.id, name=name, typeID=lc.id)
			db.session.add(instance_)
			db.session.commit()

	return curr_path_alter+'/'+fileres, msg

