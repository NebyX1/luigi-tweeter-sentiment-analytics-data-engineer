def analyze_sentiment():
    #Importamos las dependencias
    import pandas as pd
    import numpy as np
    from scipy.special import softmax
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig

    #En el caso de que aún haya quedado algún tweet con arrobamientos o links de pasos anteriores, esta función se encarga de limpiarlos
    def clean_tweet_english(tweet_english):
        new_tweet_english = []
        for t in tweet_english.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_tweet_english.append(t)
        return " ".join(new_tweet_english)

    #Esta función utiliza un modelo de Transformers para analizar el sentimiento del tweet de entrada, codifica el tweet, lo pasa por el modelo
    #y obtiene una puntuación de sentimiento, luego, clasifica las puntuaciones, determina el sentimiento y la polaridad, y los devuelve
    def get_sentiment(tweet_english):
        try:
            encoded_input = tokenizer(tweet_english, return_tensors='pt')
            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            ranking = np.argsort(scores)
            ranking = ranking[::-1]
            sentiment = config.id2label[ranking[0]]
            polarity = scores[ranking[0]]
            return sentiment, polarity
        except Exception as e:
            print(f"Error: {e}")
            return None, None

    #Aquí importamos el archivo csv a usar y lo guardamos en un dataframe
    df = pd.read_csv("translated_tweets.csv")

    #En esta línea aplicamos la función de limpiar los tweets sobre la columna que querramos usar
    df['tweet_english'] = df['tweet_english'].apply(clean_tweet_english)

    #Esto elimina cualquier fila del DataFrame donde 'tweet_english' esté vacío o solo contenga espacios en blanco.
    df = df[df['tweet_english'].str.strip() != ""]

    #Esto carga un modelo pre-entrenado de Transformers llamado 'twitter-roberta-base-sentiment' y sus componentes asociados.
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)

    #Estas líneas guardan el modelo, el tokenizador y la configuración en el directorio local llamado "local_model_directory"
    model.save_pretrained("./local_model_directory/")
    tokenizer.save_pretrained("./local_model_directory/")
    config.save_pretrained("./local_model_directory/")

    #Estas líneas vuelven a cargar el modelo, el tokenizador y la configuración desde el directorio local
    tokenizer = AutoTokenizer.from_pretrained("./local_model_directory/")
    model = AutoModelForSequenceClassification.from_pretrained("./local_model_directory/")
    config = AutoConfig.from_pretrained("./local_model_directory/")

    #Esto convoca a la función "get_sentiment(", la cual agregará dos nuevas columnas a nuestro dataframe, las mismas son "sentiment" y "polarity",
    #que contienen el resultado del análisis llevado a cabo por el modelo "Roberta" de HuggingFace, pasará tweet por tweet
    df['sentiment'], df['polarity'] = zip(*df['tweet_english'].apply(get_sentiment))

    #Guardamos en un csv lo resultante del análisis de sentimientos
    df.to_csv("tweets_with_sentiment.csv", index=False)