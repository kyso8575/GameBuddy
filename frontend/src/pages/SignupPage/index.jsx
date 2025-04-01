import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Gamepad2 } from 'lucide-react';
import { postWithoutAuth } from '../../utils/api';
import { useAuth } from '../../contexts/AuthContext';
import '../../styles/SignupPage.css';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    password: '',
    confirm_password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth(); // AuthContext에서 login 함수 가져오기

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // 기본 유효성 검사
    if (!formData.first_name || !formData.last_name || !formData.username || !formData.password || !formData.confirm_password) {
      setError('Please fill in all fields.');
      return;
    }

    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match.');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // 회원가입 요청 - 인증이 필요없는 API 호출
      const response = await postWithoutAuth('/accounts/signup/', formData);
      
      if (response.ok) {
        const data = await response.json();
        // AuthContext의 login 함수 사용
        login(data.user, data.token);
        // Redirect to homepage
        navigate('/');
      } else {
        // 서버에서 오류 응답을 받은 경우
        const errorData = await response.json();
        console.log('Error response:', errorData); // 디버깅용 로그
        
        // Django ValidationError 처리
        if (errorData.detail) {
          // 오류 메시지를 처리하는 함수
          const translateErrorMessages = (messages) => {
            if (!messages) return ['Sign up failed.'];
            
            // 문자열이나 배열을 항상 배열로 처리
            const messageArray = Array.isArray(messages) ? messages : [messages];
            
            return messageArray.map(msg => {
              // 비밀번호 오류 메시지를 사용자 친화적으로 변환
              if (msg === 'This password is too common.') {
                return 'This password is too common. Please use a more unique password.';
              } else if (msg === 'This password is entirely numeric.') {
                return 'This password consists only of numbers. Please include letters.';
              } else if (msg.includes('similar to') || msg.includes('based on')) {
                return 'Password is too similar to your personal information. Please use a different password.';
              }
              return msg; // 기타 오류 메시지는 그대로 사용
            });
          };
          
          const errorMessages = translateErrorMessages(errorData.detail);
          setError(errorMessages.join('\n'));
        } else {
          setError('Sign up failed. Please try again.');
        }
      }
    } catch (err) {
      console.error('Signup error:', err);
      
      // HTML 응답에서 추출된 ValidationError 처리
      if (err.validationErrors) {
        const errorMessages = err.validationErrors.map(msg => {
          // 비밀번호 오류 메시지를 사용자 친화적으로 변환
          if (msg === 'This password is too common.') {
            return 'This password is too common. Please use a more unique password.';
          } else if (msg === 'This password is entirely numeric.') {
            return 'This password consists only of numbers. Please include letters.';
          } else if (msg.includes('similar to') || msg.includes('based on')) {
            return 'Password is too similar to your personal information. Please use a different password.';
          }
          return msg; // 기타 오류 메시지는 그대로 사용
        });
        
        setError(errorMessages.join('\n'));
        return;
      }
      
      // 응답을 파싱할 수 없는 경우 (JSON이 아닌 경우)
      if (err.name === 'SyntaxError' && err.message.includes('JSON')) {
        setError('서버에서 잘못된 응답 형식을 받았습니다.');
        return;
      }
      
      // 서버에서 온 오류 메시지에서 ValidationError 추출
      const errorMessage = err.message || '';
      
      if (errorMessage.includes('ValidationError')) {
        // Django ValidationError 메시지 추출
        try {
          // ValidationError: ['This password is too common.'] 형식에서 메시지 추출
          const regex = /ValidationError: \[(.*?)\]/;
          const match = errorMessage.match(regex);
          
          if (match && match[1]) {
            const errorMessages = match[1].split(',').map(msg => {
              // 따옴표 제거 및 공백 정리
              msg = msg.replace(/['"]/g, '').trim();
              
              // 비밀번호 오류 메시지를 사용자 친화적으로 변환
              if (msg === 'This password is too common.') {
                return 'This password is too common. Please use a more unique password.';
              } else if (msg === 'This password is entirely numeric.') {
                return 'This password consists only of numbers. Please include letters.';
              } else if (msg.includes('similar to') || msg.includes('based on')) {
                return 'Password is too similar to your personal information. Please use a different password.';
              }
              return msg; // 기타 오류 메시지는 그대로 사용
            });
            
            setError(errorMessages.join('\n'));
            return;
          }
        } catch (parseError) {
          console.error('Error parsing validation message:', parseError);
        }
      }
      
      // 기본 오류 메시지
      setError('An error occurred while communicating with the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page-container">
      <Link to="/" className="home-logo">
        <Gamepad2 size={32} />
        <span>GameBuddy</span>
      </Link>
      
      <main className="signup-container">
        <div className="signup-form-wrapper">
          <h1 className="signup-title">Sign Up</h1>
          {error && (
            <div className="error-message">
              {error.split('\n').map((msg, index) => (
                <div key={index} className="error-item">{msg}</div>
              ))}
            </div>
          )}
          
          <form className="signup-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="first_name">First Name</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="Enter your first name"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="last_name">Last Name</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="Enter your last name"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter your username"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password (min. 8 characters)"
                minLength="8"
                required
              />
              <div className="password-requirements">
                Password must meet the following requirements:
                <ul>
                  <li>Minimum 8 characters</li>
                  <li>Include a combination of letters and numbers</li>
                  <li>Cannot consist of numbers only</li>
                  <li>Cannot use common passwords (e.g. 12345678, password, etc.)</li>
                </ul>
              </div>
            </div>
            
            <div className="form-group">
              <label htmlFor="confirm_password">Confirm Password</label>
              <input
                type="password"
                id="confirm_password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                placeholder="Confirm your password"
                minLength="8"
                required
              />
            </div>
            
            <button 
              type="submit" 
              className="signup-button"
              disabled={loading}
            >
              {loading ? 'Signing up...' : 'Sign Up'}
            </button>
          </form>
          
          <div className="signup-footer">
            <p>Already have an account? <Link to="/login">Login</Link></p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default SignupPage; 