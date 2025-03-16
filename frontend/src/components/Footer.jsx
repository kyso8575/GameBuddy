import React from 'react';
import '../styles/Footer.css';

function Footer() {
  return (
    <div className="footer-container">
      <footer className="footer">
        <div className="footer-info">
          <h4>GameFinder</h4>
          <p>Find your next favorite game with our personalized recommendations.</p>
        </div>
        <div className="footer-links">
          <h4>Quick Links</h4>
          <ul>
            <li>Home</li>
            <li>Chatbot</li>
            <li>Browse</li>
          </ul>
        </div>
        <div className="footer-genres">
          <h4>Genres</h4>
          <ul>
            <li>Action</li>
            <li>RPG</li>
            <li>Strategy</li>
          </ul>
        </div>
        <div className="footer-follow">
          <h4>Follow Us</h4>
          <ul>
            <li>🐦</li>
            <li>📘</li>
            <li>📸</li>
          </ul>
        </div>
      </footer>
      <div className="footer-bottom">
        © 2025 GameFinder. All rights reserved.
      </div>
    </div>
  );
}

export default Footer; 