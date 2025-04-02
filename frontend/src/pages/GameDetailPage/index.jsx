import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import '../../styles/GameDetailPage.css';

function GameDetailPage() {
  // Get game ID parameter from URL
  const { id } = useParams();
  const { isAuthenticated, user, token } = useAuth();
  const [gameData, setGameData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeScreenshot, setActiveScreenshot] = useState(0);
  
  // 위시리스트 관련 상태
  const [isInWishlist, setIsInWishlist] = useState(false);
  const [wishlistLoading, setWishlistLoading] = useState(false);
  const [wishlistError, setWishlistError] = useState(null);
  
  // Review related states
  const [averageRating, setAverageRating] = useState(0);
  const [reviewCount, setReviewCount] = useState(0);
  const [reviews, setReviews] = useState([]);
  const [reviewLoading, setReviewLoading] = useState(false);
  const [reviewError, setReviewError] = useState(null);
  // Pagination related states
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [pageSize, setPageSize] = useState(5); // Number of reviews to display per page
  
  // Review submission related states
  const [userRating, setUserRating] = useState(0);
  const [userReview, setUserReview] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  // State to check if user has already reviewed this game
  const [userHasReview, setUserHasReview] = useState(false);
  const [userReviewId, setUserReviewId] = useState(null);

  useEffect(() => {
    // Fetch game data from API
    const fetchGameDetails = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://127.0.0.1:8000/games/${id}/`);
        
        if (!response.ok) {
          throw new Error(`Game not found (${response.status})`);
        }
        
        const data = await response.json();
        setGameData(data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load game details');
      } finally {
        setLoading(false);
      }
    };
    
    fetchGameDetails();
  }, [id]);

  // 위시리스트 상태 확인
  useEffect(() => {
    const checkWishlistStatus = async () => {
      if (!id || !isAuthenticated() || !token) {
        setIsInWishlist(false);
        return;
      }
      
      try {
        setWishlistLoading(true);
        const response = await fetch(`http://127.0.0.1:8000/wishlist/game/${id}/`, {
          headers: {
            'Authorization': `Token ${token}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to check wishlist status (${response.status})`);
        }
        
        const data = await response.json();
        setIsInWishlist(data.is_in_wishlist);
        setWishlistError(null);
      } catch (err) {
        console.error("Error checking wishlist status:", err.message);
        setWishlistError(err.message);
        setIsInWishlist(false);
      } finally {
        setWishlistLoading(false);
      }
    };
    
    checkWishlistStatus();
  }, [id, token, isAuthenticated]);

  // 위시리스트에 추가/삭제
  const toggleWishlist = async () => {
    if (!isAuthenticated() || !token) {
      // 로그인이 필요한 경우 처리
      alert("Please login to add games to your wishlist.");
      return;
    }
    
    setWishlistLoading(true);
    
    try {
      if (isInWishlist) {
        // 위시리스트에서 삭제
        const response = await fetch(`http://127.0.0.1:8000/wishlist/game/${id}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Token ${token}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to remove from wishlist (${response.status})`);
        }
        
        setIsInWishlist(false);
      } else {
        // 위시리스트에 추가
        const response = await fetch(`http://127.0.0.1:8000/wishlist/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
          },
          body: JSON.stringify({ game_id: id })
        });
        
        if (!response.ok) {
          throw new Error(`Failed to add to wishlist (${response.status})`);
        }
        
        setIsInWishlist(true);
      }
      
      setWishlistError(null);
    } catch (err) {
      console.error("Error updating wishlist:", err.message);
      setWishlistError(err.message);
    } finally {
      setWishlistLoading(false);
    }
  };

  // Function to fetch review data
  const fetchReviews = async () => {
    if (!id) return;
    
    try {
      setReviewLoading(true);
      // Include pagination parameters in request (change sorting to updated_at)
      const response = await fetch(`http://127.0.0.1:8000/reviews/game/${id}/?page=${currentPage}&page_size=${pageSize}&ordering=-updated_at`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch reviews (${response.status})`);
      }
      
      const data = await response.json();
      
      // Process data according to backend response structure
      if (data && typeof data === 'object') {
        // Set reviews array (located in reviews property)
        if (Array.isArray(data.reviews)) {
          setReviews(data.reviews);
        } else {
          // Backup logic - if structure is different or array is returned directly
          setReviews(Array.isArray(data) ? data : []);
        }
        
        // Set average rating and review count - use values provided by backend
        if ('average_rating' in data) {
          setAverageRating(parseFloat(data.average_rating) || 0);
        }
        
        // Set pagination information
        if (data.pagination) {
          if ('total_reviews' in data.pagination) {
            setReviewCount(data.pagination.total_reviews);
          }
          if ('total_pages' in data.pagination) {
            setTotalPages(data.pagination.total_pages);
          }
          if ('current_page' in data.pagination) {
            setCurrentPage(data.pagination.current_page);
          }
          if ('page_size' in data.pagination) {
            setPageSize(data.pagination.page_size);
          }
        } else if (Array.isArray(data.reviews)) {
          // Backup logic - use reviews array length if pagination info is missing
          setReviewCount(data.reviews.length);
        }
      } else {
        // Response is not in expected format
        setReviews([]);
        setAverageRating(0);
        setReviewCount(0);
        setTotalPages(1);
      }
      
      setReviewError(null);
    } catch (err) {
      setReviewError(err.message || 'Failed to load reviews');
      setReviews([]);
      setAverageRating(0);
      setReviewCount(0);
      setTotalPages(1);
    } finally {
      setReviewLoading(false);
    }
  };

  // Review data fetching useEffect
  useEffect(() => {
    fetchReviews();
  }, [id, currentPage, pageSize]);

  // Function to fetch user's existing review
  const fetchUserReview = async () => {
    if (!id || !isAuthenticated() || !token) return;

    try {
      // API endpoint modification - adjusted to match backend API structure
      const response = await fetch(`http://127.0.0.1:8000/reviews/game/${id}/user/`, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });

      if (!response.ok) {
        // Request failed (401, 500, etc.)
        throw new Error(`Failed to fetch user review (${response.status})`);
      }

      const data = await response.json();
      
      // Response successful but no review exists
      if (data.has_review === false) {
        setUserHasReview(false);
        setUserReviewId(null);
        setUserRating(0);
        setUserReview('');
        return;
      }
      
      // User already has a review
      setUserHasReview(true);
      setUserReviewId(data.id);
      setUserRating(parseFloat(data.rating) || 0);
      setUserReview(data.review || '');
    } catch (err) {
      console.error("Error fetching user review:", err.message);
      // Set default values even if an error occurs
      setUserHasReview(false);
      setUserReviewId(null);
    }
  };

  // Check user's review when login status or game ID changes
  useEffect(() => {
    fetchUserReview();
  }, [id, token, isAuthenticated]);

  // Review submission handler
  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    
    // Re-verify authentication status
    if (!isAuthenticated() || !token) {
      setSubmitError('Login required. Please log in again.');
      return;
    }
    
    // Validation
    if (userRating === 0) {
      setSubmitError('Please select a rating.');
      return;
    }
    
    if (!userReview.trim()) {
      setSubmitError('Please enter review content.');
      return;
    }
    
    try {
      setSubmitting(true);
      setSubmitError(null);
      
      // Backend validation logic checks two different fields
      // game: required by serializer
      // game_id: required by backend view logic
      // Send both fields to resolve the issue
      const gameIdInt = parseInt(id, 10);
      const reviewData = {
        game: gameIdInt,      // Field for serializer
        game_id: gameIdInt,   // Field for backend view logic
        rating: parseFloat(userRating),
        review: userReview.trim()
      };
      
      // Set URL and method for review creation or update
      const url = userHasReview 
        ? `http://127.0.0.1:8000/reviews/${userReviewId}/` 
        : 'http://127.0.0.1:8000/reviews/';
      
      const method = userHasReview ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify(reviewData)
      });
      
      // Parse response text, needed for error handling
      const responseText = await response.text();
      
      // Try to parse as JSON only if response contains content
      let errorData;
      if (responseText) {
        try {
          errorData = JSON.parse(responseText);
        } catch (e) {
          errorData = { error: responseText };
        }
      }
      
      if (!response.ok) {
        throw new Error(errorData?.error || `Failed to ${userHasReview ? 'update' : 'submit'} review. (${response.status})`);
      }
      
      // Submission successful
      setSubmitSuccess(true);
      setUserHasReview(true); // Now has a review
      
      if (!userHasReview && errorData && errorData.id) {
        setUserReviewId(errorData.id); // Save newly created review ID
      }
      
      // Refresh review list (move to first page)
      setCurrentPage(1);
      fetchReviews();
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setSubmitSuccess(false);
      }, 3000);
      
    } catch (err) {
      setSubmitError(err.message || 'An error occurred while submitting the review.');
    } finally {
      setSubmitting(false);
    }
  };

  // 페이지 변경 핸들러
  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  // 별점 계산을 위한 함수 (UI용) - 단순화된 버전
  const renderStarsFromScore = (score, maxStars = 5) => {
    // 점수가 없거나 0이면 빈 별 5개 반환
    if (!score || score === 0 || isNaN(score)) {
      return (
        <div className="stars-container">
          {[...Array(maxStars)].map((_, i) => (
            <span key={`empty-${i}`} className="empty-star">☆</span>
          ))}
        </div>
      );
    }
    
    // 숫자로 변환하고 1-5 범위로 제한
    let numericScore = parseFloat(score);
    if (isNaN(numericScore)) numericScore = 0;
    numericScore = Math.max(0, Math.min(5, numericScore));
    
    return (
      <div className="stars-container">
        {[...Array(maxStars)].map((_, i) => (
          <span
            key={i}
            className={i < Math.floor(numericScore) ? "full-star" : 
                      (i === Math.floor(numericScore) && numericScore % 1 >= 0.5) ? "half-star" : "empty-star"}
          >
            {i < Math.floor(numericScore) || 
             (i === Math.floor(numericScore) && numericScore % 1 >= 0.5) 
              ? "★" : "☆"}
          </span>
        ))}
      </div>
    );
  };

  // 로딩 중 상태 표시
  if (loading) {
    return (
      <div className="app">
        <NavBar />
        <main className="game-detail-container">
          <div className="loading-spinner">Loading game details...</div>
        </main>
        <Footer />
      </div>
    );
  }
  
  // 에러 상태 표시
  if (error) {
    return (
      <div className="app">
        <NavBar />
        <main className="game-detail-container">
          <div className="error-message">
            <h2>Error</h2>
            <p>{error}</p>
            <button onClick={() => window.location.reload()}>Try Again</button>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  // 데이터가 없는 경우
  if (!gameData) {
    return (
      <div className="app">
        <NavBar />
        <main className="game-detail-container">
          <div className="no-data">No game data available</div>
        </main>
        <Footer />
      </div>
    );
  }

  // 문자열을 배열로 안전하게 변환하는 함수
  const safeParseArray = (str) => {
    if (!str) return [];
    
    if (typeof str === 'string') {
      try {
        // 정상적인 JSON 형식이면 파싱 시도
        return JSON.parse(str.replace(/'/g, '"'));
      } catch (e) {
        // JSON 파싱 실패시 문자열을 직접 처리
        // 대괄호 제거하고 쉼표로 분리
        const cleanStr = str.replace(/^\[|\]$/g, '').trim();
        if (!cleanStr) return [];
        return cleanStr.split(',').map(item => item.trim());
      }
    }
    
    // 이미 배열이면 그대로 반환
    return Array.isArray(str) ? str : [];
  };

  // 문자열에서 배열로 안전하게 변환
  const platforms = safeParseArray(gameData.platforms);
  const genres = safeParseArray(gameData.genres);
  const screenshots = safeParseArray(gameData.screenshots);
  const stores = safeParseArray(gameData.stores);

  const nextScreenshot = () => {
    setActiveScreenshot((prev) => (prev + 1) % screenshots.length);
  };

  const prevScreenshot = () => {
    setActiveScreenshot((prev) => (prev - 1 + screenshots.length) % screenshots.length);
  };

  // 별점 계산
  const gameRating = parseFloat(gameData.rating) || 0;
  const rawgStars = renderStarsFromScore(gameRating);

  return (
    <div className="app">
      <NavBar />
      
      <main className="game-detail-container">
        {/* Hero Banner */}
        <div className="game-hero-banner" style={{backgroundImage: screenshots.length > 0 ? `url(${screenshots[0]})` : 'none'}}>
          <div className="hero-overlay">
            <h1>{gameData.name}</h1>
          </div>
        </div>
        
        {/* 게임 정보 섹션 - 새로운 디자인 */}
        <section className="game-info-section no-image">

          <div className="game-rating-row">
            {gameData.rating && (
              <div className="rating-box">
                <div className="rating-value">{parseFloat(gameData.rating).toFixed(1) || 0}</div>
                <div className="rating-stars">
                  {rawgStars}
                </div>
                <div className="rating-label">RAWG Rating</div>
              </div>
            )}
            
            {gameData.metacritic_score && (
              <div className="metacritic-box">
                <div className="metacritic-score">{gameData.metacritic_score}</div>
                <div className="metacritic-label">Metacritic</div>
              </div>
            )}
          </div>
          
          <div className="game-details-grid">
            {/* Row 1: Genres and Playtime */}
            <div className="detail-row">
              <div className="detail-section">
                <h3 className="detail-title">Genres</h3>
                <div className="game-genres">
                  {genres.length > 0 ? genres.map((genre, index) => (
                    <span key={index} className="genre-pill">{genre}</span>
                  )) : <span className="empty-data">No genres available</span>}
                </div>
              </div>
              
              <div className="detail-section">
                <h3 className="detail-title">Playtime</h3>
                <div className="detail-value">{gameData.playtime || 0} Hours</div>
              </div>
            </div>
            
            {/* Row 2: Platforms and Released */}
            <div className="detail-row">
              <div className="detail-section">
                <h3 className="detail-title">Platforms</h3>
                <div className="game-platforms">
                  {platforms.length > 0 ? platforms.map((platform, index) => (
                    <span key={index} className="platform-pill">{platform}</span>
                  )) : <span className="empty-data">No platforms available</span>}
                </div>
              </div>
              
              <div className="detail-section">
                <h3 className="detail-title">Released</h3>
                <div className="detail-value">{gameData.released || 'N/A'}</div>
              </div>
            </div>
            
            {/* Row 3: Stores and Actions */}
            <div className="detail-row">
              <div className="detail-section">
                <h3 className="detail-title">Available on</h3>
                <div className="store-tags">
                  {stores && stores.length > 0 ? stores.map((store, index) => (
                    <span key={index} className="store-pill">{store}</span>
                  )) : <span className="empty-data">No store information</span>}
                </div>
              </div>
              
              <div className="detail-section">
                <div className="game-actions">
                  <button className="buy-button">Buy Game</button>
                  <button 
                    className={`wishlist-button ${isInWishlist ? 'in-wishlist' : ''}`} 
                    onClick={toggleWishlist}
                    disabled={wishlistLoading}
                  >
                    {wishlistLoading ? 'Loading...' : isInWishlist ? 'Remove from Wishlist' : 'Add to Wishlist'}
                  </button>
                  {wishlistError && <div className="wishlist-error">{wishlistError}</div>}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 게임 설명 섹션 */}
        <section className="game-description">
          <h2>About The Game</h2>
          {gameData.description && gameData.description.length > 10 ? (
            <div dangerouslySetInnerHTML={{ __html: gameData.description }} />
          ) : (
            <div className="expanded-description">
              <p>No description available.</p>
            </div>
          )}
        </section>

        {/* 스크린샷 섹션 - 개선된 갤러리 */}
        {screenshots.length > 0 && (
          <section className="game-media">
            <h2>Photos</h2>
            <div className="screenshot-gallery">
              <button className="gallery-nav prev" onClick={prevScreenshot}>❮</button>
              <div className="featured-screenshot">
                <img src={screenshots[activeScreenshot]} alt={`Screenshot ${activeScreenshot + 1}`} />
              </div>
              <button className="gallery-nav next" onClick={nextScreenshot}>❯</button>
            </div>
            <div className="screenshot-thumbnails">
              {screenshots.map((screenshot, index) => (
                <div 
                  key={index} 
                  className={`thumbnail ${index === activeScreenshot ? 'active' : ''}`}
                  onClick={() => setActiveScreenshot(index)}
                >
                  <img src={screenshot} alt={`Thumbnail ${index + 1}`} />
                </div>
              ))}
            </div>
          </section>
        )}

        {/* 리뷰 섹션 - 정적 UI만 표시 */}
        <section className="reviews-section">
          <div className="reviews-header">
            <h2>User Reviews</h2>
            <div className="reviews-summary">
              <div className="average-rating">
                <div className="rating-number">
                  {isNaN(averageRating) ? '0.0' : averageRating.toFixed(1)}
                </div>
                <div className="rating-stars">
                  {renderStarsFromScore(averageRating)}
                </div>
                <div className="rating-count">
                  based on {reviewCount} reviews
                </div>
              </div>
            </div>
          </div>

          {/* 새 리뷰 작성 UI */}
          {isAuthenticated() && token ? (
            <div className="write-review-container">
              <h3>Write a Review</h3>
              
              {submitSuccess && (
                <div className="submit-success">
                  Review successfully {userHasReview ? 'updated' : 'submitted'}!
                </div>
              )}
              
              {submitError && (
                <div className="submit-error">
                  {submitError}
                </div>
              )}
              
              <form className="review-form" onSubmit={handleReviewSubmit}>
                <div className="form-row">
                  <label htmlFor="review-rating">Your Rating</label>
                  <div className="rating-input">
                    <div className="star-rating">
                      {[...Array(5)].map((_, index) => {
                        const ratingValue = index + 1;
                        return (
                          <span 
                            key={index} 
                            className={`star ${ratingValue <= userRating ? 'filled' : ''}`}
                            onClick={() => setUserRating(ratingValue)}
                            onMouseEnter={() => setUserRating(ratingValue)}
                            onMouseLeave={() => setUserRating(userRating)}
                          >
                            ★
                          </span>
                        );
                      })}
                    </div>
                    <span className="rating-text">
                      {userRating ? `${userRating}/5` : 'Click to rate'}
                    </span>
                  </div>
                </div>

                <div className="form-row">
                  <label htmlFor="review-text">Review</label>
                  <textarea 
                    id="review-text" 
                    placeholder="What did you like or dislike about this game?" 
                    rows="5"
                    value={userReview}
                    onChange={(e) => setUserReview(e.target.value)}
                  ></textarea>
                </div>
                <div className="review-actions">
                  <button 
                    type="submit" 
                    className="submit-review-btn"
                    disabled={submitting}
                  >
                    {submitting ? 'Submitting...' : userHasReview ? 'Update Review' : 'Submit Review'}
                  </button>
                </div>
              </form>
            </div>
          ) : (
            <div className="login-to-review">
              <p>To write a review, please <Link to="/login" className="login-link">log in</Link>. After logging in, you can leave a review!</p>
            </div>
          )}

          {/* 리뷰 목록 */}
          <div className="reviews-list">
            <h3>Reviews</h3>
            
            {/* 페이지 크기 선택 드롭다운 추가 */}
            <div className="reviews-settings">
              <div className="page-size-selector">
                <label htmlFor="page-size">Reviews per page:</label>
                <select 
                  id="page-size" 
                  value={pageSize} 
                  onChange={(e) => {
                    const newSize = parseInt(e.target.value);
                    setPageSize(newSize);
                    setCurrentPage(1); // 페이지 크기 변경 시 첫 페이지로 이동
                  }}
                >
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                </select>
              </div>
            </div>
            
            {reviewLoading ? (
              <div className="loading-reviews">Loading reviews...</div>
            ) : reviewError ? (
              <div className="review-error">
                <p>Error loading reviews: {reviewError}</p>
                <button onClick={() => window.location.reload()}>Try Again</button>
              </div>
            ) : !Array.isArray(reviews) ? (
              <div className="review-error">
                <p>Invalid review data format. Please try again.</p>
                <button onClick={() => window.location.reload()}>Reload</button>
              </div>
            ) : reviews.length === 0 ? (
              <div className="no-reviews">No reviews yet. Be the first to review!</div>
            ) : (
              // 리뷰 목록 UI (실제 데이터)
              <div className="reviews-container">
                {reviews.map(review => (
                  <div className="review-item" key={review.id || `review-${Math.random()}`}>
                    <div className="review-header">
                      <div className="reviewer-info">
                        <div className="reviewer-name">
                          {review.user ? 
                            (review.user.first_name ? review.user.first_name : 
                             review.user.name ? review.user.name : review.user.username) 
                            : review.username || 'Anonymous'}
                        </div>
                        <div className="review-date">
                          {review.updated_at ? `${new Date(review.updated_at).toLocaleDateString()}` : 'Unknown date'}
                        </div>
                      </div>
                      <div className="review-rating">
                        {renderStarsFromScore(review.rating || 0)}
                      </div>
                    </div>
                    <div className="review-content">
                      <p>{review.review || review.content || 'No content'}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {/* 페이지네이션 UI */}
            <div className="reviews-pagination">
              <div className="pagination-controls">
                <button 
                  className="page-btn" 
                  disabled={currentPage === 1} 
                  onClick={() => handlePageChange(currentPage - 1)}
                >
                  &lt; Prev
                </button>
                
                {/* 페이지 번호 버튼들 */}
                {[...Array(Math.min(5, totalPages))].map((_, index) => {
                  // 표시할 페이지 번호 계산
                  let pageNum;
                  if (totalPages <= 5) {
                    // 전체 페이지가 5개 이하면 1부터 순서대로 표시
                    pageNum = index + 1;
                  } else {
                    // 현재 페이지 주변의 페이지 번호 표시
                    if (currentPage <= 3) {
                      // 현재 페이지가 앞쪽인 경우 1~5 표시
                      pageNum = index + 1;
                    } else if (currentPage >= totalPages - 2) {
                      // 현재 페이지가 뒤쪽인 경우 마지막 5개 표시
                      pageNum = totalPages - 4 + index;
                    } else {
                      // 그 외의 경우 현재 페이지를 중심으로 앞뒤로 2개씩 표시
                      pageNum = currentPage - 2 + index;
                    }
                  }
                  
                  return (
                    <button 
                      key={pageNum} 
                      className={`page-num ${currentPage === pageNum ? 'active' : ''}`}
                      onClick={() => handlePageChange(pageNum)}
                    >
                      {pageNum}
                    </button>
                  );
                })}
                
                <button 
                  className="page-btn" 
                  disabled={currentPage === totalPages || totalPages === 0} 
                  onClick={() => handlePageChange(currentPage + 1)}
                >
                  Next &gt;
                </button>
              </div>
              <div className="pagination-info">
                Page {currentPage} of {totalPages} ({reviewCount} reviews)
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default GameDetailPage;