def save_database():    
    import pandas as pd
    import database_engine

    engine = database_engine.engine

    # Lee el archivo CSV
    df = pd.read_csv("tweets_with_sentiment.csv")

    # Guarda el DataFrame en la tabla 'tabla_1' de la base de datos
    df.to_sql('tabla_1', con=engine, if_exists='replace', index=False)

    # Crea un archivo dummy para indicar que la tarea se ha completado correctamente
    with open('databaseOK.txt', 'w') as f:
        f.write('OK')