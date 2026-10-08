import React from "react";
import { useAuth } from "../context/AuthContext";

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="page-container">
      <h1>Customer Account Profile</h1>

      {user && (
        <div className="card" style={{ maxWidth: "600px" }}>
          <div className="profile-detail">
            <strong>User ID:</strong> #{user.id}
          </div>
          <div className="profile-detail">
            <strong>Email Address:</strong> {user.email}
          </div>
          <div className="profile-detail">
            <strong>Account Role:</strong> <span className="user-badge">{user.role}</span>
          </div>
          <div className="profile-detail">
            <strong>Account State:</strong> <span className={`status-badge status-${user.state.toLowerCase()}`}>{user.state}</span>
          </div>
          <div className="profile-detail">
            <strong>Available Cash Balance:</strong> ${user.available_cash}
          </div>
        </div>
      )}
    </div>
  );
};
