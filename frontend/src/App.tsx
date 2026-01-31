import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '@/context/AuthContext';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { Navbar } from '@/components/Navbar';
import { LoginPage } from '@/pages/LoginPage';
import { UserDashboard } from '@/pages/UserDashboard';
import { AdminDashboard } from '@/pages/AdminDashboard';
import { SavedDesignsPage } from '@/pages/SavedDesignsPage';
import { ProfilePage } from '@/pages/ProfilePage';
import { DesignSuggestionPage } from '@/pages/DesignSuggestionPage';
import './index.css';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          <Route
            path="/user-dashboard"
            element={
              <ProtectedRoute requiredRole="user">
                <Navbar />
                <UserDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin-dashboard"
            element={
              <ProtectedRoute requiredRole="admin">
                <Navbar />
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/saved-designs"
            element={
              <ProtectedRoute requiredRole="user">
                <Navbar />
                <SavedDesignsPage />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/design-suggestions/:uploadId"
            element={
              <ProtectedRoute requiredRole="user">
                <Navbar />
                <DesignSuggestionPage />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Navbar />
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
