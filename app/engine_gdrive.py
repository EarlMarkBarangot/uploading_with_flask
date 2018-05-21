from __future__ import print_function
import os

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from werkzeug import secure_filename
from app import db
from models import Users, Anonymous, Audio, Images, Profile, Type
import controller
from flask_login import current_user
import shutil
from sqlalchemy import and_

def get_credentials():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('app/json/storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('app/json/client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def upload_(*u_file):
    print(u_file)
    DRIVE = discovery.build('drive', 'v3', http=get_credentials().authorize(Http()))

    id_container = []
    for fname, mimeType in u_file:
        metadata = {'name': fname}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = DRIVE.files().create(body=metadata, media_body=fname, fields='webViewLink, id').execute()
        if res:
            id_container.append(res.get('id'))
    try:
        return id_container[0]
    except IndexError:
        pass
    return None

def download_(id):
    DRIVE = discovery.build('drive', 'v3', http=get_credentials().authorize(Http()))
    data = DRIVE.files().export(fileId=id, mimeType=None).execute()
    if data:
        filename = secure_filename(data.filename)
        data.save(os.path.join('app/static/', filename))


def gdrive_upload(file, name, typpe, allowed_func, curr_folder, modelClass, resource):
    file_rename = ""
    msg = "not ok"
    if file and allowed_func(file.filename):
        filename = secure_filename(file.filename)

        curr_path = curr_folder+'/'+str(current_user.id)

        if os.path.isdir(curr_path)==False:
            os.makedirs(curr_path)

        file.save(os.path.join(curr_path, filename))
        uploading = upload_((curr_path+'/'+filename, None))

        lc = Type.query.filter_by(name=str(typpe)).first()

        if uploading:
            if resource=='profile':
                proft = Profile.query.filter(and_(Profile.userid==current_user.id, Profile.typeID==lc.id)).all()
                for p in proft:
                    p.status = 0
                    db.session.add(p)
                db.session.commit()

                instance_ = modelClass(link=str(uploading), userid=current_user.id, typeID=lc.id)
                db.session.add(instance_)
                db.session.commit()

            else:
                instance_ = modelClass(link=str(uploading), userid=current_user.id, name=name, typeID=lc.id)
                db.session.add(instance_)
                db.session.commit()
            msg = "ok"
        shutil.rmtree(curr_path)
        return uploading, msg
    return None, msg


############ Original code ##########################################################################
#SCOPES = 'https://www.googleapis.com/auth/drive'
#store = file.Storage('json/storage.json')
#creds = store.get()
#if not creds or creds.invalid:
#    flow = client.flow_from_clientsecrets('json/client_secret.json', SCOPES)
#    creds = tools.run_flow(flow, store)
#DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

#FILES = (
#    ('w23.jpg', None),
#    ('index92.jpg', 'application/vnd.google-apps.photo'),
#)

#l = []
#for filename, mimeType in FILES:
#    metadata = {'name': filename}
#    if mimeType:
#        metadata['mimeType'] = mimeType
#    res = DRIVE.files().create(body=metadata, media_body=filename, fields='webViewLink, id').execute()
#    if res:
#        print('Uploaded "%s" (%s)' % (filename, 'application/vnd.google-apps.photo'))
#        l.append(res.get('id'))
#print (l[0])

#if res:
    #MIMETYPE = 'application/pdf'
#    MIMETYPE = 'application/vnd.google-apps.photo'
#    data = DRIVE.files().export(fileId=res['id'], mimeType=MIMETYPE).execute()
#    if data:
#        fn = '%s.jpg' % os.path.splitext(filename)[0]
#        with open(fn, 'wb') as fh:
#            fh.write(data)
#        print('Downloaded "%s" (%s)' % (fn, MIMETYPE))
