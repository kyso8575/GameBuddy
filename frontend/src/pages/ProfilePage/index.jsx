import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import '../../styles/ProfilePage.css';

// 이미지 경로를 상수로 정의
const DEFAULT_PROFILE_IMAGE = '/images/default_profile.png';
const DEFAULT_GAME_IMAGE = '/images/default_game.png';
const FALLBACK_IMAGE = 'https://via.placeholder.com/150?text=Image';

const ProfilePage = () => {
  const { user, token, isAuthenticated } = useAuth();
  
  // 상태 정의
  const [profile, setProfile] = useState(null);
  const [wishlist, setWishlist] = useState([]);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState({
    profile: true,
    wishlist: true,
    comments: true
  });
  const [error, setError] = useState({
    profile: null,
    wishlist: null,
    comments: null
  });

  // 프로필 정보 가져오기
  useEffect(() => {
    const fetchProfileData = async () => {
      if (!isAuthenticated() || !token) {
        return;
      }

      try {
        setLoading(prev => ({ ...prev, profile: true }));
        const response = await fetch('http://127.0.0.1:8000/accounts/current-user/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        });

        if (!response.ok) {
          throw new Error(`프로필 정보를 가져오는데 실패했습니다 (${response.status})`);
        }

        const data = await response.json();
        setProfile(data);
        setError(prev => ({ ...prev, profile: null }));
      } catch (err) {
        console.error('프로필 정보 가져오기 오류:', err.message);
        setError(prev => ({ ...prev, profile: err.message }));
      } finally {
        setLoading(prev => ({ ...prev, profile: false }));
      }
    };

    fetchProfileData();
  }, [token, isAuthenticated]);

  // 위시리스트 가져오기
  useEffect(() => {
    const fetchWishlist = async () => {
      if (!isAuthenticated() || !token) {
        return;
      }

      try {
        setLoading(prev => ({ ...prev, wishlist: true }));
        const response = await fetch('http://127.0.0.1:8000/wishlist/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        });

        if (!response.ok) {
          throw new Error(`위시리스트를 가져오는데 실패했습니다 (${response.status})`);
        }

        const data = await response.json();
        // wishlist API는 배열을 반환하고, 각 항목에는 game_details가 포함되어 있음
        const formattedWishlist = data.map(item => ({
          id: item.id,
          title: item.game_details.name,
          genre: item.game_details.genres ? JSON.parse(item.game_details.genres)[0] : '미분류',
          image: item.game_details.background_image || DEFAULT_GAME_IMAGE,
          gameId: item.game_details.id
        }));
        
        setWishlist(formattedWishlist);
        setError(prev => ({ ...prev, wishlist: null }));
      } catch (err) {
        console.error('위시리스트 가져오기 오류:', err.message);
        setError(prev => ({ ...prev, wishlist: err.message }));
      } finally {
        setLoading(prev => ({ ...prev, wishlist: false }));
      }
    };

    fetchWishlist();
  }, [token, isAuthenticated]);

  // 댓글 목록 가져오기
  useEffect(() => {
    const fetchComments = async () => {
      if (!isAuthenticated() || !token || !user) {
        return;
      }

      try {
        setLoading(prev => ({ ...prev, comments: true }));
        const response = await fetch(`http://127.0.0.1:8000/reviews/?user_id=${user.id}`, {
          headers: {
            'Authorization': `Token ${token}`
          }
        });

        if (!response.ok) {
          throw new Error(`댓글 목록을 가져오는데 실패했습니다 (${response.status})`);
        }

        const data = await response.json();
        console.log('댓글 API 응답 데이터:', data);
        
        // API 응답 구조에 따라 조정
        let userComments = [];
        if (data.reviews) {
          userComments = data.reviews;
        } else if (Array.isArray(data)) {
          userComments = data;
        }
        
        // 각 댓글에 대해 게임 정보 가져오기
        const enrichedComments = await Promise.all(userComments.map(async (comment) => {
          // 이미 game_details가 있다면 그것을 사용
          if (comment.game_details && comment.game_details.name) {
            return {
              ...comment,
              gameTitle: comment.game_details.name,
              gameImage: comment.game_details.background_image || DEFAULT_GAME_IMAGE
            };
          }
          
          // game_details가 없다면 game_id를 사용해 게임 정보 가져오기
          const gameId = typeof comment.game === 'number' ? comment.game : null;
          if (!gameId) {
            return {
              ...comment,
              gameTitle: '게임 정보 없음',
              gameImage: DEFAULT_GAME_IMAGE
            };
          }
          
          try {
            const gameResponse = await fetch(`http://127.0.0.1:8000/games/${gameId}/`, {
              headers: {
                'Authorization': token ? `Token ${token}` : ''
              }
            });
            
            if (!gameResponse.ok) {
              return {
                ...comment,
                gameTitle: `게임 #${gameId}`,
                gameImage: DEFAULT_GAME_IMAGE
              };
            }
            
            const gameData = await gameResponse.json();
            return {
              ...comment,
              gameTitle: gameData.name || `게임 #${gameId}`,
              gameImage: gameData.background_image || DEFAULT_GAME_IMAGE
            };
          } catch (error) {
            console.error(`게임 정보 가져오기 오류(ID: ${gameId}):`, error);
            return {
              ...comment,
              gameTitle: `게임 #${gameId}`,
              gameImage: DEFAULT_GAME_IMAGE
            };
          }
        }));
        
        console.log('가공된 댓글 데이터:', enrichedComments);
        setComments(enrichedComments);
        setError(prev => ({ ...prev, comments: null }));
      } catch (err) {
        console.error('댓글 목록 가져오기 오류:', err.message);
        setError(prev => ({ ...prev, comments: err.message }));
      } finally {
        setLoading(prev => ({ ...prev, comments: false }));
      }
    };

    fetchComments();
  }, [token, isAuthenticated, user]);

  // 위시리스트에서 게임 삭제
  const handleRemoveFromWishlist = async (gameId) => {
    if (!isAuthenticated() || !token) {
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/wishlist/game/${gameId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(`위시리스트에서 삭제하는데 실패했습니다 (${response.status})`);
      }

      // 성공적으로 삭제된 경우 UI 업데이트
      setWishlist(prevWishlist => prevWishlist.filter(item => item.gameId !== gameId));
    } catch (err) {
      console.error('위시리스트 삭제 오류:', err.message);
      alert('위시리스트에서 게임을 삭제하는데 문제가 발생했습니다.');
    }
  };

  // 댓글 삭제
  const handleDeleteComment = async (commentId) => {
    if (!isAuthenticated() || !token) {
      return;
    }

    if (!window.confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/reviews/${commentId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(`댓글 삭제에 실패했습니다 (${response.status})`);
      }

      // 성공적으로 삭제된 경우 UI 업데이트
      setComments(prevComments => prevComments.filter(comment => comment.id !== commentId));
    } catch (err) {
      console.error('댓글 삭제 오류:', err.message);
      alert('댓글 삭제 중 문제가 발생했습니다.');
    }
  };

  // 로딩 중이면 로딩 표시
  if (loading.profile) {
    return (
      <div className="profile-page">
        <NavBar />
        <div className="profile-container">
          <div className="loading-message">프로필 정보를 불러오는 중...</div>
        </div>
        <Footer />
      </div>
    );
  }

  // 프로필 정보 로딩 실패
  if (error.profile) {
    return (
      <div className="profile-page">
        <NavBar />
        <div className="profile-container">
          <div className="error-message">
            프로필 정보를 불러오는데 실패했습니다: {error.profile}
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // 프로필 정보가 없으면
  if (!profile) {
    return (
      <div className="profile-page">
        <NavBar />
        <div className="profile-container">
          <div className="error-message">
            프로필 정보를 찾을 수 없습니다. <Link to="/login">로그인</Link>이 필요합니다.
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="profile-page">
      <NavBar />
      <div className="profile-container">
        {/* 프로필 정보 섹션 */}
        <section className="profile-card">
          <div className="profile-header">
            <div className="profile-avatar-container">
              {profile.profile_image ? (
                <img
                  src={profile.profile_image}
                  alt="프로필 이미지"
                  className="profile-avatar"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = DEFAULT_PROFILE_IMAGE;
                  }}
                />
              ) : (
                <img
                  src={DEFAULT_PROFILE_IMAGE}
                  alt="기본 프로필 이미지"
                  className="profile-avatar"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = FALLBACK_IMAGE;
                  }}
                />
              )}
            </div>
            <div className="profile-basic-info">
              <h2 className="profile-name">{profile.first_name || profile.username}</h2>
              <p className="profile-username">@{profile.username}</p>
              <p className="profile-email">{profile.email}</p>
              <p className="profile-joined">가입일: {new Date(profile.date_joined || Date.now()).toLocaleDateString()}</p>
            </div>
          </div>
          <p className="profile-bio">{profile.bio || '자기 소개가 없습니다.'}</p>
          <div className="profile-stats">
            <div className="stat-item">
              <span className="stat-value">{wishlist.length}</span>
              <span className="stat-label">위시리스트</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{comments.length}</span>
              <span className="stat-label">댓글</span>
            </div>
          </div>
        </section>

        {/* 위시리스트 섹션 */}
        <section className="wishlist-card">
          <h3 className="section-title">위시리스트</h3>
          <div className="wishlist-container">
            {loading.wishlist ? (
              <p className="loading-message">위시리스트를 불러오는 중...</p>
            ) : error.wishlist ? (
              <p className="error-message">위시리스트를 불러오는데 실패했습니다: {error.wishlist}</p>
            ) : wishlist.length === 0 ? (
              <p className="empty-message">위시리스트에 게임이 없습니다.</p>
            ) : (
              <ul className="wishlist-items">
                {wishlist.map(game => (
                  <li key={game.id} className="wishlist-item">
                    <div className="wishlist-item-content">
                      <div className="game-image-small">
                        <img 
                          src={game.image} 
                          alt={game.title}
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = DEFAULT_GAME_IMAGE;
                          }}
                        />
                      </div>
                      <div className="game-info">
                        <h4 className="game-title">{game.title}</h4>
                        <p className="game-genre">장르: {game.genre}</p>
                      </div>
                    </div>
                    <div className="wishlist-actions">
                      <button
                        className="remove-button"
                        onClick={() => handleRemoveFromWishlist(game.gameId)}
                      >
                        삭제
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>

        {/* 댓글 섹션 */}
        <section className="comments-card">
          <h3 className="section-title">내 댓글</h3>
          <div className="comments-container">
            {loading.comments ? (
              <p className="loading-message">댓글을 불러오는 중...</p>
            ) : error.comments ? (
              <p className="error-message">댓글을 불러오는데 실패했습니다: {error.comments}</p>
            ) : comments.length === 0 ? (
              <p className="empty-message">작성한 댓글이 없습니다.</p>
            ) : (
              <ul className="comments-list">
                {comments.map(comment => (
                  <li key={comment.id} className="comment-item">
                    <div className="comment-header">
                      <div className="comment-game-info">
                        <Link to={`/game/${comment.game}`} className="game-image-link">
                          <div className="game-image-small">
                            <img 
                              src={comment.gameImage} 
                              alt={comment.gameTitle}
                              onError={(e) => {
                                e.target.onerror = null;
                                e.target.src = DEFAULT_GAME_IMAGE;
                              }}
                            />
                          </div>
                        </Link>
                        <span className="game-title">
                          {comment.gameTitle || comment.game_details?.name || `게임 #${comment.game}`}
                        </span>
                      </div>
                      <span className="comment-date">
                        {comment.updated_at ? new Date(comment.updated_at).toLocaleDateString() : '날짜 정보 없음'}
                      </span>
                    </div>
                    <p className="comment-content">{comment.review || comment.content || '내용 없음'}</p>
                    <div className="comment-actions">
                      <button 
                        className="remove-button"
                        onClick={() => handleDeleteComment(comment.id)}
                      >
                        댓글 삭제
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      </div>
      <Footer />
    </div>
  );
};

export default ProfilePage; 