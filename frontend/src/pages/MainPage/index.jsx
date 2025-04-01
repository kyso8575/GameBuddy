import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import GameCard from '../../components/GameCard';
import '../../styles/MainPage.css';

function MainPage() {
  // 상태 관리
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // 페이지네이션 상태
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 28; // 페이지당 50개 게임
  
  // 입력 필드 상태 (UI에 표시되는 값)
  const [searchInput, setSearchInput] = useState('');
  const [genreInput, setGenreInput] = useState('All Genres');
  const [platformInput, setPlatformInput] = useState('All Platforms');
  
  // 활성화된 필터 상태 (실제 API 요청에 사용)
  const [activeFilters, setActiveFilters] = useState({
    search: '',
    genres: 'All Genres',
    platforms: 'All Platforms',
    page: 1,
    items_per_page: itemsPerPage
  });
  
  // 장르와 플랫폼 목록 (API에서 받아올 수도 있음)
  const genres = ['Action', 'Adventure', 'RPG', 'Strategy', 'FPS', 'Simulation', 'Sports', 'Puzzle'];
  const platforms = ['PC', 'PS5', 'Xbox Series X', 'Switch', 'Mobile'];

  // 필터링된 게임 데이터 가져오기
  const fetchGames = async () => {
    setLoading(true);
    setError(null);
    

    
    try {
      // 필터 옵션을 POST 요청의 body에 포함
      const response = await axios.post('http://127.0.0.1:8000/games/', {
        search: activeFilters.search,
        genres: activeFilters.genres,
        platforms: activeFilters.platforms,
        page: activeFilters.page,
        items_per_page: activeFilters.items_per_page
      });
      
  
      
      // Adjust based on API response format
      if (response.data.games) {
        setGames(response.data.games);
        setTotalPages(response.data.total_pages || 1);
      } else {
        setGames(response.data);
        // Calculate total pages (ideally this would come from the server)
        setTotalPages(Math.ceil(response.data.length / itemsPerPage));
      }
      
      
      
    } catch (err) {
      console.error('Error occurred while fetching game data:', err);
      setError('Unable to load game data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Only make API request when activeFilters changes
  useEffect(() => {
    fetchGames();
  }, [activeFilters]); // Only run when activeFilters changes
  
  // Filter application handler (button click)
  const applyFilters = (e) => {
    e.preventDefault();
    
    // Return to first page when filters change
    setCurrentPage(1);
    setActiveFilters({
      search: searchInput,
      genres: genreInput,
      platforms: platformInput,
      page: 1,
      items_per_page: itemsPerPage
    });
  };
  
  // Page change handler
  const handlePageChange = (newPage) => {
    if (newPage < 1 || newPage > totalPages) return;
    
    setCurrentPage(newPage);
    setActiveFilters({
      ...activeFilters,
      page: newPage
    });
  };
  
  // Search input handler
  const handleSearchInput = (e) => {
    setSearchInput(e.target.value);
  };
  
  // Execute search on Enter key
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      applyFilters(e);
    }
  };
  
  // Genre selection handler
  const handleGenreChange = (e) => {
    setGenreInput(e.target.value);
  };
  
  // Platform selection handler
  const handlePlatformChange = (e) => {
    setPlatformInput(e.target.value);
  };

  // Pagination component
  const Pagination = () => {
    // Calculate page number range to display
    const pageRange = 5;
    let startPage = Math.max(1, currentPage - Math.floor(pageRange / 2));
    const endPage = Math.min(totalPages, startPage + pageRange - 1);
    
    // Adjust startPage (if end page is less than totalPages)
    if (endPage - startPage + 1 < pageRange) {
      startPage = Math.max(1, endPage - pageRange + 1);
    }
    
    const pageNumbers = [];
    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push(i);
    }
    
    return (
      <div className="pagination">
        <button 
          className="pagination-btn" 
          onClick={() => handlePageChange(1)}
          disabled={currentPage === 1}
        >
          &laquo;
        </button>
        <button 
          className="pagination-btn" 
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          &lt;
        </button>
        
        {pageNumbers.map(number => (
          <button
            key={number}
            className={`pagination-btn ${number === currentPage ? 'active' : ''}`}
            onClick={() => handlePageChange(number)}
          >
            {number}
          </button>
        ))}
        
        <button 
          className="pagination-btn"
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          &gt;
        </button>
        <button 
          className="pagination-btn"
          onClick={() => handlePageChange(totalPages)}
          disabled={currentPage === totalPages}
        >
          &raquo;
        </button>
      </div>
    );
  };

  return (
    <div className="app">
      {/* Using NavBar component */}
      <NavBar />

      {/* Search and filter section */}
      <section className="search-filter-section">
        <div className="search-box white-bg">
          <input
            type="text"
            className="search-input white-bg"
            placeholder="Search games..."
            value={searchInput}
            onChange={handleSearchInput}
            onKeyPress={handleKeyPress}
          />
          <button 
            className="search-button white-bg"
            onClick={applyFilters}
          >
            🔍
          </button>
        </div>
        <div className="dropdowns">
          <select 
            className="dropdown white-bg"
            value={genreInput} 
            onChange={handleGenreChange}
          >
            <option value="All Genres">All Genres</option>
            {genres.map(genre => (
              <option key={genre} value={genre}>{genre}</option>
            ))}
          </select>
          <select 
            className="dropdown white-bg"
            value={platformInput}
            onChange={handlePlatformChange}
          >
            <option value="All Platforms">All Platforms</option>
            {platforms.map(platform => (
              <option key={platform} value={platform}>{platform}</option>
            ))}
          </select>
          <button 
            className="filter-button"
            onClick={applyFilters}
          >
            Filter
          </button>
        </div>
      </section>

      {/* Game card section */}
      <main className="main-content">
        {loading ? (
          <div className="loading-message">Loading games...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : games.length === 0 ? (
          <div className="no-results-message">No games found matching your criteria.</div>
        ) : (
          games.map((game) => (
            <div key={game.id} className="game-card-wrapper">
              <GameCard
                id={game.id}
                name={game.name}
                rating={game.metacritic_score || "N/A"}
                tags={`${game.genres || ""} • ${game.platforms || ""}`}
                imageUrl={game.background_image}
              />
            </div>
          ))
        )}
      </main>
      
      {/* Pagination section - Display only when there are games and not loading */}
      {!loading && games.length > 0 && totalPages > 1 && (
        <div className="pagination-container">
          <Pagination />
        </div>
      )}

      {/* Footer component usage */}
      <Footer />
    </div>
  );
}

export default MainPage;