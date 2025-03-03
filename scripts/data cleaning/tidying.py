import pandas as pd
import pycountry # for languages convertion


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


# Tidy original language to be full word
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
    
    # Statistics for popularity, vote average, and vote count
print(movies_df[['popularity', 'vote_average', 'vote_count']].describe())

    # Data type
movies_df['popularity'] = pd.to_numeric(movies_df['popularity'], errors='coerce')
movies_df['vote_average'] = pd.to_numeric(movies_df['vote_average'], errors='coerce')
movies_df['vote_count'] = pd.to_numeric(movies_df['vote_count'], errors='coerce')


# Creating a `user_id` column
valid_indices = movies_df["user_rating"].notna() & (movies_df["user_rating"] != "")
movies_df.loc[valid_indices, "user_id"] = range(1, valid_indices.sum() + 1)

# Convert user_id to integers
movies_df["user_id"] = movies_df["user_id"].astype("Int64")  # Keeps None as <NA>


# Making user ratings uniform
  # Convert to numeric values (coerce invalid entries to NaN)
movies_df["user_rating"] = pd.to_numeric(movies_df["user_rating"], errors="coerce")
  # Replace NaN with 0 or any other value of choice, before converting to integers
movies_df["user_rating"] = movies_df["user_rating"].fillna(0).round().astype(int)


# Changing the `title` type
  # Convert to pandas' new string type
movies_df["title"] = movies_df["title"].astype("string")
  # Check the dtype again
print(movies_df["title"].dtype)
