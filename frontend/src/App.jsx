import { useState } from 'react'
import './App.css'

function App() {
  const [movie, setMovie] = useState('')
  const [recommendations, setRecommendations] = useState([])
  const [error, setError] = useState('')

  const getRecommendations = async () => {
    if (!movie.trim()) {
      setError('Please enter a movie name')
      setRecommendations([])
      return
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/recommend?movie=${movie}`
      )

      const data = await response.json()

      if (!response.ok) {
        setError('Please search any other movie')
        setRecommendations([])
        return
      }

      setRecommendations(data.recommendations)
      setError('')
    } catch {
      setError('Server error. Please try again later.')
      setRecommendations([])
    }
  }

  return (
    <div className="movie-app">
      <div className="container py-5">
        <h1 className="app-title text-center mb-4">🎬 Movie Recommender</h1>

        <div className="search-box mx-auto mb-4">
          <input
            type="text"
            className="form-control movie-input"
            placeholder="Search a movie..."
            value={movie}
            onChange={(e) => setMovie(e.target.value)}
          />
          <button className="btn movie-btn" onClick={getRecommendations}>
            Recommend
          </button>
        </div>

        {error && (
          <div className="alert alert-warning text-center">
            {error}
          </div>
        )}

        <div className="row justify-content-center">
          {recommendations.map((rec, index) => (
            <div key={index} className="col-md-4 col-sm-6 mb-3">
              <div className="movie-card">
                🎥 {rec}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
