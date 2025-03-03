import requests
import pandas as pd
import time

api_key = "d3e8d7fcb94be031986259192b4fdfb0"

# Base URLs
url = "https://api.themoviedb.org/3/movie/popular"
credits_url_template = "https://api.themoviedb.org/3/movie/{}/credits"
providers_url_template = "https://api.themoviedb.org/3/movie/{}/watch/providers"

total_pages = 100
all_movies = []

for page in range(1, total_pages + 1):
    parameters = {"api_key": api_key, "page": page}
    response = requests.get(url, params=parameters)
    
    if response.status_code == 200:
        data = response.json()
        movies = data["results"]
        
        for movie in movies:
            movie_id = movie["id"]
            
            # Get cast names
            credits_url = credits_url_template.format(movie_id)
            credits_response = requests.get(credits_url, params={"api_key": api_key})
            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                cast_names = {cast_member["name"] for cast_member in credits_data.get("cast", [])}  # Use a set for uniqueness
                movie["cast_names"] = ", ".join(cast_names)  # Convert to comma-separated string
            else:
                movie["cast_names"] = None
            
            # Get watch providers
            providers_url = providers_url_template.format(movie_id)
            providers_response = requests.get(providers_url, params={"api_key": api_key})
            if providers_response.status_code == 200:
                providers_data = providers_response.json()
                provider_names = set()  # Store unique provider names
                
                for region, provider_info in providers_data.get("results", {}).items():
                    for category, providers_list in provider_info.items():
                        if isinstance(providers_list, list):
                            provider_names.update(provider["provider_name"] for provider in providers_list)
                
                movie["watch_providers"] = ", ".join(provider_names)
            else:
                movie["watch_providers"] = None
            
            time.sleep(0.2)  # Short delay to avoid rate limiting
        
        all_movies.extend(movies)
    else:
        print("Error:", response.status_code)
    
    time.sleep(0.5)
    
# Convert to DataFrame
movies_df = pd.DataFrame(all_movies)

# Checking for missing data
missing_data = movies_df.isnull().sum()
print(missing_data)

# Display the first few rows
print(movies_df[["title", "cast_names", "watch_providers"]].head())
