def create_wordcloud():
    
    #Importamos las dependencias
    import pandas as pd
    import nltk
    from nltk.corpus import stopwords
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    from database_engine import engine

    #Guardamos el engine de SQL Alchemy en la variable engine
    engine = engine

    #Importamos los módulos de NLTK para quitar palabras de enlace
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('spanish'))

    #Leemos desde la base de datos, la tabla "tabla_1"
    df = pd.read_sql_table('tabla_1', engine)

    #Guardamos dentro de un dataframe el contenido de la columna "Comentario"
    df['Comentario'] = df['Comentario'].fillna('')

    #Combinamos todos los tweets a lo largo de la columna "Comentario"
    combined_tweets = " ".join(df['Comentario'])

    #Convertimos a tokens las palabras para su mejor tratamiento
    word_tokens = nltk.word_tokenize(combined_tweets)
    filtered_text = " ".join(word for word in word_tokens if word.casefold() not in stop_words)

    #Le indicamos el tamaño que queremos que tenga el wordcloud generado y la cantidad de palabras que queremos que aparezcan
    wordcloud = WordCloud(width=800, height=400, max_words=120).generate(filtered_text)

    #Le indicamos a matplotlib las características con las que debe crear nuestro wordcloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    #Guardamos en la carpeta raíz del proyecto el wordcloud generado en formato png
    wordcloud.to_file("wordcloud.png")

    #Esto sirve para mostrar en pantalla el wordcloud generado, por defecto está deshabilitado
    # plt.show()