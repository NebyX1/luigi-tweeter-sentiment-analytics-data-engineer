#Importamos las dependencias
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#Cargamos el contenido del archivo .env(variables de entorno)
load_dotenv()

#Aquí importamos dentro de nuevas variables los datos del archivo .env que nos permitirán conectarnos a la base de datos
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')

#Creamos el motor(engine) de conexión a nuestra base de datos MySQl, que acturá de DataWarehouse
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')