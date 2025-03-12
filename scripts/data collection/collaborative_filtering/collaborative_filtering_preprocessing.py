import pandas as pd

# Load dataframes
movies_df = pd.read_csv("movies_data.csv")
movie_reviews_df = pd.read_csv("movie_reviews_data.csv")


def preprocessing(dataframe):
    
    # Select columns
    dataframe = dataframe[['movie_id', 'author', 'user_rating']]
    
    ## more data preprocessing 
    
    return dataframe


movie_reviews_df = preprocessing(movie_reviews_df)
