import React from 'react';
import NavBar from '../../components/NavBar';
import Footer from '../../components/Footer';
import './ChatbotPage.css';

function ChatbotPage() {
  return (
    <div className="app">
      {/* NavBar 컴포넌트 재사용 */}
      <NavBar />

      {/* 챗봇 페이지 콘텐츠 */}
      <main className="chatbot-content">
        <h1>Game Recommendation Chatbot</h1>
        <p>Ask our AI to recommend games based on your preferences!</p>
        
        <div className="chat-container">
          <div className="chat-messages">
            <div className="message bot">
              Hello! I can help you find your next favorite game. What type of games do you enjoy?
            </div>
            <div className="message user">
              I like strategy games with good storylines
            </div>
            <div className="message bot">
              Great! Here are some strategy games with compelling stories:
              <ul>
                <li>Civilization VI</li>
                <li>XCOM 2</li>
                <li>Fire Emblem: Three Houses</li>
                <li>Into the Breach</li>
              </ul>
              Would you like more recommendations or details about any of these games?
            </div>
          </div>
          
          <div className="chat-input">
            <input 
              type="text" 
              placeholder="Type your message here..." 
              className="message-input"
            />
            <button className="send-button">Send</button>
          </div>
        </div>
      </main>

      {/* Footer 컴포넌트 재사용 */}
      <Footer />
    </div>
  );
}

export default ChatbotPage; 