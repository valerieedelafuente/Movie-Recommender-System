# Creates the dictionary of genre IDs and names
import requests
import pandas as pd

api_key = "d3e8d7fcb94be031986259192b4fdfb0"

# Base URL for the TMDb popular movies endpoint
url = "https://api.themoviedb.org/3/genre/movie/list"

# Set parameters like the page number and API key
parameters = {
    "api_key": api_key,
    "page":1
}

# Make the GET request to fetch the data
response = requests.get(url, params=parameters)

# Check if the request was successful
if response.status_code == 200:
    genre_data = response.json()  # Convert response to JSON
    genres = genre_data["genres"]  # Extract the list of genres
    genre_dict = {genre["id"]: genre["name"] for genre in genres}  # Create dictionary
    print(genre_dict)  # Print the genre mapping

else:
    print("Error", response.status_code)