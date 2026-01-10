from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import prepare_dataframe

df = prepare_dataframe(
    'data/tmdb_5000_movies.csv',
    'data/tmdb_5000_credits.csv'
)

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()

similarity = cosine_similarity(vectors)


def recommend(movie):
    if movie not in df['title'].values:
        return []

    index = df[df['title'] == movie].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [df.iloc[i[0]].title for i in movies_list]
