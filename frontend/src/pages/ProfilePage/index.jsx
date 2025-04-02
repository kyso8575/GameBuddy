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

// 서버로부터 받은 이미지 URL이 기본 이미지인지 확인하는 함수
const isDefaultProfileImage = (url) => {
  return !url || url.includes('default_profile.png');
};

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
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const fileInputRef = React.useRef(null);
  const [imageKey, setImageKey] = useState(Date.now());

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
        console.log('프로필 정보 응답:', data); // 응답 데이터 확인
        
        // 프로필 이미지가 있고 기본 이미지가 아닌 경우에만 URL 처리
        if (data.profile_image && !isDefaultProfileImage(data.profile_image)) {
          // URL 인코딩 문제를 방지하기 위해 전체 URL 구조 확인
          try {
            // URL 객체를 사용하여 유효성 검사 및 정규화
            const imageUrl = new URL(data.profile_image, 'http://127.0.0.1:8000');
            data.profile_image = imageUrl.href;
            console.log('정규화된 이미지 URL:', data.profile_image);
          } catch (urlError) {
            console.error('이미지 URL 파싱 오류:', urlError);
            // 백엔드에서 받은 URL을 그대로 사용
          }
          
          // 캐시 버스팅을 위한 타임스탬프 추가
          data.profile_image = data.profile_image.includes('?') 
            ? `${data.profile_image}&t=${new Date().getTime()}` 
            : `${data.profile_image}?t=${new Date().getTime()}`;
        } else {
          // 기본 이미지이거나 이미지가 없는 경우는 null로 설정하여 로컬 이미지 사용
          data.profile_image = null;
        }
        
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

  // 프로필 이미지 업로드 함수
  const handleProfileImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // 파일 타입 검증
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setUploadError('이미지 파일(JPEG, PNG, GIF, WEBP)만 업로드 가능합니다.');
      return;
    }

    // 파일 크기 검증 (5MB 제한)
    if (file.size > 5 * 1024 * 1024) {
      setUploadError('파일 크기는 5MB 이하여야 합니다.');
      return;
    }

    setIsUploading(true);
    setUploadError(null);

    try {
      const formData = new FormData();
      formData.append('profile_image', file);

      const response = await fetch('http://127.0.0.1:8000/accounts/update-profile-image/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error(`이미지 업로드 실패 (${response.status})`);
      }

      const data = await response.json();
      console.log('이미지 업로드 응답:', data);
      
      // 이미지 URL 검증 및 캐시 방지
      let imagePath = data.profile_image;
      
      // URL 객체로 변환하여 유효성 검사
      try {
        const imageUrl = new URL(imagePath, 'http://127.0.0.1:8000');
        imagePath = imageUrl.href;
        console.log('정규화된 업로드 이미지 URL:', imagePath);
      } catch (urlError) {
        console.error('업로드 이미지 URL 파싱 오류:', urlError);
        // 원래 URL 유지
      }
      
      // 캐시 방지를 위한 타임스탬프 추가
      const imageWithTimestamp = imagePath.includes('?') 
        ? `${imagePath}&t=${new Date().getTime()}` 
        : `${imagePath}?t=${new Date().getTime()}`;
      
      // 프로필 상태 업데이트
      setProfile(prevProfile => ({
        ...prevProfile,
        profile_image: imageWithTimestamp
      }));
      
      // 이미지 갱신을 위한 키 업데이트
      setImageKey(Date.now());

      // 성공 메시지 표시
      alert('프로필 이미지가 성공적으로 업데이트되었습니다.');
      
      // 2초 후 페이지 새로고침
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err) {
      console.error('이미지 업로드 오류:', err.message);
      setUploadError('이미지 업로드 중 오류가 발생했습니다. 다시 시도해 주세요.');
    } finally {
      setIsUploading(false);
      // 파일 입력 초기화
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  // 이미지 업로드 버튼 클릭 핸들러
  const handleUploadButtonClick = () => {
    fileInputRef.current?.click();
  };

  // 프로필 이미지 삭제 함수 수정
  const handleDeleteProfileImage = async () => {
    if (!isAuthenticated() || !token) {
      return;
    }

    // 사용자 확인
    if (!window.confirm('프로필 이미지를 삭제하고 기본 이미지로 돌아가시겠습니까?')) {
      return;
    }

    setIsUploading(true);
    setUploadError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/accounts/update-profile-image/', {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`이미지 삭제 실패 (${response.status})`);
      }

      const data = await response.json();
      console.log('이미지 삭제 응답:', data);

      // 프로필 상태 업데이트 (기본 이미지로 설정)
      setProfile(prevProfile => ({
        ...prevProfile,
        profile_image: null // 로컬 기본 이미지 사용
      }));
      
      // 이미지 갱신을 위한 키 업데이트
      setImageKey(Date.now());

      // 성공 메시지 표시
      alert('프로필 이미지가 성공적으로 삭제되었습니다.');
      
      // 페이지 새로고침
      setTimeout(() => {
        window.location.reload();
      }, 1000);
    } catch (err) {
      console.error('이미지 삭제 오류:', err.message);
      setUploadError('이미지 삭제 중 오류가 발생했습니다. 다시 시도해 주세요.');
    } finally {
      setIsUploading(false);
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
                  key={imageKey}
                  src={`${profile.profile_image}`}
                  alt="프로필 이미지"
                  className="profile-avatar"
                  crossOrigin="anonymous"
                  onError={(e) => {
                    console.error('프로필 이미지 로드 실패:', e);
                    // 디버깅을 위해 추가 정보 출력
                    console.log('시도한 이미지 URL:', e.target.src);
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
                    console.error('기본 이미지 로드 실패:', e);
                    console.log('시도한 기본 이미지 URL:', e.target.src);
                    e.target.onerror = null;
                    e.target.src = FALLBACK_IMAGE;
                  }}
                />
              )}
              <div className="profile-image-upload">
                <input
                  type="file"
                  accept="image/*"
                  ref={fileInputRef}
                  onChange={handleProfileImageUpload}
                  style={{ display: 'none' }}
                />
                <div className="profile-image-buttons">
                  <button 
                    className="upload-button"
                    onClick={handleUploadButtonClick}
                    disabled={isUploading}
                  >
                    {isUploading ? '업로드 중...' : '이미지 변경'}
                  </button>
                  {profile.profile_image && (
                    <button 
                      className="delete-button"
                      onClick={handleDeleteProfileImage}
                      disabled={isUploading}
                    >
                      삭제
                    </button>
                  )}
                </div>
                {uploadError && <p className="upload-error">{uploadError}</p>}
              </div>
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