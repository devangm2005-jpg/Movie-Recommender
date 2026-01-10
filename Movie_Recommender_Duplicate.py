import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


# print(movies.columns,credits.columns)

movies = movies[['genres','keywords','overview','title']]

movies = movies.merge(credits,on='title')
# print(movies.columns)
# print(movies.info())

# print(movies.shape)
movies = movies.dropna()
# print(movies.shape)

def convert(obj):
    global obj_list
    obj_list = []
    for i in ast.literal_eval(obj):
        obj_list.append(i['name'])
    
    return obj_list

movies['keywords'] = movies['keywords'].apply(convert)
movies['genres'] = movies['genres'].apply(convert)


def fetch_director(obj):
    global director_list
    director_list = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            director_list.append(i['name'])
            break
    return director_list

movies['crew'] = movies['crew'].apply(fetch_director)

def convert_cast(obj):
    global cast_list 
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
# print(movies.loc[0].tags)

df = movies[['movie_id','title','tags']]
# movies = movies[['id','title','cast','crew','genres','keywords','overview']]

# df['tags'] = df['tags'].apply(lambda x : ' '.join(x))
# df['tags'] = df['tags'].apply(lambda x : x.lower())

ps = PorterStemmer()

def stemming(obj):
    global stem_list
    stem_list = []
    for i in obj:
        stem_list.append(ps.stem(i))
    return ' '.join(stem_list)

df.loc[:, 'tags'] = df['tags'].apply(stemming)

# print(df.loc[0].tags)

cv = CountVectorizer(max_features=5000,stop_words='english')
vectors  = cv.fit_transform(df['tags']).toarray()
# print(vectors)
# print(cv.get_feature_names_out())

# Calculate distance of all vectors from each other
similarity = cosine_similarity(vectors)

def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in movies_list:
        print(df.iloc[i[0]].title)

movie = input("Movie Name : ")
if movie in list(df['title']):
    recommend(movie)
else:
    print("Enter Another Movie Name")
