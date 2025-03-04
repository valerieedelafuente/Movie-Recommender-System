import requests

API_KEY = "d3e8d7fcb94be031986259192b4fdfb0"
url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1"

response = requests.get(url)

if response.status_code == 200:
    movies = response.json()["results"]
    print("Get movie data successfully! Top 5 popular movies:")
    for movie in movies[:5]:
        print(movie["title"])
else:
    print("Request failed, error code:", response.status_code)

