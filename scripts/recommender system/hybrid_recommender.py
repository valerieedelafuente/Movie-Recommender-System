import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import random
import numpy as np
import ast

sys.path.append("/Users/tessivinjack/Documents/GitHub/Pstat134-Movie-Recommender-System/scripts/recommender system")

from collaborative_recomender import item_based_recommender

sys.path.append("/Users/tessivinjack/Documents/GitHub/Pstat134-Movie-Recommender-System/scripts/recommender system")

from Content-Based Filtering copy import recommend_movies

from collaborative_recommender import item_based_recommender

## im giving up, collab below ##

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
def item_based_recommender(title, movies_pivot=movies_pivot, num_recs=10):
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


## content below ##

movie_content_df = pd.read_csv('/Users/tessivinjack/Documents/GitHub/Pstat134-Movie-Recommender-System/data/movie_content_processed.csv')
movie_content_df["combined_features"] = (
    movie_content_df["genre_ids"].fillna("").str.replace(",", " ") + " | " +  
    movie_content_df["cast_names"].fillna("").str.replace(",", " ") + " | " +  
    movie_content_df["watch_providers"].fillna("").str.replace(",", " ")
)

#movie_content_df["combined_features"] = (
    #movie_content_df["genre_ids"].fillna("").str.replace(",", " ") + " | " +  
    #movie_content_df["cast_names"].fillna("").str.replace(",", " ")
#)

movie_content_df["combined_features"].head()

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(stop_words="english", min_df=2)

tfidf_matrix = tfidf_vectorizer.fit_transform(movie_content_df["combined_features"])

print("TF-IDF Matrix Shape:", tfidf_matrix.shape)

from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

print("Cosine Similarity Matrix Shape:", cosine_sim.shape)
print("Sample Cosine Similarity Scores:\n", cosine_sim[:5, :5])

from difflib import get_close_matches

def recommend_movies(movie_title, movie_content_df, cosine_sim, top_n=11):
    # prepprocess input: remove space and lowercase
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

    
    recommendations = movie_content_df.iloc[[i[0] for i in top_movies]][["title", "genre_ids", "rating_average"]]

    return recommendations

def final_movie_recs(title, num_recs=num_recs):
    top_100_movies = recommend_movies(title, movie_content, cosine_sim, top_n=100)
    
    filtered_movie_titles = set(top_100_movies["title"])
    filtered_movies_pivot = movies_pivot[movies_pivot.index.isin(filtered_movie_titles)]
    filtered_movie_reviews = movie_reviews_df[movie_reviews_df["movie_id"].isin(
        movies_merged[movies_merged["title"].isin(filtered_movie_titles)]["movie_id"]
    )]

    final_recommendations = item_based_recommender(title, num_recs=10)
    return final_recommendations


