# load_data.py
import pickle
import requests
from io import BytesIO

MOVIES_URL = "https://huggingface.co/datasets/Devang2005/movie-recommender-artifacts/resolve/main/movies.pkl"
SIMILARITY_URL = "https://huggingface.co/datasets/Devang2005/movie-recommender-artifacts/resolve/main/similarity.pkl"

def load_pickle(url):
    response = requests.get(url)
    response.raise_for_status()
    return pickle.load(BytesIO(response.content))

# Load once (IMPORTANT)
df = load_pickle(MOVIES_URL)
similarity = load_pickle(SIMILARITY_URL)
