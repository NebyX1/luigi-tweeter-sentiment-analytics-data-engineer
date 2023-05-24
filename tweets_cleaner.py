def clean_tweets():
    #Importamos las dependencias
    import pandas as pd
    import re
    import numpy as np

    #Importamos el archivo csv generado en el paso anterior que fue el scraping de tweets
    df = pd.read_csv('scrapped_tweets.csv')

    #Convertimos todos los datos de "Comentario" a tipo string para no tener problemas de "tipado"
    df['Comentario'] = df['Comentario'].astype(str)

    #Aplicamos expresiones regulares para eliminar caracteres indeseados, enlaces y arrobamiento, y luego convertimos todo a minúsculas 
    df['Comentario'] = df['Comentario'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    df['Comentario'] = df['Comentario'].apply(lambda x: re.sub(r'\s+', ' ', x))
    df['Comentario'] = df['Comentario'].apply(lambda x: re.sub(r'http\S+|www.\S+', '', x))
    df['Comentario'] = df['Comentario'].apply(lambda x: re.sub(r'@\w+', '', x))
    df['Comentario'] = df['Comentario'].apply(lambda x: re.sub(r'\d+', '', x))
    df['Comentario'] = df['Comentario'].apply(lambda x: x.lower().strip())

    #Reemplazamos los espacios en blanco de la columna Comentario con "Nan"
    df['Comentario'].replace('', np.nan, inplace=True)

    #Eliminamos todas las filas que tengan valor "Nan" en la celda de la columna "Comentario"
    df.dropna(subset=['Comentario'], inplace=True)

    #Eliminamos todos los tweets duplicados y solo nos quedamos con uno de ellos en caso de existir más de uno
    df.drop_duplicates(subset='Comentario', keep='first', inplace=True)

    #Guardamos el resultado de la limpieza sin un índice
    df.to_csv('cleaned_tweets.csv', index=False)