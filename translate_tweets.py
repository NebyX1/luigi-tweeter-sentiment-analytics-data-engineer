def trans_tweets():
    #Importamos las dependencias
    import pandas as pd
    from deep_translator import GoogleTranslator

    #Creamos una función con bloque try/except para manejo de errores, que traducirá cada tweet(text) que se le pase de español a inglés.
    def translate_to_english(text):
        try:
            return GoogleTranslator(source='spanish', target='english').translate(text)
        except Exception as e:
            print(f"Error: {text} --> {str(e)}")
            return text

    #Importamos el archivo csv con los tweets ya limpios y lo guardamos en un dataframe
    df = pd.read_csv("cleaned_tweets.csv")

    #En caso de que por alguna razón existan celdas en blanco, los rellenaremos con "Nan"
    df['Comentario'] = df['Comentario'].fillna('')

    #Aplicamos a toda la columna comentarios la función "translate_to_english", lo que recorrerá tweet por tweet y los traducirá al inglés.
    df['tweet_english'] = df['Comentario'].apply(translate_to_english)

    #Guardamos nuestro dataframe resultante dentro de un archivo csv
    df.to_csv("translated_tweets.csv", index=False)