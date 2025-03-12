import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import random
import numpy as np

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

### Stop running here and skip to bottom to run ###

# Test it with one movie
query_no = np.random.choice(movies_pivot.shape[0])
distances, indices = knn.kneighbors(movies_pivot.iloc[query_no,:].values.reshape(1, -1), n_neighbors = 6)

# Format recommendations
num = []
name = []
distance = []
rating = []

for i in range(0, len(distances.flatten())):
    if i == 0:
        print(f"Recommendations for {movies_pivot.index[query_no]} viewers :\n")
    else:
        movie_name = movies_pivot.index[indices.flatten()[i]]
        print(f"{i}: {movie_name} , with a distance of {distances.flatten()[i]}")        
        num.append(i)
        name.append(movie_name)
        distance.append(distances.flatten()[i])
        rating.append(*movies_copy[movies_copy["title"]==movies_pivot.index[indices.flatten()[i]]]["user_rating"].values)


# Put into DataFrame
dic = {"Number" : num, "Movie Name" : name, "Rating" : rating}
recommendation = pd.DataFrame(data = dic)
recommendation.set_index("Number", inplace = True)

title = movies_pivot.index[query_no]

# Create function for collaborative recs
def collaborative_recommender(title, num_recs = 10):
    # Make a copy of the movies dataframe to avoid modifying the original
    movies_copy = movies_df.copy()
    # Create a pivot table where rows are movie titles and columns are user IDs
    movies_pivot = movies_copy.pivot_table(index="title", columns="user_id", values="user_rating").fillna(0)
    # Create the compressed sparse row (CSR) matrix for the KNN model
    movies_matrix = csr_matrix(movies_pivot.values)
    # Fit the KNN model with cosine similarity
    knn = NearestNeighbors(metric="cosine", algorithm="brute")
    knn.fit(movies_matrix)
    # Get the index of the movie in the pivot table
    query_no = movies_pivot.index.get_loc(title)
    # Get the nearest neighbors (movies similar to the input movie)
    distances, indices = knn.kneighbors(movies_pivot.iloc[query_no,:].values.reshape(1, -1), n_neighbors=num_recs)
    # Initialize lists to store the recommendations
    num = []
    name = []
    distance = []
    rating = []
    # Format the recommendations
    for i in range(0, len(distances.flatten())):
        if i == 0:
            print(f"Recommendations for {title} viewers:\n")
        else:
            movie_name = movies_pivot.index[indices.flatten()[i]]
            print(f"{i}: {movie_name} , with a distance of {distances.flatten()[i]}")        
            num.append(i)
            name.append(movie_name)
            distance.append(distances.flatten()[i])
            rating.append(*movies_copy[movies_copy["title"] == movie_name]["user_rating"].values)
    # Create a DataFrame to return the recommendations
    dic = {"Number": num, "Movie Name": name, "Rating": rating, "Distance": distance}
    recommendation = pd.DataFrame(data=dic)
    recommendation.set_index("Number", inplace=True)
    return recommendation





# New collab funct with new data










# Create function for collaborative recs
def item_based_recommender(title, num_recs=10):
    if title not in movies_pivot.index:
        return f"Movie '{title}' not found in the dataset."

    query_idx = movies_pivot.index.get_loc(title)
    distances, indices = knn.kneighbors(movies_pivot.iloc[query_idx, :].values.reshape(1, -1), n_neighbors=num_recs + 1)

    recommendations = []
    for i in range(1, len(indices.flatten())):  # Skip the first (it’s the movie itself)
        movie_name = movies_pivot.index[indices.flatten()[i]]
        avg_rating = movies_merged[movies_merged["title"] == movie_name]["user_rating"].mean()
        recommendations.append((movie_name, avg_rating, distances.flatten()[i]))

    return pd.DataFrame(recommendations, columns=["Movie Name", "Avg Rating", "Distance"]).set_index("Movie Name")

