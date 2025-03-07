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


# Vote average
    """
    Vote average: Average of all user ratings, on a scale of 1 to 10.
                  A quantitative assessment of the overall quality of a movie.
    """
    # Data type
movies_df['vote_average'] = pd.to_numeric(movies_df['vote_average'], errors='coerce')
movies_df['vote_average'] = movies_df['vote_average'].round(0).astype(int) # vote_average to round


# Creating a `release_year` column
movies_df = movies_df.copy()  # Ensure movies_df is a separate DataFrame
movies_df["release_date"] = movies_df["release_date"].astype(str)
movies_df = movies_df[movies_df["release_date"] != '']
movies_df["release_year"] = pd.to_numeric(movies_df["release_date"].str[:4], errors = "coerce")
movies_df = movies_df.drop(columns=["release_date"])


# Changing the `title` type
  # Convert to pandas' new string type
movies_df["title"] = movies_df["title"].astype("string")
  # Check the dtype again
print(movies_df["title"].dtype)


# Reordering column names
  # Define the new column order
new_column_order = ['id', 'title', 'release_year', 'genre_ids', 'original_language', 'cast_names', 'watch_providers', 'vote_average']
# Reorganize columns in the DataFrame
movies_df = movies_df[new_column_order]


