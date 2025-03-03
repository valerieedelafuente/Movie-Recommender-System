# overview - nlp
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt') # needed for word tokenization
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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


print(movies_df.columns)
