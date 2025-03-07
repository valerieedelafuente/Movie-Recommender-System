# Tidying `user_id`
  # Creating a `user_id` column
user_id_map = {}  # Dictionary to store user_name -> user_id mapping
current_id = 1

valid_indices = movies_df["user_rating"].notna() & (movies_df["user_rating"] != "")

for idx in movies_df.loc[valid_indices].index:
    user_name = movies_df.at[idx, "user_name"]
    
    if user_name not in user_id_map:
        user_id_map[user_name] = current_id
        current_id += 1
    
    movies_df.at[idx, "user_id"] = user_id_map[user_name]

  # Convert `user_id` to integers
movies_df["user_id"] = movies_df["user_id"].astype("Int64")  # Keeps None as <NA>


# Tidying user_name
  #`user_name` check missing and convert to NA
movies_df['user_name'] = movies_df['user_name'].replace('', pd.NA)
movies_df['user_name'].eq('').sum()#check convert NA success or fail
