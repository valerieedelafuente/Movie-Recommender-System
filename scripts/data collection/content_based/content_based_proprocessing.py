import pandas as pd

def preprocessing(dataframe):
    # Map genre_ids to genre names
    dataframe['genre_ids'] = dataframe['genre_ids'].apply(lambda x: [genre_dict[genre_id] for genre_id in x])
    
    # Select columns
    dataframe = dataframe[['id', 'title', 'release_date', 'genre_ids', 'original_language', 'cast_names', 'watch_providers', 'vote_average']]
    
    ## more data preprocessing 
    
    return dataframe


movies_df = preprocessing(movies_df)
