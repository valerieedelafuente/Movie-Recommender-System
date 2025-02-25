import requests
import pandas as pd
import time

api_key = "your_api_key"

# Base URLs
movies_url = "https://api.themoviedb.org/3/movie/popular"
credits_url_template = "https://api.themoviedb.org/3/movie/{}/credits"

total_pages = 5  # Adjust as needed
all_movies = []

for page in range(1, total_pages + 1):
    parameters = {
        "api_key": api_key,
        "page": page
    }
    
    response = requests.get(movies_url, params=parameters)
    
    if response.status_code == 200:
        data = response.json()
        movies = data["results"]
        
        for movie in movies:
            movie_id = movie["id"]
            credits_url = credits_url_template.format(movie_id)
            credits_response = requests.get(credits_url, params={"api_key": api_key})
            
            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                # Get only the first three cast members' names
                cast_names = [cast["name"] for cast in credits_data.get("cast", [])[:3]]
                movie["cast_names"] = ", ".join(cast_names)  # Store as a string
            else:
                movie["cast_names"] = None  # Handle missing cast data
            
            time.sleep(0.2)  # Small delay to avoid rate limits
        
        all_movies.extend(movies)
    else:
        print("Error:", response.status_code)

    time.sleep(0.5)  # Delay before fetching the next page

# Convert to DataFrame
movies_df = pd.DataFrame(all_movies)

# Checking for missing data
missing_data = movies_df.isnull().sum()
print(missing_data)

# Display the first few rows
print(movies_df[["title", "cast_names"]].head())
