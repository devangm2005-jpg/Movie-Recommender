from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import recommend

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Movie Recommender API is Running"


@app.route('/recommend', methods=['GET'])
def get_recommendations():
    movie = request.args.get('movie')

    if not movie:
        return jsonify({'error': 'Movie name is required'}), 400

    recommendations = recommend(movie)

    if not recommendations:
        return jsonify({'error': 'Movie not found'}), 404

    return jsonify({'recommendations': recommendations})


if __name__ == '__main__':
    app.run(debug=True)
