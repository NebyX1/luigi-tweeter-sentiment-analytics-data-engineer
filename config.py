#Importamos dependencias
from dotenv import load_dotenv
import os

#Cargamos el contenido del archivo .env(variables de entorno)
load_dotenv()

#Aquí importamos dentro de nuevas variables los datos del archivo .env que nos permitirán inciar Chrome con nuestra cuenta de usuario y perfil
chrome_driver = os.environ['CHROME_DRIVER']
profile_path = os.environ['PROFILE_PATH']