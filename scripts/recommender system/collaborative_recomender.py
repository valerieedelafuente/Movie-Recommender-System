import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import random
import numpy as np
import ast

# Join movies_df and movie_reviews_df and clean
movies_merged = pd.merge(movies_df, movie_reviews_df, left_on='id', right_on='movie_id')
columns = ['title', 'movie_id', 'user_id', 'user_rating']
movies_merged = movies_merged[columns]

# Every row represents a movie and every column a user/reviewer
# Values are that users review/rating of the movie
movies_pivot = movies_merged.pivot_table(index="title",columns="user_id",values="user_rating").fillna(0)

# Create Compressed Sparse Row (CSR) matrix
movies_matrix = csr_matrix(movies_pivot.values)

# Fit KNN model with cosine similarity as distance metric
knn = NearestNeighbors(metric = "cosine", algorithm = "brute")
knn.fit(movies_matrix)

# Load movie content df
movie_content_processed = pd.read_csv('data/movie_content_processed.csv')
cols = ['movie_id', 'rating_average', 'genre_ids', 'watch_providers']
movie_content = movie_content_processed[cols]

# Create function for collaborative recs
def item_based_recommender(title, num_recs=10):
    if title not in movies_pivot.index:
        return f"Movie '{title}' not found in the dataset."
    
    query_idx = movies_pivot.index.get_loc(title)
    distances, indices = knn.kneighbors(movies_pivot.iloc[query_idx, :].values.reshape(1, -1), n_neighbors=num_recs + 1)

    popular_streaming_services = [
        'Netflix', 'Amazon Prime Video', 'Hulu', 'Disney+', 'Apple TV', 'HBO Max', 
        'YouTube', 'Google Play Movies', 'Peacock', 'Paramount+',
        'Max', 'Mubi', 'Amazon Video', 'Netflix basic with Ads', 'Hoopla', 'Vudu']
    
    
    recommendations = []
    for i in range(1, len(indices.flatten())):  # Skip the first (it’s the movie itself)
        movie_name = movies_pivot.index[indices.flatten()[i]]
        movie_info = movie_content[movie_content['movie_id'] == movies_merged[movies_merged['title'] == movie_name]['movie_id'].iloc[0]]
        if not movie_info.empty:
            avg_rating = movie_info['rating_average'].iloc[0]
            genre_ids = movie_info['genre_ids'].iloc[0]
            genre_ids = ast.literal_eval(genre_ids)
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

