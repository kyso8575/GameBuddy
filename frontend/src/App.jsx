import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage";
import ChatbotPage from "./pages/ChatbotPage";
import GameDetailPage from "./pages/GameDetailPage";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/chatbot" element={<ChatbotPage />} />
        <Route path="/game/:id" element={<GameDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
