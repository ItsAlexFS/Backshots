from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

#cargar de .env las variables de entorno
load_dotenv()

#CREAR INSTANCIA DE SQL
mysql = MySQL()

#funcion para conectar db
def init_db(app):
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
    mysql.init_app(app)


    #definimos cursor
def get_db_connection():
    try:
        connection=mysql.connection
        return connection.cursor()
    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")