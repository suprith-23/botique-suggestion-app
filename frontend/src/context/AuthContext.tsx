import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthToken } from '@/types';
import { api } from '@/services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string, isAdmin: boolean) => Promise<void>;
  register: (email: string, username: string, password: string, fullName: string, isAdmin: boolean) => Promise<void>;
  logout: () => void;
  updateUser: (fullName?: string, password?: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string, isAdmin: boolean) => {
    try {
      const response = await api.login(email, password);
      const data: AuthToken = response.data;

      if (isAdmin && data.user.role !== 'admin') {
        throw new Error('Not an admin account');
      }

      setToken(data.access_token);
      setUser(data.user);
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, username: string, password: string, fullName: string, isAdmin: boolean) => {
    try {
      const response = isAdmin
        ? await api.registerAdmin(email, username, password, fullName)
        : await api.registerUser(email, username, password, fullName);

      const user: User = response.data;
      setUser(user);
      localStorage.setItem('user', JSON.stringify(user));
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const updateUser = async (fullName?: string, password?: string) => {
    try {
      const response = await api.updateUser(fullName, password);
      const updatedUser: User = response.data;
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
    } catch (error) {
      throw error;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isAuthenticated: !!token,
        login,
        register,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
