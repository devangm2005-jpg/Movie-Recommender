# recommender.py
from preprocessing import prepare_dataframe

# Load dataset once
df, similarity = prepare_dataframe(
    'data/tmdb_5000_movies.csv',
    'data/tmdb_5000_credits.csv'
)

def recommend(movie_name):
    try:
        movie_index = df[df['title'] == movie_name].index[0]
    except IndexError:
        return []  # Movie not found

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_titles = [df.iloc[i[0]].title for i in movies_list]
    return recommended_titles
