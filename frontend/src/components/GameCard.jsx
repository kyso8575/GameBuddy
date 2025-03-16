import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/GameCard.css';

function GameCard({ id, title, rating, tags, imageUrl }) {
  return (
    <Link to={`/game/${id}`} className="game-card-link">
      <div className="game-card">
        <div className="game-screenshot">
          {imageUrl ? <img src={imageUrl} alt={title} /> : 'Game Screenshot'}
        </div>
        <h3 className="game-title">{title}</h3>
        <div className="rating">⭐ {rating}</div>
        <div className="tags">{tags}</div>
      </div>
    </Link>
  );
}

export default GameCard;
