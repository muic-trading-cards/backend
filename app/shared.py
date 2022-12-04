#configs live here, like the database engine creds
import os
from app.credentials import *

prepare_credentials()
db_user     = os.environ.get("mysql_user")
db_password = os.environ.get("mysql_password")
db_host     = os.environ.get("mysql_host")
mysql_db    = os.environ.get("login_db") #old but login_db is the name of the database before deciding to just use one database for everything
#shouldn't be a big deal, this class isn't focused on security, let's just get it working before adding more stuff


mysql_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{mysql_db}"
default_profile_picture_url = "https://e-bugle.com/uploads/empty_user.png"
