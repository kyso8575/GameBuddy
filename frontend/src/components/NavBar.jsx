import React from 'react';
import { Link } from 'react-router-dom';
import { Gamepad2, User, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import '../styles/NavBar.css';

function NavBar() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="header">
      <nav className="nav-container">
        <div className="logo-container">
          <Gamepad2 size={36} className="gamepad-icon" />
          <Link to="/" className="logo">GameBuddy</Link>
        </div>
        <ul className="menu">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/chatbot">Chatbot</Link></li>
          <li><Link to="/browse">Browse</Link></li>
          <li><Link to="/about">About</Link></li>
        </ul>
        <div className="auth-buttons">
          {isAuthenticated() ? (
            <>
              <Link to="/profile" className="auth-btn profile-btn">
                <User size={18} />
                <span>{user?.first_name || user?.username || 'Profile'}</span>
              </Link>
              <button onClick={logout} className="auth-btn logout-btn">
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="auth-btn login-btn">Login</Link>
              <Link to="/signup" className="auth-btn signup-btn">Sign Up</Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}

export default NavBar;
