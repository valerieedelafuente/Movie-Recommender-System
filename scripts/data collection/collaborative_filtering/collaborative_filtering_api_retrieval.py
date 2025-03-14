import requests
import pandas as pd
import time

# API key for TMDb
api_key = "d3e8d7fcb94be031986259192b4fdfb0"

# Base URLs
popular_movies_url = "https://api.themoviedb.org/3/movie/popular"
reviews_url_template = "https://api.themoviedb.org/3/movie/{}/reviews"

# Number of pages to retrieve
total_pages = 200 
all_movies = []

# Fetch popular movies
for page in range(1, total_pages + 1):
    response = requests.get(popular_movies_url, params={"api_key": api_key, "page": page})
    
    if response.status_code == 200:
        movies = response.json().get("results", [])
        all_movies.extend(movies)
    else:
        print("Error:", response.status_code)
        break

    time.sleep(0.5)  # Prevent rate-limiting
    print(page)

# Convert movies to DataFrame
movies_df = pd.DataFrame(all_movies)
movies_df_uncleaned = movies_df.copy()
movies_df_uncleaned.to_csv("movies_data_uncleaned.csv", index=False)
movies_df = pd.DataFrame(all_movies)[['id', 'title']]


# Fetch reviews for each movie
reviews_data = []

timeout_duration = 0.5

for movie_id in movies_df["id"]:
    response = requests.get(reviews_url_template.format(movie_id), params={"api_key": api_key})
    
    if response.status_code == 200:
        reviews = response.json().get("results", [])
        for review in reviews:
            reviews_data.append({
                "movie_id": movie_id,
                "author": review.get("author", "Unknown"),
                "user_rating": review.get("author_details", {}).get("rating", None)  # Changed "rating" to "user_rating"
            })
    else:
        print("Error:", response.status_code)

    time.sleep(0.5)

# Convert reviews to DataFrame
movie_reviews_df = pd.DataFrame(reviews_data)


# Fetch reviews for each movie
reviews_data = []

timeout_duration = 0.5

for movie_id in movies_df["id"]:
    try:
        response = requests.get(reviews_url_template.format(movie_id), params={"api_key": api_key}, timeout=timeout_duration)
        if response.status_code == 200:
            reviews = response.json().get("results", [])
            for review in reviews:
                reviews_data.append({
                    "movie_id": movie_id,
                    "author": review.get("author", "Unknown"),
                    "user_rating": review.get("author_details", {}).get("rating", None)  # Changed "rating" to "user_rating"
                })
        else:
            print("Error:", response.status_code)
    except requests.exceptions.Timeout:
        print(f"Request for movie {movie_id} reviews timed out.")
        break  # Or handle it in another way

    time.sleep(0.5)
    

# Convert reviews to DataFrame
movie_reviews_df = pd.DataFrame(reviews_data)


# Save both dataframes
movies_df.to_csv("movies_data.csv", index=False)
movie_reviews_df.to_csv("movie_reviews_data.csv", index=False)
