import pandas as pd
import ast
# Dont need this file...

# Load dataframes
movies_df = pd.read_csv("data/movies_data.csv")
movie_reviews_df = pd.read_csv("data/movie_reviews_data.csv")
movie_content_df = pd.read_csv('data/movie_content_data.csv')

# Collab 
def preprocessing(dataframe):
    
    # Select columns
    dataframe = dataframe[['movie_id', 'author', 'user_rating']]
    
    ## more data preprocessing 
    
    return dataframe

movie_reviews_df = preprocessing(movie_reviews_df)




# Content preprocessing below
movie_content_df["genre_ids"] = movie_content_df["genre_ids"].apply(ast.literal_eval)

api_key = "d3e8d7fcb94be031986259192b4fdfb0"

# Base URL for the TMDb popular movies endpoint
url = "https://api.themoviedb.org/3/genre/movie/list"

# Set parameters like the page number and API key
parameters = {
    "api_key": api_key,
    "page":1
}

# Make the GET request to fetch the data
response = requests.get(url, params=parameters)

# Check if the request was successful
if response.status_code == 200:
    genre_data = response.json()  # Convert response to JSON
    genres = genre_data["genres"]  # Extract the list of genres
    genre_dict = {genre["id"]: genre["name"] for genre in genres}  # Create dictionary
    print(genre_dict)  # Print the genre mapping

else:
    print("Error", response.status_code)

def preprocessing(dataframe):
    # Map genre_ids to genre names
    dataframe['genre_ids'] = dataframe['genre_ids'].apply(lambda x: [genre_dict[genre_id] for genre_id in x])
    
    # Select columns
    dataframe = dataframe[['movie_id', 'title', 'release_date', 'genre_ids', 'original_language', 'cast_names', 'watch_providers', 'rating_average', 'vote_count']]
    
    return dataframe


movie_content_df = preprocessing(movie_content_df)

movie_content_df.to_csv("movie_content_processed.csv", index=False)


