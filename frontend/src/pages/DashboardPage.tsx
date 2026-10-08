import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getPortfolioStats, getDailyAnalytics, triggerMarketTick } from "../services/api";

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<any>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [tickMessage, setTickMessage] = useState("");

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      if (user?.role === "CUSTOMER") {
        const [s, a] = await Promise.all([getPortfolioStats(), getDailyAnalytics()]);
        setStats(s);
        setAnalytics(a);
      }
    } catch (err: any) {
      console.error("Dashboard error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, [user]);

  const handleTick = async () => {
    try {
      const res = await triggerMarketTick();
      setTickMessage(`Updated ${res.ticked_stocks_count} stock prices in synthetic market random-walk tick.`);
      loadDashboardData();
    } catch (err: any) {
      setTickMessage(`Market tick error: ${err.message}`);
    }
  };

  if (loading) return <div className="loading-spinner">Loading dashboard analytics...</div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Welcome, {user?.email}</h1>
        <button className="btn-secondary" onClick={handleTick}>
          ⚡ Trigger Market Random-Walk Tick
        </button>
      </div>

      {tickMessage && <div className="info-banner">{tickMessage}</div>}

      {user?.role === "CUSTOMER" && stats && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Total Invested</span>
              <span className="stat-value">${stats.total_invested}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Current Value</span>
              <span className="stat-value">${stats.current_value}</span>
            </div>
            <div className={`stat-card ${Number(stats.absolute_pnl) >= 0 ? "positive" : "negative"}`}>
              <span className="stat-label">Absolute P&L</span>
              <span className="stat-value">${stats.absolute_pnl}</span>
            </div>
            <div className={`stat-card ${Number(stats.percent_pnl) >= 0 ? "positive" : "negative"}`}>
              <span className="stat-label">Percentage P&L</span>
              <span className="stat-value">{stats.percent_pnl}%</span>
            </div>
          </div>

          {analytics && (
            <div className="dashboard-grid">
              <div className="card">
                <h3>📈 Top Gainers (AC-10)</h3>
                {analytics.top_gainers.length === 0 ? (
                  <p className="empty-state">No holdings available to rank gainers.</p>
                ) : (
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Symbol</th>
                        <th>Avg Buy Price</th>
                        <th>Current Price</th>
                        <th>Gain</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analytics.top_gainers.map((g: any) => (
                        <tr key={g.symbol}>
                          <td><strong>{g.symbol}</strong></td>
                          <td>${g.average_buy_price}</td>
                          <td>${g.current_price}</td>
                          <td className="text-green">+{g.percent_pnl}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>

              <div className="card">
                <h3>📉 Top Losers (AC-10)</h3>
                {analytics.top_losers.length === 0 ? (
                  <p className="empty-state">No holdings available to rank losers.</p>
                ) : (
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Symbol</th>
                        <th>Avg Buy Price</th>
                        <th>Current Price</th>
                        <th>Loss</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analytics.top_losers.map((l: any) => (
                        <tr key={l.symbol}>
                          <td><strong>{l.symbol}</strong></td>
                          <td>${l.average_buy_price}</td>
                          <td>${l.current_price}</td>
                          <td className="text-red">{l.percent_pnl}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {user?.role === "ADMIN" && (
        <div className="admin-welcome-card">
          <h2>Admin Control Center</h2>
          <p>You have administrative access to user role partitioning, stock catalog CRUD, order auditing, and platform analytics.</p>
          <div className="quick-links">
            <Link to="/admin/users" className="btn-primary">Manage Users</Link>
            <Link to="/admin/stocks" className="btn-primary">Manage Catalog</Link>
            <Link to="/admin/statistics" className="btn-primary">Platform Stats</Link>
          </div>
        </div>
      )}
    </div>
  );
};
