import React, { useEffect, useState } from "react";
import { listAdminUsers, updateAdminUserRole, suspendAdminUser, reactivateAdminUser } from "../../services/api";

export const AdminUsersPage: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await listAdminUsers();
      setUsers(data);
    } catch (err: any) {
      setError(err.message || "Failed to load admin user list");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleRoleChange = async (userId: number, currentRole: string) => {
    setError("");
    setSuccess("");
    const newRole = currentRole === "ADMIN" ? "CUSTOMER" : "ADMIN";
    try {
      await updateAdminUserRole(userId, newRole);
      setSuccess(`Role for User #${userId} updated to ${newRole} (AC-02)!`);
      loadUsers();
    } catch (err: any) {
      setError(err.message || "Role change failed");
    }
  };

  const handleToggleSuspend = async (userId: number, currentState: string) => {
    setError("");
    setSuccess("");
    try {
      if (currentState === "ACTIVE") {
        await suspendAdminUser(userId);
        setSuccess(`User #${userId} suspended (AC-02)!`);
      } else {
        await reactivateAdminUser(userId);
        setSuccess(`User #${userId} reactivated (AC-02)!`);
      }
      loadUsers();
    } catch (err: any) {
      setError(err.message || "Action failed");
    }
  };

  return (
    <div className="page-container">
      <h1>Admin User Management (AC-02)</h1>
      <p className="subtitle">Role partitioning & account state management (ACTIVE / SUSPENDED).</p>

      {error && <div className="error-banner">{error}</div>}
      {success && <div className="success-banner">{success}</div>}

      {loading ? (
        <div className="loading-spinner">Loading users...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Role</th>
              <th>Account State</th>
              <th>Available Cash</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>#{u.id}</td>
                <td>{u.email}</td>
                <td>
                  <span className="user-badge">{u.role}</span>
                </td>
                <td>
                  <span className={`status-badge status-${u.state.toLowerCase()}`}>
                    {u.state}
                  </span>
                </td>
                <td>${u.available_cash}</td>
                <td>
                  <button className="btn-secondary" onClick={() => handleRoleChange(u.id, u.role)}>
                    Switch to {u.role === "ADMIN" ? "CUSTOMER" : "ADMIN"}
                  </button>
                  <button
                    className={u.state === "ACTIVE" ? "btn-danger-sm" : "btn-success-sm"}
                    onClick={() => handleToggleSuspend(u.id, u.state)}
                    style={{ marginLeft: "0.5rem" }}
                  >
                    {u.state === "ACTIVE" ? "Suspend" : "Reactivate"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
