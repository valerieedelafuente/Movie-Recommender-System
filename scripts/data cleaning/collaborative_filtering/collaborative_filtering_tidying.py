# Tidying `user_id`
# Creating a `user_id` column
user_id_map = {}  # Dictionary to store author -> user_id mapping
current_id = 1

valid_indices = movie_reviews_df["user_rating"].notna() & (movie_reviews_df["user_rating"] != "")

for idx in movie_reviews_df.loc[valid_indices].index:
    author = movie_reviews_df.at[idx, "author"]
    
    if author not in user_id_map:
        user_id_map[author] = current_id
        current_id += 1
    
    movie_reviews_df.at[idx, "user_id"] = user_id_map[author]

# Convert `user_id` to integers (nullable type to allow NaN)
movie_reviews_df["user_id"] = movie_reviews_df["user_id"].astype("Int64")

# Drop the "author" column
movie_reviews_df = movie_reviews_df.drop(columns=["author"])

