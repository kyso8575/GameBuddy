import React from 'react';
import { useParams } from 'react-router-dom';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import './GameDetailPage.css';

function GameDetailPage() {
  // URL에서 게임 ID 파라미터 가져오기
  const { id } = useParams();
  
  // 실제 앱에서는 ID를 기반으로 API에서 게임 데이터를 가져올 것입니다
  // 여기서는 예시 데이터를 사용합니다
  const gameData = {
    id: id,
    title: `Game Title ${id}`,
    rating: '4.7',
    releaseDate: '2023-05-15',
    developer: 'Game Studio',
    publisher: 'Game Publisher',
    platforms: ['PC', 'PS5', 'Xbox Series X'],
    genres: ['Action', 'Adventure', 'RPG'],
    description: 'This is a detailed description of the game. It includes information about the storyline, gameplay mechanics, and features that make this game unique and enjoyable. Players will embark on an epic journey through a beautifully crafted world filled with challenges and adventures.',
    systemRequirements: {
      minimum: {
        os: 'Windows 10 64-bit',
        processor: 'Intel Core i5-6600K or AMD Ryzen 5 1600',
        memory: '8 GB RAM',
        graphics: 'NVIDIA GeForce GTX 970 or AMD Radeon RX 580',
        storage: '50 GB available space'
      },
      recommended: {
        os: 'Windows 10 64-bit',
        processor: 'Intel Core i7-8700K or AMD Ryzen 7 3700X',
        memory: '16 GB RAM',
        graphics: 'NVIDIA GeForce RTX 2070 or AMD Radeon RX 5700 XT',
        storage: '50 GB SSD'
      }
    },
    screenshots: [
      'screenshot1.jpg',
      'screenshot2.jpg',
      'screenshot3.jpg'
    ],
    videos: [
      'https://www.youtube.com/embed/example1',
      'https://www.youtube.com/embed/example2'
    ]
  };

  return (
    <div className="app">
      <NavBar />
      
      <main className="game-detail-container">
        {/* 게임 헤더 섹션 */}
        <section className="game-header">
          <div className="game-cover">
            <div className="game-cover-placeholder">Game Cover</div>
          </div>
          <div className="game-basic-info">
            <h1>{gameData.title}</h1>
            <div className="game-meta">
              <span className="rating">⭐ {gameData.rating}</span>
              <span className="release-date">Released: {gameData.releaseDate}</span>
              <span className="developer">Developer: {gameData.developer}</span>
              <span className="publisher">Publisher: {gameData.publisher}</span>
            </div>
            <div className="game-tags">
              {gameData.genres.map((genre, index) => (
                <span key={index} className="genre-tag">{genre}</span>
              ))}
            </div>
            <div className="platforms">
              {gameData.platforms.map((platform, index) => (
                <span key={index} className="platform-tag">{platform}</span>
              ))}
            </div>
            <div className="action-buttons">
              <button className="primary-button">Buy Game</button>
              <button className="secondary-button">Add to Wishlist</button>
            </div>
          </div>
        </section>

        {/* 게임 설명 섹션 */}
        <section className="game-description">
          <h2>About The Game</h2>
          <p>{gameData.description}</p>
        </section>

        {/* 스크린샷 섹션 */}
        <section className="game-media">
          <h2>Screenshots & Videos</h2>
          <div className="screenshots-container">
            {gameData.screenshots.map((screenshot, index) => (
              <div key={index} className="screenshot">
                <div className="screenshot-placeholder">Screenshot {index + 1}</div>
              </div>
            ))}
          </div>
          
          {/* 영상 섹션 */}
          <div className="videos-container">
            {gameData.videos.map((video, index) => (
              <div key={index} className="video-embed">
                <div className="video-placeholder">Video {index + 1}</div>
              </div>
            ))}
          </div>
        </section>

        {/* 시스템 요구사항 섹션 */}
        <section className="system-requirements">
          <h2>System Requirements</h2>
          <div className="requirements-grid">
            <div className="minimum-requirements">
              <h3>Minimum</h3>
              <ul>
                <li><strong>OS:</strong> {gameData.systemRequirements.minimum.os}</li>
                <li><strong>Processor:</strong> {gameData.systemRequirements.minimum.processor}</li>
                <li><strong>Memory:</strong> {gameData.systemRequirements.minimum.memory}</li>
                <li><strong>Graphics:</strong> {gameData.systemRequirements.minimum.graphics}</li>
                <li><strong>Storage:</strong> {gameData.systemRequirements.minimum.storage}</li>
              </ul>
            </div>
            <div className="recommended-requirements">
              <h3>Recommended</h3>
              <ul>
                <li><strong>OS:</strong> {gameData.systemRequirements.recommended.os}</li>
                <li><strong>Processor:</strong> {gameData.systemRequirements.recommended.processor}</li>
                <li><strong>Memory:</strong> {gameData.systemRequirements.recommended.memory}</li>
                <li><strong>Graphics:</strong> {gameData.systemRequirements.recommended.graphics}</li>
                <li><strong>Storage:</strong> {gameData.systemRequirements.recommended.storage}</li>
              </ul>
            </div>
          </div>
        </section>

        {/* 리뷰 섹션 */}
        <section className="game-reviews">
          <h2>Player Reviews</h2>
          <div className="review-summary">
            <div className="review-score">4.7</div>
            <div className="review-text">
              <strong>Very Positive</strong>
              <p>Based on 1,200+ reviews</p>
            </div>
          </div>
          <div className="reviews-list">
            <div className="review-card">
              <div className="reviewer">
                <div className="reviewer-avatar">👤</div>
                <div className="reviewer-name">Player123</div>
              </div>
              <div className="review-content">
                <div className="review-rating">⭐⭐⭐⭐⭐</div>
                <p>This game is amazing! The graphics are stunning, and the gameplay is smooth and engaging. I've spent over 100 hours playing and still discovering new things.</p>
              </div>
            </div>
            <div className="review-card">
              <div className="reviewer">
                <div className="reviewer-avatar">👤</div>
                <div className="reviewer-name">Gamer456</div>
              </div>
              <div className="review-content">
                <div className="review-rating">⭐⭐⭐⭐</div>
                <p>Great game with an immersive story. The only downside is that some levels can be a bit repetitive. Still worth playing though!</p>
              </div>
            </div>
          </div>
          <button className="load-more-button">Load More Reviews</button>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default GameDetailPage; 