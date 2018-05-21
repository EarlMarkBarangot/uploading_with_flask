from werkzeug import secure_filename

img_folder = 'app/static/uploads/img/'
audio_folder = 'app/static/uploads/audio/'
profile_folder = 'app/static/uploads/profile/'

img_folder_alter = '/static/uploads/img/'
audio_folder_alter = '/static/uploads/audio/'
profile_folder_alter = '/static/uploads/profile/'

app_dump = 'app/dumps'




available_extension = set(['png', 'jpg', 'PNG', 'JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in available_extension

audio_available_extension = set(['mp3', 'flac', 'aac'])

def audio_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in audio_available_extension