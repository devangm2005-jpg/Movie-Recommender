import os
import pandas as pd
import ast
from nltk.stem.porter import PorterStemmer

# Absolute path of backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ps = PorterStemmer()


def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]


def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []


def convert_cast(obj):
    return [i['name'] for i in ast.literal_eval(obj)[:3]]


def stem_words(words):
    return " ".join([ps.stem(word) for word in words])


def prepare_dataframe(movies_path, credits_path):
    # FIX: absolute paths
    movies_path = os.path.join(BASE_DIR, movies_path)
    credits_path = os.path.join(BASE_DIR, credits_path)

    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    for col in ['genres', 'keywords', 'cast', 'crew']:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    movies['tags'] = movies['tags'].apply(stem_words)

    return movies[['movie_id', 'title', 'tags']]
