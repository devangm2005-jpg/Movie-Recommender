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
        `https://movie-recommender-70vk.onrender.com/recommend?movie=${movie}`
      )

      if (!response.ok) {
        setError('Please search any other movie')
        setRecommendations([])
        return
      }

      const data = await response.json()
      setRecommendations(data.recommendations || [])
      setError('')
    } catch {
      setError('Server error. Please try again later.')
      setRecommendations([])
    }
  }

  return (
    <div className="movie-app">
      <h1 className="app-title">🎬 Movie Recommender</h1>

      <div className="search-box">
        <input
          type="text"
          className="movie-input"
          placeholder="Search a movie..."
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
        />
        <button className="movie-btn" onClick={getRecommendations}>
          Recommend
        </button>
      </div>

      {error && <div className="alert">{error}</div>}

      <div className="row">
        {recommendations.map((rec, index) => (
          <div key={index} className="movie-card">
            🎥 {rec}
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
