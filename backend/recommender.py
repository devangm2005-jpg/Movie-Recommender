import os
from preprocessing import prepare_dataframe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df, similarity = prepare_dataframe(
    os.path.join(BASE_DIR, "data/tmdb_5000_movies.csv"),
    os.path.join(BASE_DIR, "data/tmdb_5000_credits.csv")
)

def recommend(movie_name):
    movie_name = movie_name.lower()

    titles = df['title'].str.lower()

    if movie_name not in titles.values:
        return []

    movie_index = titles[titles == movie_name].index[0]

    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [df.iloc[i[0]].title for i in movies_list]
