from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'user'
app.config['MYSQL_DATABASE_DB'] = 'gloriamenu'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)