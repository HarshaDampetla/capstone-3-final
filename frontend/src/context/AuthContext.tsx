import React, { createContext, useContext, useState, useEffect } from "react";
import { getToken, setToken, clearToken, loginUser, registerUser, getProfile } from "../services/api";

interface User {
  id: number;
  email: string;
  role: "CUSTOMER" | "ADMIN" | "SUSPENDED";
  state: "ACTIVE" | "SUSPENDED";
  available_cash: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  register: (email: string, pass: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setTokenState] = useState<string | null>(getToken());
  const [loading, setLoading] = useState<boolean>(true);

  const refreshUser = async () => {
    if (!getToken()) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const u = await getProfile();
      setUser(u as User);
    } catch {
      clearToken();
      setTokenState(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (email: string, pass: string) => {
    const res = await loginUser({ email, password: pass });
    setToken(res.access_token);
    setTokenState(res.access_token);
    const u = await getProfile();
    setUser(u as User);
  };

  const register = async (email: string, pass: string) => {
    await registerUser({ email, password: pass });
    await login(email, pass);
  };

  const logout = () => {
    clearToken();
    setTokenState(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
