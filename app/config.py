#configs live here, like the database engine creds

db_user     = "root"
db_password = "my_password"
db_host     = "localhost"
db_name     = "my_db"

mysql_database = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"