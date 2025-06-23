# Hybrid Movie Recommender System using TMDb API

## Overview

This repository is a fork of a group project I contributed to for the **PSTAT 134: Statistical Data Science** course at UC Santa Barbara. The goal was to build a **hybrid movie recommendation system** using real-time data from the TMDb API. 

By combining **content-based filtering** with **collaborative filtering**, we created a personalized movie suggestion engine that mimics the structure of platforms like Netflix and Hulu.

## Repository Structure

```
├── data/
│   ├── movie_content_df.csv
│   ├── movie_content_processed.csv
│   ├── movie_reviews_data.csv
│   ├── movies_data_uncleaned.csv
│   └── movies_data.csv
│
├── results/
│   ├── Movie Recommender System Project Overview.html
│   └── Movie Recommender System Project.pdf
│
├── scripts/
│   ├── data collection/
│   │   ├── content based/
│   │   │   └── content_based_api_retrieval.py
│   │   │   └── content_based_preprocessing.py
│   │   │   └── genre_id_dict.py
│   │   └── collaborative_filtering/
│   │       └── collaborative_filtering_api_retrieval.py
│   │   │   └── collaborative_filtering_preprocessing.py
│   ├── data cleaning/
│   │   ├── content based/
│   │   │   └── content_based_tidying.py
│   │   └── collaborative_filtering/
│   │       └── collaborative_filtering_tidying.py
│   ├── eda/
│   │   └── EDA.py
│   └── recommender system/
│       └── hybrid_recommender.py
│       └── collaborative_recommender.py
│
├── README.md

```

---

## 🔧 Methods

### Data Collection
- Retrieved ~4,000 movies and ~9,600 user reviews from TMDb using API requests.
- Gathered metadata: genre, cast, release year, watch providers, language, etc.

### Data Cleaning
- Converted genre IDs and language codes into readable formats.
- Created `release_year` column and normalized rating scales.
- Handled missing values and standardized column types.

### Recommendation System
- **Content-Based**: Filters movies based on user interests and movie features.
- **Collaborative**: Matches user preferences using review patterns and ratings.
- **Cascade Hybrid**: Uses content filtering to narrow candidates, then ranks with collaborative filtering.

---

## Results

The system successfully provides high-quality recommendations even in the presence of missing review data. The hybrid cascade approach improves personalization while mitigating cold-start issues.

Full project report:  
- [HTML Overview](results/Movie%20Recommender%20System%20Project%20Overview.html)  
- [PDF Report](results/Movie%20Recommender%20System%20Project.pdf)

---

## Technologies Used

- Python (Pandas, NumPy, Scikit-learn, Requests)
- TMDb API
- Quarto / Jupyter
- Git & GitHub

---

## Authors

- Valerie De La Fuente (@valerieedelafuente)
- Jiajia Feng (@JiajiaFeng18)
- Tess Ivinjack (@tessivinjack)
- Leslie Cervantes Rivera (@lescer3)
