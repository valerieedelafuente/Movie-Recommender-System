import pandas as pd

def preprocessing(dataframe):
    
    # Select columns
    dataframe = dataframe[['movie_id', 'author', 'user_rating']]
    
    ## more data preprocessing 
    
    return dataframe


movie_reviews_df = preprocessing(movie_reviews_df)
