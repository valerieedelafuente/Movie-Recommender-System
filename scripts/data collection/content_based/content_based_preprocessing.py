import pandas as pd
import ast

movie_content_df = pd.read_csv('/Users/tessivinjack/Downloads/movie_content_df.csv')
movie_content_df['genre_ids'] = movie_content_df['genre_ids'].apply(ast.literal_eval)

def genre_preprocessing(dataframe):
    # Map genre_ids to genre names
    dataframe['genre_ids'] = dataframe['genre_ids'].apply(lambda x: [genre_dict[genre_id] for genre_id in x])
    
    return dataframe


movie_content_df = genre_preprocessing(movie_content_df)
movies_df = genre_preprocessing(movies_df)


def columns_preprocessing_content(dataframe):
      dataframe = dataframe[['movie_id', 'title', 'release_date', 'genre_ids', 'original_language', 'cast_names', 'watch_providers', 'rating_average', 'vote_count']]
      
      return dataframe
    
def columns_preproccesing_collab(dataframe):
      dataframe = dataframe[['id', 'title', 'release_date', 'genre_ids', 'original_language', 'vote_count']]
      
      return dataframe

    
movie_content_df = columns_preprocessing_content(movie_content_df)
movies_df = columns_preproccesing_collab(movies_df)

