# preprocessing.py
import pandas as pd
import numpy as np
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def prepare_dataframe(movies_path, credits_path):
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    movies = movies[['genres','keywords','overview','title']]
    movies = movies.merge(credits, on='title')
    movies = movies.dropna()

    def convert(obj):
        obj_list = []
        for i in ast.literal_eval(obj):
            obj_list.append(i['name'])
        return obj_list

    movies['keywords'] = movies['keywords'].apply(convert)
    movies['genres'] = movies['genres'].apply(convert)

    def fetch_director(obj):
        director_list = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                director_list.append(i['name'])
                break
        return director_list

    movies['crew'] = movies['crew'].apply(fetch_director)

    def convert_cast(obj):
        cast_list = []
        counter = 0
        for i in ast.literal_eval(obj):
            counter += 1
            if counter <= 3:
                cast_list.append(i['name'])
            else:
                break
        return cast_list

    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['overview'] = movies['overview'].apply(lambda x:x.split())
    movies['cast'] = movies['cast'].apply(lambda x : [i.replace(' ','') for i in x])
    movies['crew'] = movies['crew'].apply(lambda x : [i.replace(' ','') for i in x])
    movies['genres'] = movies['genres'].apply(lambda x : [i.replace(' ','') for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x : [i.replace(' ','') for i in x])
    movies['tags'] = movies['keywords'] + movies['genres'] + movies['cast'] + movies['crew']

    df = movies[['title','tags']]

    ps = PorterStemmer()

    def stem_words(obj):
        return ' '.join([ps.stem(i) for i in obj])

    df['tags'] = df['tags'].apply(stem_words)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vectors)

    return df, similarity
