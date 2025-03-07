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
movie_content_df['genre_ids'] = movie_content_df['genre_ids'].apply(clean_genre_ids)
    # Check genre_ids missing and type
movie_content_df['genre_ids'].isna().sum() # No missing data
movies_content_df['genre_ids'].apply(type).value_counts() # All are string type


# Tidying original language to be full word
def convert_language_code(code):
    try:
        language = pycountry.languages.get(alpha_2=code)
        return language.name
    except:
        return code  # no corresponding language, return original language code
      
movie_content_df['original_language'] = movie_content_df['original_language'].apply(convert_language_code)


# Rating average, vote count
    """
    Rating average: Average of all user ratings, on a scale of 1 to 10.
                  A quantitative assessment of the overall quality of a movie.
    
    Vote count: The total number of people who voted for the movie.
                The more votes there are, the more reliable the average score is.
    """
    
    # Data type
movie_content_df['rating_average'] = pd.to_numeric(movie_content_df['rating_average'], errors='coerce')
movie_content_df['rating_average'] = movie_content_df['rating_average'].round(0).astype(int) # vote_average to round
movie_content_df['vote_count'] = pd.to_numeric(movie_content_df['vote_count'], errors='coerce')


# Creating a `release_year` column
movie_content_df = movie_content_df.copy()  # Ensure movies_df is a separate DataFrame
movie_content_df["release_date"] = movie_content_df["release_date"].astype(str)
movie_content_df = movies_df[movie_content_df["release_date"] != '']
movie_content_df["release_year"] = pd.to_numeric(movie_content_df["release_date"].str[:4], errors = "coerce")
#movie_content_df["release_year"] = movie_content_df["release_date"].astype(str).str[:4].astype(int)
movie_content_df = movie_content_df.drop(columns=["release_date"])


# Changing the `title` type
  # Convert to pandas' new string type
movie_content_df["title"] = movie_content_df["title"].astype("string")
  # Check the dtype again
print(movie_content_df["title"].dtype)
    
    
# Editing `cast_names`
movie_content_df["cast_names"] = movie_content_df["cast_names"].replace("", pd.NA)


# Editing `watch_providers`
movie_content_df["watch_providers"] = movie_content_df["watch_providers"].replace("", pd.NA)


# Reordering column names
  # Define the new column order
new_column_order = ['movie_id', 'title', 'release_year', 'genre_ids', 'original_language', 'cast_names', 'watch_providers', 'rating_average', 'vote_count']
# Reorganize columns in the DataFrame
movie_content_df = movie_content_df[new_column_order]
