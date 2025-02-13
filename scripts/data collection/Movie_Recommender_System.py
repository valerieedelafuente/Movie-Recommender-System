import requests
import pandas as pd

api_key = "d3e8d7fcb94be031986259192b4fdfb0"

# Base URL for the TMDb popular movies endpoint
url = "https://api.themoviedb.org/3/movie/popular"

# Set parameters like the page number and API key
parameters = {
    "api_key": api_key,
    "page":1
}

# Make the GET request to fetch the data
response = requests.get(url, params=parameters)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  
    movies = data["results"] 
    movies_df = pd.DataFrame(movies)
    print(movies_df)

else:
    print("Error", response.status_code)

# Checking for missing data
missing_data = movies_df.isnull().sum()
print(missing_data)