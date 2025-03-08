import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap

missing_values = movie_content_df.isnull().sum()

missing_values = missing_values[missing_values > 0]
missing_values.sort_values(inplace = True)

plt.figure(figsize = (14,10))
missing_values.plot(kind = "barh", color = "green")
plt.show()

#plotting missing values for movie_content_df
plt.figure(figsize = (18,8))
sns.heatmap(movie_content_df.isnull(), cmap = "Purples")
#plt.tight_layout()
plt.xlabel('Variables')
plt.ylabel('Column Number')
plt.xticks(rotation = 80)
plt.title('Missing Values for movie_content_df')
plt.subplots_adjust(bottom = 0.25)
plt.show()

#plotting missing values for movie_reviews_df
plt.figure(figsize = (18,8))
sns.heatmap(movie_reviews_df.isnull(), cmap = "Purples")
plt.xlabel('Variables')
plt.ylabel('Column Number')
plt.title('Missing Values for movie_reviews_df')
plt.subplots_adjust(bottom = 0.25)
plt.show()

#separating genres and exploding
movie_content_df['genre_list'] = movie_content_df['genre_ids'].str.split(',')
movies_exploded = movie_content_df.explode('genre_list')

#bar chart for genre counts
genre_counts = movies_exploded['genre_list'].value_counts()
plt.figure(figsize = (12, 6))
sns.barplot(x = genre_counts.index[:10], y = genre_counts.values[:10], palette = "coolwarm")
plt.xticks(rotation = 45)
plt.xlabel('Genre')
plt.ylabel('Count')
plt.subplots_adjust(bottom = .25)
plt.show()

#countplot for languages
plt.figure(figsize = (12, 6))
sns.countplot(y = 'original_language', data = movie_content_df, order = movie_content_df['original_language'].value_counts(ascending = False).index[:15])
plt.xlabel('Count')
plt.ylabel('Language')
plt.subplots_adjust(left = .25)
plt.show()

#separating actors and exploding
movie_content_df['actors_list'] = movie_content_df['cast_names'].str.split(',')
movies_exploded = movie_content_df.explode('actors_list')

#bar chart for actor counts
actors_count = movies_exploded['actors_list'].value_counts().sort_values(ascending = False)
plt.figure(figsize = (12, 6))
sns.barplot(x = actors_count.values[:15], y = actors_count.index[:15], orient = 'h', color = "skyblue")
plt.xlabel('Count')
plt.ylabel('Actor')
plt.yticks(rotation = 0)
plt.subplots_adjust(left = .25)
plt.show()

#separating providers and exploding
movie_content_df['providers_list'] = movie_content_df['watch_providers'].str.split(',')
movies_exploded = movie_content_df.explode('providers_list')

#grouping by providers_list and taking the mean of popularity
provider_ratings = movies_exploded.groupby('providers_list')['vote_count'].mean().sort_values(ascending = False)
print(provider_ratings.head(15))

#bar chart for providers based on popularity mean 
plt.figure(figsize = (12,6))
sns.barplot(x = provider_ratings.values[:15], y = provider_ratings.index[:15], color = "pink")
plt.xlabel('Count')
plt.ylabel('Provider')
plt.title('Which providers have the highest-rated movies?')
plt.subplots_adjust(left = .35)
plt.show()

'''plt.figure(figsize = (12,6))
plt.hist(movies_exploded['vote_count'])
plt.xlim(0,500)
plt.show()'''

#vote average vs vote count
plt.figure(figsize = (12,6))
sns.barplot(x = 'rating_average', y = 'vote_count', data = movies_exploded)
plt.xlabel('Rating Average')
plt.ylabel('Vote Count')
plt.show()

#user rating
plt.figure(figsize = (12,6))
plt.hist(movie_reviews_df['user_rating'], bins = 30, color = "mediumaquamarine",edgecolor = 'black', align = 'mid')
plt.xlabel('User rating')
plt.ylabel('Count')
plt.show()

plt.figure(figsize = (12,6))
corr_matrix = movies_exploded.corr(numeric_only = True)
sns.heatmap(corr_matrix, annot = True, cmap = 'coolwarm', fmt = '.2f')
plt.subplots_adjust(left = .15, bottom = 0.15)
plt.xticks(rotation = 45)
plt.show()
