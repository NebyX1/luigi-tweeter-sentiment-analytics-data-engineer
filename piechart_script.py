def create_piechart():
    #Importamos las dependencias
    import pandas as pd
    import matplotlib.pyplot as plt
    from database_engine import engine

    #Guardamos el engine de SQL Alchemy en la variable engine
    engine = engine

    #Leemos desde la base de datos, la tabla "tabla_1"
    df = pd.read_sql_table('tabla_1', engine)

    #Va recorrer la columna "sentiment" de nuestro dataframe y sumará la cantidad de veces que se repite cada valor disponible(negative, positive y neutral)
    sentiment_counts = df['sentiment'].value_counts()

    #Le indicamos a matplotlib las características con las que debe crear nuestro piechart
    plt.figure(figsize=(10, 5))
    plt.pie(sentiment_counts, labels = sentiment_counts.index, autopct='%1.1f%%')
    plt.title('Sentiment Analysis Pie Chart')

    #Guardamos en la carpeta raíz del proyecto el piechart generado en formato png
    plt.savefig("piechart.png")

    #Esto sirve para mostrar en pantalla el piechart generado, por defecto está deshabilitado
    # plt.show()