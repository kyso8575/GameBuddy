import React from 'react';
import { Link } from 'react-router-dom';
import { Gamepad2 } from 'lucide-react';
import '../styles/NavBar.css';

function NavBar() {
  return (
    <header className="header">
      <nav className="nav-container">
        <div className="logo-container">
          <Gamepad2 size={36} className="gamepad-icon" />
          <Link to="/" className="logo">GameFinder</Link>
        </div>
        <ul className="menu">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/chatbot">Chatbot</Link></li>
          <li><Link to="/browse">Browse</Link></li>
          <li><Link to="/about">About</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default NavBar;
