# recommender.py
from load_data import df, similarity

def recommend(movie_name):
    movie_name = movie_name.lower()
    titles = df['title'].str.lower()

    if movie_name not in titles.values:
        return []

    movie_index = titles[titles == movie_name].index[0]

    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    return [df.iloc[i[0]].title for i in movies_list]
