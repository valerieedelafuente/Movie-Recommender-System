import pandas as pd
import ast

# Import data to preprocess
movie_content_df = pd.read_csv('data/movie_content_df.csv')
movies_df = pd.read_csv('data/movies_data.csv')


def genre_preprocessing(dataframe):
    # Convert genre_ids to lists
    dataframe['genre_ids'] = dataframe['genre_ids'].apply(ast.literal_eval)
    
    # Map genre_ids to genre names
    dataframe['genre_ids'] = dataframe['genre_ids'].apply(lambda x: [genre_dict[genre_id] for genre_id in x])
    
    return dataframe


def content_preprocessing(dataframe):
      # Format genre_ids
      dataframe = genre_preprocessing(dataframe)
    
      # Select necessary columns
      dataframe = dataframe[['movie_id', 'title', 'release_date', 'genre_ids', 'original_language', 'cast_names', 'watch_providers', 'rating_average', 'vote_count']]
      
      return dataframe
    
# Apply the preprocessing function
movie_content_df = content_preprocessing(movie_content_df)

    
def collab_preproccesing(dataframe):
      # Format genre_ids
      movies_df = genre_preprocessing(movies_df)
      
      # Select necessary columns
      dataframe = dataframe[['id', 'title', 'release_date', 'genre_ids', 'original_language', 'vote_count']]
      
      return dataframe

# Apply the preprocessing function
movies_df = collab_preproccesing(movies_df)

