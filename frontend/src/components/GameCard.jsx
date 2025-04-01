import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/GameCard.css';

function GameCard({ id, name, rating, tags, imageUrl }) {
  // Extract and process genre and platform arrays from string
  const formatList = (str) => {
    try {
      // Parse string to array
      const array = JSON.parse(str.replace(/'/g, '"'));
      // Select up to 3 items and join with commas
      return array.slice(0, 3).join(', ') + (array.length > 3 ? ' ...' : '');
    } catch (e) {
      // Return original string if parsing fails
      return str;
    }
  };

  // Separate genres and platforms from tags string (e.g., "[Action, RPG] • [PC, PS5]")
  const [genresStr, platformsStr] = (tags || '[] • []').split('•').map(item => item.trim());
  const genres = formatList(genresStr);
  const platforms = formatList(platformsStr);
  
  // Convert rating to number for styling
  const numericRating = parseFloat(rating) || 0;
  
  // Determine color based on score
  const getRatingColor = (score) => {
    if (score >= 85) return 'rating-excellent';
    if (score >= 70) return 'rating-good';
    if (score >= 50) return 'rating-average';
    return 'rating-poor';
  };
  
  return (
    <Link to={`/game/${id}`} className="game-card-link">
      <div className="game-card">
        <div className="game-screenshot">
          {imageUrl ? (
            <img src={imageUrl} alt={name} />
          ) : (
            <div className="placeholder-image">No Image Available</div>
          )}
        </div>
        <div className="game-info">
          <h3 className="game-name">{name}</h3>
          
          <div className={`rating ${getRatingColor(numericRating)}`}>
            <span className="rating-score">{rating}</span>
            {rating !== 'N/A' && <span className="rating-label"> / 100</span>}
          </div>
          
          <div className="game-metadata">
            {genres && (
              <div className="game-genres">
                <span className="metadata-label">Genre:</span> {genres}
              </div>
            )}
            
            {platforms && (
              <div className="game-platforms">
                <span className="metadata-label">Platform:</span> {platforms}
              </div>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}

export default GameCard;
