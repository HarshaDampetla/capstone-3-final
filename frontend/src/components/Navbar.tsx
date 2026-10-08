import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/dashboard">🚀 MarketScope</Link>
      </div>
      {user && (
        <div className="nav-links">
          {user.role === "CUSTOMER" && (
            <>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/stocks">Stocks</Link>
              <Link to="/watchlists">Watchlists</Link>
              <Link to="/orders">Orders</Link>
              <Link to="/portfolio">Portfolio</Link>
              <Link to="/analytics">Analytics</Link>
              <Link to="/profile">Profile</Link>
            </>
          )}

          {user.role === "ADMIN" && (
            <>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/admin/users">Users</Link>
              <Link to="/admin/stocks">Catalog</Link>
              <Link to="/admin/orders">Orders</Link>
              <Link to="/admin/statistics">Stats</Link>
            </>
          )}
        </div>
      )}
      <div className="nav-user">
        {user ? (
          <>
            <span className="user-badge">{user.role}</span>
            <span className="user-email">{user.email}</span>
            {user.role === "CUSTOMER" && (
              <span className="cash-badge">Cash: ${user.available_cash}</span>
            )}
            <button className="btn-logout" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn-link">Login</Link>
            <Link to="/register" className="btn-primary">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};
