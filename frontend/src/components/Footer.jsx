import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Footer.css';

function Footer() {
  return (
    <div className="footer-container">
      <footer className="footer">
        <div className="footer-about">
          <h4>GameBuddy</h4>
          <p>Your personal guide to the gaming world. Discover, explore, and find your next favorite game.</p>
          <div className="social-icons">
            <span className="social-icon">🐦</span>
            <span className="social-icon">📘</span>
            <span className="social-icon">📸</span>
            <span className="social-icon">📱</span>
          </div>
        </div>
        
        <div className="footer-links">
          <h4>Explore</h4>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/chatbot">Chatbot</Link></li>
          </ul>
        </div>
        
        <div className="footer-links">
          <h4>Resources</h4>
          <ul>
            <li>Privacy Policy</li>
            <li>Terms of Service</li>
            <li>Cookie Policy</li>
          </ul>
        </div>
        
        <div className="footer-contact">
          <h4>Contact Us</h4>
          <p>Email: support@gamebuddy.com</p>
        </div>

      </footer>
    </div>
  );
}

export default Footer; 