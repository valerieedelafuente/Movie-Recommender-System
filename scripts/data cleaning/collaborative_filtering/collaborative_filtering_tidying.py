movies_df = pd.read_csv("movies_data.csv")
movie_reviews_df = pd.read_csv("movie_reviews_data.csv")

# Tidying `user_id`
# Creating a `user_id` column
user_id_map = {}  # Dictionary to store author -> user_id mapping
current_id = 1

# Ensure 'user_id' column exists
movie_reviews_df["user_id"] = pd.NA  

# Get valid indices
valid_indices = movie_reviews_df["user_rating"].notna() & (movie_reviews_df["user_rating"] != "")

# Store user IDs in a list to avoid modifying DataFrame during iteration
user_ids = []

for idx, author in movie_reviews_df.loc[valid_indices, "author"].items():
    if author not in user_id_map:
        user_id_map[author] = current_id
        current_id += 1
    user_ids.append((idx, user_id_map[author]))

# Assign user IDs to the DataFrame
for idx, user_id in user_ids:
    movie_reviews_df.loc[idx, "user_id"] = user_id

# Convert `user_id` to integers (nullable type to allow NaN)
movie_reviews_df["user_id"] = movie_reviews_df["user_id"].astype("Int64")

# Drop the "author" column
movie_reviews_df = movie_reviews_df.drop(columns=["author"])
