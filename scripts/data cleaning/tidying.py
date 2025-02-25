import pandas as pd

# Adult column
unique_vals_adult = movies_df['adult'].unique()
print(unique_vals_adult) # Should we omit this?

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

# Omit overview?

# Popularity, vote average, vote count?

