# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import recommend

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Movie Recommender API is running!"})

@app.route("/recommend")
def recommend_movie():
    movie_name = request.args.get("movie", "").strip()
    
    if not movie_name:
        return jsonify({"error": "Movie name is required"}), 400
    
    try:
        recommendations = recommend(movie_name)
        
        if not recommendations:
            return jsonify({"error": "Movie not found. Please search any other movie"}), 404
        
        return jsonify({"recommendations": recommendations})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error. Please try again later."}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
