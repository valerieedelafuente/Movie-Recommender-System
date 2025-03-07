import requests
import pandas as pd
import time

api_key = "d3e8d7fcb94be031986259192b4fdfb0"

# Base URL for the TMDb popular movies endpoint
url = "https://api.themoviedb.org/3/movie/popular"

total_pages = 499
all_movies = []

for page in range(1, total_pages + 1):
  # Set parameters like the page number and API key
    parameters = {
        "api_key": api_key,
        "page": page
    }
    # Set parameters like the page number and API key
    response = requests.get(url, params = parameters)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        movies = data["results"]
        all_movies.extend(movies)
        #movies_df = pd.DataFrame(movies)
        #print(movies_df)
    else:
        print("Error", response.status_code)
      #adds small delay
    time.sleep(0.5)

#appending all_movies
movies_df = pd.DataFrame(all_movies)

