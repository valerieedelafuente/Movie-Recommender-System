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
    if title not in movies_pivot.index:
        return f"Movie '{title}' not found in the dataset."
      
    popular_streaming_services = [
    'Netflix', 'Amazon Prime Video', 'Hulu', 'Disney+', 'Apple TV', 'HBO Max', 
    'YouTube', 'Google Play Movies', 'Peacock', 'Paramount+',
    'Max', 'Mubi', 'Amazon Video', 'Netflix basic with Ads', 'Hoopla', 'Vudu']
    
    query_idx = movies_pivot.index.get_loc(title)
    #print('out here at query index', query_idx)
    distances, indices = knn.kneighbors(movies_pivot.iloc[query_idx, :].values.reshape(1, -1), n_neighbors=num_recs + 1)

    #print('made it out here')
    
    #print(f"indices.flatten(): {indices.flatten()}")
    #print(f"movies_pivot.shape: {movies_pivot.shape}")

    
    recommendations = []
    for i in range(1, len(indices.flatten())):  # Skip the first (it’s the movie itself)
        movie_name = movies_pivot.index[indices.flatten()[i]]
        #print('movie name', movie_name)
        #print('merged title', movies_merged[movies_merged['title'] == movie_name])
        
        movie_info = movie_content_df[movie_content_df['movie_id'] == movies_merged[movies_merged['title'] == movie_name]['movie_id'].iloc[0]]
        #print('movie info', movie_info)
        if not movie_info.empty:
            avg_rating = movie_info['rating_average'].iloc[0]
            genre_ids = movie_info['genre_ids'].iloc[0]
            #genre_ids = ast.literal_eval(genre_ids)
            if isinstance(genre_ids, str):
                genre_ids = eval(genre_ids)
            genre_str = ", ".join(genre_ids)
            watch_providers = movie_info['watch_providers'].iloc[0]
            if isinstance(watch_providers, float):
              watch_providers = ""
            filtered_watch_providers = [provider.strip() for provider in watch_providers.split(',') 
                            if any(popular.lower() in provider.lower() for popular in popular_streaming_services)]
            formatted_watch_providers = ", ".join(filtered_watch_providers)
            recommendations.append((movie_name, genre_str, avg_rating, formatted_watch_providers))
    print(f"🎬 Using matched movie: {title}\n")
    print(f"📌 Top {num_recs} movies similar to '{title}':")

    for i, (movie_name, genre, rating, watch_providers) in enumerate(recommendations, start=1):
        print(f"{i}. {movie_name} (Genre: {genre}, Rating: {rating})")
        print(f"   📺 Where to stream: {watch_providers}")
        print()


# final hybrid recommender below




def final_movie_recs(title):
  #print(movie_content_df[movie_content_df["title"] == title])
  top_100_movies = content_based_movie_recs(title, movie_content_df, cosine_sim, top_n=101)
  #print(top_100_movies)
  #print(top_100_movies.columns)
  
  popular_streaming_services = [
    'Netflix', 'Amazon Prime Video', 'Hulu', 'Disney+', 'Apple TV', 'HBO Max', 
    'YouTube', 'Google Play Movies', 'Peacock', 'Paramount+',
    'Max', 'Mubi', 'Amazon Video', 'Netflix basic with Ads', 'Hoopla', 'Vudu']
      
  movie_row = movie_content_df[movie_content_df["title"] == title]
  #print(movie_row)
  if not movie_row.empty:
    top_100_movies = pd.concat([top_100_movies, movie_row], ignore_index=True)
    #top_100_movies = top_100_movies[['movie_id', 'title', 'genre_ids', 'rating_average']]
    #print('top 100', top_100_movies) # prints rec movie twice so has 102 rows
  elif movie_row.empty:
    return f"Movie '{title}' not found in the dataset."
  
  movie_id = movie_row["movie_id"].values[0] if not movie_row.empty else None
  #print('movie idddd', movie_id)
  if movie_id not in movie_reviews_df["movie_id"].values:
      input_movie_id = movie_row["movie_id"].values[0]
      
      input_movie_title = movie_row["title"].values[0]
      top_100_movies = top_100_movies[
            (top_100_movies["movie_id"] != input_movie_id) & 
            (top_100_movies["title"] != input_movie_title)]
      #print(top_100_movies.head(10))
      #return top_100_movies.head(10)
      
      print(f"🎬 Using matched movie: {input_movie_title}\n")
      print(f"📌 Top 10 movies similar to '{input_movie_title}':")
      
      for counter, (i, row) in enumerate(top_100_movies.head(10).iterrows(), 1):
        #genres = ', '.join(row['genre_ids'])
        genres = row['genre_ids']
        if isinstance(genres, str):
            genres = eval(genres)
        genres = ', '.join(genres)
        print(f"{counter}. {row['title']} (Genre: {genres}, Rating: {row['rating_average']:.2f})")
        
        available_providers = [provider for provider in row['watch_providers'].split(', ') if provider in popular_streaming_services]
        
        if available_providers:
            print(f"   📺 Where to stream: {', '.join(available_providers)}")
        print()
  
  else:
    movie_ids_set = set(top_100_movies["movie_id"])
    #print(8461 in movie_ids_set)
    movies_subset = movies_df[movies_df["id"].isin(movie_ids_set)]
    #print(movies_subset)
    reviews_subset = movie_reviews_df[movie_reviews_df["movie_id"].isin(movie_ids_set)]
    #print(reviews_subset[reviews_subset["movie_id"] == 10234])
    
    movies_merged = movies_subset.merge(reviews_subset, left_on="id", right_on="movie_id")
    #print(movies_merged[movies_merged['id'] == 334])
    #print(movies_merged)
    #print(movies_merged.columns)
    
    movies_pivot = movies_merged.pivot_table(index="title",columns="id",values="user_rating").fillna(0)
    #print(movies_pivot)
    #print('Anora' in movies_pivot.index)
    
    # Create Compressed Sparse Row (CSR) matrix
    movies_matrix = csr_matrix(movies_pivot.values)
    
    # Fit KNN model with cosine similarity as distance metric
    knn = NearestNeighbors(metric = "cosine", algorithm = "brute")
    knn.fit(movies_matrix)
    
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





