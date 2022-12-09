#configs live here, like the database engine creds
import os
from app.credentials import *


db_user     = os.environ.get("mysql_user")
db_password = os.environ.get("mysql_password")
db_host     = os.environ.get("mysql_host")
mysql_db    = os.environ.get("login_db") #old but login_db is the name of the database before deciding to just use one database for everything

s3_user     = os.environ.get("mysql_user") #reusing same user and password
s3_password = os.environ.get("mysql_password")
s3_host     = os.environ.get("mysql_host")
s3_port = "9000"
#shouldn't be a big deal, this class isn't focused on security, let's just get it working before adding more stuff


mysql_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{mysql_db}"
default_profile_picture_url = "https://e-bugle.com/uploads/empty_user.png"

s3_config = {
    "service_name": "s3",
    "aws_access_key_id": s3_user,
    "aws_secret_access_key": s3_password,
    "endpoint_url": f"http://{s3_host}:{s3_port}",
    "verify": False
}
