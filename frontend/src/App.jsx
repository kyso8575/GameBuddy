import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import MainPage from "./pages/MainPage";
import ChatbotPage from "./pages/ChatbotPage";
import GameDetailPage from "./pages/GameDetailPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import ProfilePage from "./pages/ProfilePage";

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  // Show loading indicator while authentication info is loading
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  // Redirect to login page if not authenticated
  if (!isAuthenticated()) {
    return <Navigate to="/login" />;
  }
  
  // Render children if authenticated
  return children;
};

// Route that redirects authenticated users to home
const AuthRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  if (isAuthenticated()) {
    return <Navigate to="/" />;
  }
  
  return children;
};

// Router separated into a separate component (AuthProvider uses useNavigate)
const AppRouter = () => {
  return (
    <AuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={
          <AuthRoute>
            <LoginPage />
          </AuthRoute>
        } />
        <Route path="/signup" element={
          <AuthRoute>
            <SignupPage />
          </AuthRoute>
        } />
        
        {/* Public game routes - accessible without login */}
        <Route path="/" element={<MainPage />} />
        <Route path="/game/:id" element={<GameDetailPage />} />
        
        {/* Protected routes */}
        <Route path="/chatbot" element={
          <ProtectedRoute>
            <ChatbotPage />
          </ProtectedRoute>
        } />
        <Route path="/profile" element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        } />
      </Routes>
    </AuthProvider>
  );
};

const App = () => {
  return (
    <Router>
      <AppRouter />
    </Router>
  );
};

export default App;
