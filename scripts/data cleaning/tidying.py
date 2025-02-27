import pandas as pd
import pycountry # for languages convertion


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
def convert_language_code(code):
    try:
        language = pycountry.languages.get(alpha_2=code)
        return language.name
    except:
        return code  # no corresponding language, return original language code


movies_df['original_language'] = movies_df['original_language'].apply(convert_language_code)
print(movies_df[['original_language']].head())


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
    
    # Check missing value. Result: No missing value
print(movies_df[['popularity', 'vote_average', 'vote_count']].isnull().sum())
    # Statistics
print(movies_df[['popularity', 'vote_average', 'vote_count']].describe())
    # Data type
movies_df['popularity'] = pd.to_numeric(movies_df['popularity'], errors='coerce')
movies_df['vote_average'] = pd.to_numeric(movies_df['vote_average'], errors='coerce')
movies_df['vote_count'] = pd.to_numeric(movies_df['vote_count'], errors='coerce')

# overview - nlp
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    
    # remove punctuation and special characters, keep letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # lower-case
    text = text.lower()
    
    # token
    tokens = text.split()
    
    # remove stop word, stemming
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    # reconstruct into a string
    return " ".join(tokens)

movies_df['overview_processed'] = movies_df['overview'].apply(preprocess_text)
print(movies_df[['overview', 'overview_processed']].head())
    
