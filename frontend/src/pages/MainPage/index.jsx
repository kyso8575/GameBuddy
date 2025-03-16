import React from 'react';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import GameCard from '../../components/GameCard';
import '../../styles/MainPage.css';

function MainPage() {
  // 게임 데이터 배열
  const games = [
    { id: 1, title: 'Game Title 1', rating: '4.5', tags: 'Action • PC' },
    { id: 2, title: 'Game Title 2', rating: '4.8', tags: 'RPG • PS5' },
    { id: 3, title: 'Game Title 3', rating: '4.2', tags: 'Strategy • PC' },
    { id: 4, title: 'Game Title 4', rating: '4.7', tags: 'Adventure • Switch' },
    { id: 5, title: 'Game Title 5', rating: '4.4', tags: 'FPS • PC' },
    { id: 6, title: 'Game Title 6', rating: '4.6', tags: 'Racing • PS5' },
    { id: 7, title: 'Game Title 7', rating: '4.3', tags: 'Simulation • PC' },
    { id: 8, title: 'Game Title 8', rating: '4.9', tags: 'MMORPG • PC' },
    { id: 9, title: 'Game Title 9', rating: '4.7', tags: 'Puzzle • Mobile' },
    { id: 10, title: 'Game Title 10', rating: '4.5', tags: 'Sports • PS5' },
  ];

  return (
    <div className="app">
      {/* NavBar 컴포넌트 사용 */}
      <NavBar />

      {/* 검색 및 필터 영역 */}
      <section className="search-filter-section">
        <div className="search-box white-bg">
          <input
            type="text"
            className="search-input white-bg"
            placeholder="Search games..."
          />
          <button className="search-button white-bg">🔍</button>
        </div>
        <div className="dropdowns">
          <select className="dropdown white-bg">
            <option>Genre</option>
            <option>Action</option>
            <option>RPG</option>
            <option>Strategy</option>
          </select>
          <select className="dropdown white-bg">
            <option>Platform</option>
            <option>PC</option>
            <option>PS5</option>
            <option>Switch</option>
          </select>
          <button className="filter-button">Filter</button>
        </div>
      </section>

      {/* 게임 카드 영역 */}
      <main className="main-content">
        {games.map((game) => (
          <GameCard
            key={game.id}
            id={game.id}
            title={game.title}
            rating={game.rating}
            tags={game.tags}
          />
        ))}
      </main>

      {/* Footer 컴포넌트 사용 */}
      <Footer />
    </div>
  );
}

export default MainPage;