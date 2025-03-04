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

# Checking for missing data
missing_data = movies_df.isnull().sum()
print(missing_data)

# Optional: convert movie_df to csv file
# Convenient for me to watch columns
#movies_df.to_csv('movies_df.csv', index=False)
#movies_df.to_csv('~/Desktop/Pstat134/movies_df.csv', index=False)

