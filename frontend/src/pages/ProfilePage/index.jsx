import React, { useState } from 'react';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import './styles.css';

const ProfilePage = () => {
  // Sample profile data for UI demonstration
  const [profile] = useState({
    name: '사용자명',
    username: 'user123',
    email: 'user@example.com',
    bio: '게임을 좋아하는 유저입니다. RPG와 전략 게임을 주로 플레이합니다.',
    avatarUrl: '', // 실제 URL이 있으면 교체
    date_joined: '2023-01-01'
  });

  // Sample wishlist data
  const [wishlist] = useState([
    { id: 1, title: '엘든 링', genre: 'RPG', image: 'https://via.placeholder.com/150' },
    { id: 2, title: '문명 VI', genre: '전략', image: 'https://via.placeholder.com/150' },
    { id: 3, title: '하데스', genre: '액션 로그라이크', image: 'https://via.placeholder.com/150' },
    { id: 4, title: '젤다의 전설', genre: '어드벤처', image: 'https://via.placeholder.com/150' }
  ]);

  // Sample comments data
  const [comments] = useState([
    { 
      id: 1, 
      game: { title: '엘든 링', id: 1 }, 
      content: '이 게임은 정말 재미있어요! 오픈 월드의 자유도가 매력적입니다.', 
      created_at: '2023-01-15' 
    },
    { 
      id: 2, 
      game: { title: '문명 VI', id: 2 }, 
      content: '전략 게임 중에서 최고입니다. 그래픽도 아주 훌륭합니다.', 
      created_at: '2023-02-20' 
    },
    { 
      id: 3, 
      game: { title: '하데스', id: 3 }, 
      content: '스토리와 게임플레이 모두 매력적이에요. 추천합니다!', 
      created_at: '2023-03-10' 
    }
  ]);

  return (
    <div className="profile-page">
      <NavBar />
      <div className="profile-container">
        {/* 프로필 정보 섹션 */}
        <section className="profile-card">
          <div className="profile-header">
            <div className="profile-avatar-container">
              {profile.avatarUrl ? (
                <img
                  src={profile.avatarUrl}
                  alt="프로필 이미지"
                  className="profile-avatar"
                />
              ) : (
                <div className="profile-avatar-placeholder">
                  <span>이미지 없음</span>
                </div>
              )}
            </div>
            <div className="profile-basic-info">
              <h2 className="profile-name">{profile.name}</h2>
              <p className="profile-username">@{profile.username}</p>
              <p className="profile-email">{profile.email}</p>
              <p className="profile-joined">가입일: {new Date(profile.date_joined).toLocaleDateString()}</p>
            </div>
          </div>
          <p className="profile-bio">{profile.bio}</p>
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
            {wishlist.length === 0 ? (
              <p className="empty-message">위시리스트에 게임이 없습니다.</p>
            ) : (
              <ul className="wishlist-items">
                {wishlist.map(game => (
                  <li key={game.id} className="wishlist-item">
                    <div className="game-image-small">
                      <img src={game.image} alt={game.title} />
                    </div>
                    <div className="game-info">
                      <h4 className="game-title">{game.title}</h4>
                      <p className="game-genre">장르: {game.genre}</p>
                    </div>
                    <button className="remove-button">삭제</button>
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
            {comments.length === 0 ? (
              <p className="empty-message">작성한 댓글이 없습니다.</p>
            ) : (
              <ul className="comments-list">
                {comments.map(comment => (
                  <li key={comment.id} className="comment-item">
                    <div className="comment-header">
                      <span className="game-title">{comment.game.title}</span>
                      <span className="comment-date">
                        {new Date(comment.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="comment-content">{comment.content}</p>
                    <a href={`/game/${comment.game.id}`} className="goto-game">
                      게임 페이지로 이동
                    </a>
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