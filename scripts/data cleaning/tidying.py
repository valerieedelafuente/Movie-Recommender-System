import pandas as pd
import pycountry # for languages convertion
import pandas as pd


# Tidying genre_IDs 
def clean_genre_ids(value):
    if isinstance(value, list):  # If it's already a list, clean and join
        return ', '.join(genre.strip() for genre in value)
    elif isinstance(value, str) and value.startswith('c(') and value.endswith(')'):
        # Handle string cases formatted like R's "c(...)"
        genres = [genre.strip().strip('"') for genre in value[2:-1].split(',')]
        return ', '.join(genres)
    return value  # Return as is if neither case

    # Apply the function to genre_ids column
movies_df['genre_ids'] = movies_df['genre_ids'].apply(clean_genre_ids)
    # Check genre_ids missing and type
movies_df['genre_ids'].isna().sum() # No missing data
movies_df['genre_ids'].apply(type).value_counts() # All are string type


# Tidying original language to be full word
def convert_language_code(code):
    try:
        language = pycountry.languages.get(alpha_2=code)
        return language.name
    except:
        return code  # no corresponding language, return original language code
      
movies_df['original_language'] = movies_df['original_language'].apply(convert_language_code)


# Popularity, vote average, vote count
    """
    Popularity: Calculated based on a variety of factors.
                Number of views, downloads, number of positive and negative feedback......
                Used to measure the popularity or current attention of a movie.
  
    Vote average: Average of all user ratings, on a scale of 1 to 10.
                  A quantitative assessment of the overall quality of a movie.
    
    Vote count: The total number of people who voted for the movie.
                The more votes there are, the more reliable the average score is.
    """
    
    # Data type
movies_df['popularity'] = pd.to_numeric(movies_df['popularity'], errors='coerce')
movies_df['vote_average'] = pd.to_numeric(movies_df['vote_average'], errors='coerce')
movies_df['vote_average'] = movies_df['vote_average'].round(0).astype(int) # vote_average to round
movies_df['vote_count'] = pd.to_numeric(movies_df['vote_count'], errors='coerce')

    # Statistics for popularity, vote average, and vote count
print(movies_df[['popularity', 'vote_average', 'vote_count']].describe())


# Creating a `release_year` column
movies_df = movies_df.copy()  # Ensure movies_df is a separate DataFrame

#code created by Leslie
movies_df["release_date"] = movies_df["release_date"].astype(str)
movies_df = movies_df[movies_df["release_date"] != '']
movies_df["release_year"] = pd.to_numeric(movies_df["release_date"].str[:4], errors = "coerce")

#movies_df["release_year"] = movies_df["release_date"].astype(str).str[:4].astype(int)
movies_df = movies_df.drop(columns=["release_date"])


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


# Making user ratings uniform
  # Convert to numeric values (coerce invalid entries to NaN)
#movies_df["user_rating"] = pd.to_numeric(movies_df["user_rating"], errors="coerce")
  # Replace NaN with 0 or any other value of choice, before converting to integers
#movies_df["user_rating"] = movies_df["user_rating"].fillna(0).round().astype(int)


# Changing the `title` type
  # Convert to pandas' new string type
movies_df["title"] = movies_df["title"].astype("string")
  # Check the dtype again
print(movies_df["title"].dtype)


# Tidying `popularity`
movies_df.loc[:, "popularity"] = movies_df["popularity"].round(0).astype(int)


# Reordering column names
  # Define the new column order
new_column_order = ['id', 'title', 'release_year', 'genre_ids', 'original_language', 'cast_names', 'watch_providers', 'popularity', 'vote_average', 'vote_count', 'user_name', 'user_id', 'user_rating']
# Reorganize columns in the DataFrame
movies_df = movies_df[new_column_order]


