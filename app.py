#Importamos dependencias
from flask import Flask, render_template, send_from_directory
import os

#Creamos nuestra app de Flask
app = Flask(__name__)

#Le indicamos a Flask cual será la ruta en la que se encuentra nuestro html de Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

#!Como no guardaremos las imágenes en un directorio "static" que es por defecto donde se guardar archivos CSS, imágenes y scripts en Flask, hay 
#!que indicarle las rutas directamente de dónde están los archivos que importaremos, porque Flask no soporta importaciones directas de imágenes

#Esta es la ruta para importar el logo en nuestro archivo dashboard.html
@app.route('/logo/<path:filename>')
def custom_static1(filename):
    return send_from_directory(os.path.join(app.root_path, 'logo'), filename)

#Esta es la ruta para importar tanto el wordcloud como el piechart en nuestro archivo dashboard.html
@app.route('/root/<path:filename>')
def custom_static2(filename):
    return send_from_directory(app.root_path, filename)

#En esta parte le indicamos a Flask que cuando se ejecute el comando app.run() debe correr nuestra aplicación web
if __name__ == '__main__':
    app.run()