import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: "CUSTOMER" | "ADMIN";
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading-spinner">Loading authentication...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.state === "SUSPENDED" || user.role === "SUSPENDED") {
    return (
      <div className="error-banner" style={{ margin: "2rem", padding: "1.5rem" }}>
        <h2>Account Suspended</h2>
        <p>Your account has been suspended. Access to protected features is restricted.</p>
      </div>
    );
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};
