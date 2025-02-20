import pandas as pd

def preprocessing(dataframe):
    # Map genre_ids to genre names
    dataframe['genre_ids'] = dataframe['genre_ids'].apply(lambda x: [genre_dict[genre_id] for genre_id in x])
    
    # Select columns
    dataframe = dataframe[['adult', 'id', 'title', 'genre_ids', 'original_language', 'overview', 'popularity', 'release_date', 'vote_average', 'vote_count']]
    
    
    ## more data preprocessing 
    
    
    
    
    return dataframe


movies_df = preprocessing(movies_df)
movies_df.head()