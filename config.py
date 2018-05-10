import os

basedir = os.path.abspath(os.path.dirname(__file__))

#app configs
app_sql_uri = 'mysql://root:@localhost/up'
app_secret_key = "flasky"
app_headers = "Content-Type, Authorization"

#google drive configs
gdrive_user = ''
gdrive_password = ''