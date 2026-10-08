import React, { useEffect, useState } from "react";
import { getPortfolioStats } from "../services/api";

export const PortfolioPage: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadPortfolioData = async () => {
    setLoading(true);
    try {
      const data = await getPortfolioStats();
      setStats(data);
    } catch (err: any) {
      setError(err.message || "Failed to load portfolio stats");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPortfolioData();
  }, []);

  if (loading) return <div className="loading-spinner">Loading portfolio performance metrics...</div>;
  if (error) return <div className="error-banner">{error}</div>;

  return (
    <div className="page-container">
      <h1>Portfolio & Holdings Valuation (AC-09)</h1>
      <p className="subtitle">All calculations strictly enforce Python Decimal arithmetic.</p>

      {stats && (
        <div className="stats-grid" style={{ marginBottom: "2rem" }}>
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
      )}
    </div>
  );
};
