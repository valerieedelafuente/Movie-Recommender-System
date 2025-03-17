import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import random
import numpy as np
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# content based filtering below 

movie_content_df = pd.read_csv('/Users/tessivinjack/Documents/GitHub/Pstat134-Movie-Recommender-System/data/movie_content_processed.csv')
movie_content_df["combined_features"] = (
    movie_content_df["genre_ids"].apply(lambda x: " ".join(x) if isinstance(x, list) else "") + " | " + 
    movie_content_df["cast_names"].fillna("").str.replace(",", " ") + " | " +  
    movie_content_df["watch_providers"].fillna("").str.replace(",", " ")
)

tfidf_vectorizer = TfidfVectorizer(stop_words="english", min_df=2)
tfidf_matrix = tfidf_vectorizer.fit_transform(movie_content_df["combined_features"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def content_based_movie_recs(movie_title, movie_content_df, cosine_sim, top_n=10):
    # preprocess input: remove space and lowercase
    clean_title = movie_title.strip().lower()

    # preprocess movie title
    movie_content_df["clean_title"] = movie_content_df["title"].str.strip().str.lower()

    # find the most similar movie
    possible_matches = get_close_matches(clean_title, movie_content_df["clean_title"], n=1, cutoff=0.7)
    
    if possible_matches:
        clean_title = possible_matches[0]
    
    movie_idx = movie_content_df[movie_content_df["clean_title"] == clean_title].index

    if movie_idx.empty:
        return f"Movie '{movie_title.strip()}' not found. Please check the title."

    movie_idx = movie_idx[0]
   
    similarity_scores = list(enumerate(cosine_sim[movie_idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
   
    top_movies = similarity_scores[1:top_n+1]
    
    recommendations = movie_content_df.iloc[[i[0] for i in top_movies]][["movie_id", "title", "genre_ids", "rating_average", "watch_providers"]]

    # Add the input movie itself to the recommendations (if not already present)
    input_movie_row = movie_content_df.iloc[[movie_idx]][["movie_id", "title", "genre_ids", "rating_average", "watch_providers"]]
    recommendations = pd.concat([input_movie_row, recommendations], ignore_index=True)
    
    return recommendations
  

content_based_movie_recs('Funny Games', movie_content_df, cosine_sim, top_n=100)
  
  
  
  
  
# collaborative based recs below
movie_reviews_df = pd.read_csv("/Users/tessivinjack/Downloads/movie_reviews_data.csv")

def collaborative_based_movie_recs(title, movies_pivot, movies_merged, knn, num_recs=10):
    # Check if movie is within dataset
    if title not in movies_pivot.index:
        return f"Movie '{title}' not found in the dataset."
      
    # List only popular streaming services to include
    popular_streaming_services = [
    'Netflix', 'Amazon Prime Video', 'Hulu', 'Disney+', 'Apple TV', 'HBO Max', 
    'YouTube', 'Google Play Movies', 'Peacock', 'Paramount+',
    'Max', 'Mubi', 'Amazon Video', 'Netflix basic with Ads', 'Hoopla', 'Vudu']
    
    # Get index of movie to get recommendations for
    query_idx = movies_pivot.index.get_loc(title)
    
    # Given KNN model, find top 10 most similar movies based on user ratings
    distances, indices = knn.kneighbors(movies_pivot.iloc[query_idx, :].values.reshape(1, -1), n_neighbors=num_recs + 1)
    
    recommendations = []
    for i in range(1, len(indices.flatten())):  # Skip the first movie (it's itself)
        # Extract movie name and information
        movie_name = movies_pivot.index[indices.flatten()[i]]
        movie_info = movie_content_df[movie_content_df['movie_id'] == movies_merged[movies_merged['title'] == movie_name]['movie_id'].iloc[0]]
        
        # Check that the movie exists in content DataFrame
        if not movie_info.empty:
            # Extract movie rating and genres
            avg_rating = movie_info['rating_average'].iloc[0]
            genre_ids = movie_info['genre_ids'].iloc[0]
            # Convert genre ids to lists and join to make a string
            if isinstance(genre_ids, str):
                genre_ids = eval(genre_ids)
            genre_str = ", ".join(genre_ids)
            
            # Collect watch provider information for each movie
            watch_providers = movie_info['watch_providers'].iloc[0]
            # Format info so it only contains the popular streaming services
            if isinstance(watch_providers, float):
              watch_providers = ""
            filtered_watch_providers = [provider.strip() for provider in watch_providers.split(',') 
                            if any(popular.lower() in provider.lower() for popular in popular_streaming_services)]
            formatted_watch_providers = ", ".join(filtered_watch_providers)
            # Add all information to list of recommendations
            recommendations.append((movie_name, genre_str, avg_rating, formatted_watch_providers))
    
    print(f"🎬 Using matched movie: {title}\n")
    print(f"📌 Top {num_recs} movies similar to '{title}':")
    
    # Print out movie information for each recommendation in formatted way
    for i, (movie_name, genre, rating, watch_providers) in enumerate(recommendations, start=1):
        print(f"{i}. {movie_name} (Genre: {genre}, Rating: {rating})")
        print(f"   📺 Where to stream: {watch_providers}")
        print()


# final hybrid recommender below




def final_movie_recs(title):
  # Retrieve top 100 content based recommendations
  top_100_movies = content_based_movie_recs(title, movie_content_df, cosine_sim, top_n=101)
  
  # List only popular streaming services to include
  popular_streaming_services = [
    'Netflix', 'Amazon Prime Video', 'Hulu', 'Disney+', 'Apple TV', 'HBO Max', 
    'YouTube', 'Google Play Movies', 'Peacock', 'Paramount+',
    'Max', 'Mubi', 'Amazon Video', 'Netflix basic with Ads', 'Hoopla', 'Vudu']
      
  # Extract row with movie content for given movie
  movie_row = movie_content_df[movie_content_df["title"] == title]
  
  # Check if movie exists in content DataFrame
  if not movie_row.empty:
    # Add movie to top 100 DataFrame so that this can be fed into other recommender
    top_100_movies = pd.concat([top_100_movies, movie_row], ignore_index=True)
  # If movie does not exist in contet DataFrame, let user know
  elif movie_row.empty:
    return f"Movie '{title}' not found in the dataset."
  
  # Extract specific movie id
  movie_id = movie_row["movie_id"].values[0] if not movie_row.empty else None
  
  # Check if movie does not have reviews in the reviews DataFrame
  if movie_id not in movie_reviews_df["movie_id"].values:
      # Extract movie id and title of given movie
      input_movie_id = movie_row["movie_id"].values[0]
      input_movie_title = movie_row["title"].values[0]
      
      # Remove the given movie from top 100 movies DataFrame
      top_100_movies = top_100_movies[
            (top_100_movies["movie_id"] != input_movie_id) & 
            (top_100_movies["title"] != input_movie_title)]
      
      print(f"🎬 Using matched movie: {input_movie_title}\n")
      print(f"📌 Top 10 movies similar to '{input_movie_title}':")
      
      # Format and print top 10 rows of the top 100 DataFrame
      for counter, (i, row) in enumerate(top_100_movies.head(10).iterrows(), 1):
        # Extract genre id for each movie
        genres = row['genre_ids']
        # If genre is a string, convert to list and format to joined string for printing
        if isinstance(genres, str):
            genres = eval(genres)
        genres = ', '.join(genres)
        print(f"{counter}. {row['title']} (Genre: {genres}, Rating: {row['rating_average']:.2f})")
        
        # Select and format only the popular watch providers
        available_providers = [provider for provider in row['watch_providers'].split(', ') if provider in popular_streaming_services]
        
        # Print out all available streaming services
        if available_providers:
            print(f"   📺 Where to stream: {', '.join(available_providers)}")
        print()
  
  # If movie does have reviews in the reviews DataFrame
  else:
    # Select all unique movies in the top 100 content based recommendations
    movie_ids_set = set(top_100_movies["movie_id"])
    # Subset movies_df to include only the top 100 movies 
    movies_subset = movies_df[movies_df["id"].isin(movie_ids_set)]
    # Subset movie_reviews_df to incude only the top 100 movies
    reviews_subset = movie_reviews_df[movie_reviews_df["movie_id"].isin(movie_ids_set)]
    # Merge both subsetted DataFrames: movies and their reviews
    movies_merged = movies_subset.merge(reviews_subset, left_on="id", right_on="movie_id")
    
    # Pivot the merged table so that rows are movies, columns are users, values are those users ratings
    movies_pivot = movies_merged.pivot_table(index="title",columns="id",values="user_rating").fillna(0)
    
    # Create Compressed Sparse Row (CSR) matrix of pivoted table
    movies_matrix = csr_matrix(movies_pivot.values)
    
    # Fit KNN model with cosine similarity as distance metric
    knn = NearestNeighbors(metric = "cosine", algorithm = "brute")
    knn.fit(movies_matrix)
    
    # Run top 100 recs through collaborative recommender to get top 10 recommendations
    final_recommendations = collaborative_based_movie_recs(title, movies_pivot, movies_merged, knn, num_recs=10)
    
    return final_recommendations

final_movie_recs("Companion")


#################


collab_ids = set(movies_df["id"])
content_ids = set(movie_content_df["movie_id"])
review_ids = set(movie_reviews_df["movie_id"])
missing_in_content = collab_ids - content_ids
missing_in_collab = content_ids - collab_ids
missing_in_review = collab_ids - review_ids





