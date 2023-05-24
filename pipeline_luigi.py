#Importamos las dependencias
import os
import luigi
import webbrowser

#Importamos los componentes(funciones)
from twitterscraper import extract_tweets as et
from tweets_cleaner import clean_tweets as ct
from translate_tweets import trans_tweets as tt
from sentiment_analyzer import analyze_sentiment as sa
from save_to_database import save_database as sd
from wordcloud_script import create_wordcloud as wc
from piechart_script import create_piechart as cp
from app import app

#!Creamos una clase que se encargue de eliminar todos los archivos en caso de que existan, es lo primero que se ejecutará
#!Esto es importante a la hora de iniciar una nueva sesión de Luigi, porque si existe algún archivo de alguna sesión anterior
#!Luigi se salteará el orden de pasos, ocasionando que no se haga el proceso como debe de ser.
class LetsCleanIt:
    @staticmethod
    def CleanAll():
        files_to_remove = [
            'scrapped_tweets.csv',
            'cleaned_tweets.csv',
            'translated_tweets.csv',
            'tweets_with_sentiment.csv',
            'databaseOK.txt',
            'piechart.png',
            'wordcloud.png',
        ]
        
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

#!A partir de aquí le indicaremos a Luigi el paso a paso que debe de recorrer, es decir, qué ejecute las tareas en el orden secuenciado que deseamos
#!Cada etapa será similar, primero se le indica qué es necesario para inciar una tarea, como regla general Luigi espera un "output" de cada tarea
#!para indicarle a la siguiente que debe comenzar, pues la anterior ya ha finalizado.
#!Por ello es que cada tarea genera un archivo csv(o txt en caso del script de guardado en base de datos).


#?Aquí le indicamos que debe comenzar esta tarea de forma inicial y por ello no requiere un output anterior para inciar
class ExtractTweets(luigi.Task):
    def run(self):
        et()

    #Una vez que se finaliza la tarea actual, se generará el archivo csv, que le indique a la siguiente tarea que puede comenzar
    def complete(self):
        return os.path.exists('scrapped_tweets.csv')


#?Aquí le indicamos a Luigi que antes de comenzar esta tarea debe esperar que la anterior haya finalizado, el indicador es el archivo csv generado
class CleanTweets(luigi.Task):
    def requires(self):
        return ExtractTweets()

    #Si se verifica que la tarea anterior ha terminado, se ejecutará esta nueva tarea
    def run(self):
        ct()

    #Nuevamente se indica que una vez finalizada la tarea actual, debe crear un archivo csv para que la tarea siguiente pueda ejecutarse
    def complete(self):
        return os.path.exists('cleaned_tweets.csv')

#!A partur de aquí será una repetición de todo lo indicado anteriormente

#Tarea que traduce los tweets
class TranslateTweets(luigi.Task):
    def requires(self):
        return CleanTweets()

    def run(self):
        tt()

    def complete(self):
        return os.path.exists('translated_tweets.csv')

#Tarea que realiza el análisis de sentimientos
class AnalyzeSentiment(luigi.Task):
    def requires(self):
        return TranslateTweets()

    def run(self):
        sa()

    def complete(self):
        return os.path.exists('tweets_with_sentiment.csv')

#Tarea que guarda el dataframe dentro de una tabla en nuestra base de datos
class SaveDatabase(luigi.Task):
    def requires(self):
        return AnalyzeSentiment()

    def run(self):
        if os.path.exists('databaseOK.txt'):
            os.remove('databaseOK.txt')
        sd()

    def complete(self):
        return os.path.exists('databaseOK.txt')
    
#Tarea que crea nuestro piechart
class CreatePiechart(luigi.Task):
    def requires(self):
        return SaveDatabase()

    def run(self):
        if os.path.exists('piechart.png'):
            os.remove('piechart.png')
        cp()

    def complete(self):
        return os.path.exists('piechart.png')

#Tarea que crea nuestra wordcloud
class CreateWordCloud(luigi.Task):
    def requires(self):
        return CreatePiechart()

    def run(self):
        if os.path.exists('wordcloud.png'):
            os.remove('wordcloud.png')
        wc()

    def complete(self):
        return os.path.exists('wordcloud.png')
    

#Tarea que
class RunApp(luigi.Task):
    def requires(self):
        return CreateWordCloud()
    
    #Como esta es la última tarea no generará un archivo de output que le indique que esta tarea ha finalizado, por lo que se ejecutará indefinidamente
    def run(self):
        webbrowser.open("http://localhost:5000")
        app.run()
    
if __name__ == '__main__':
    #Acá indicamos que lo primero que debe ejecutar es la función de eliminar todos los archivos en caso de existir
    LetsCleanIt.CleanAll()
    #Le indicamos que debe ejecutar Flask como útlima medida y que por lo tanto, hasta que no se cierre Flask no se ha terminado el conjunto de tareas
    luigi.run(main_task_cls=RunApp)