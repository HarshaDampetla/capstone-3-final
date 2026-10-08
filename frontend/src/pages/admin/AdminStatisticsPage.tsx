import React, { useEffect, useState } from "react";
import { getPlatformAnalytics, triggerMarketTick } from "../../services/api";

export const AdminStatisticsPage: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [tickMsg, setTickMsg] = useState("");

  const loadPlatformStats = async () => {
    setLoading(true);
    try {
      const data = await getPlatformAnalytics();
      setStats(data);
    } catch (err: any) {
      setError(err.message || "Failed to load platform stats");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlatformStats();
  }, []);

  const handleTick = async () => {
    try {
      const res = await triggerMarketTick();
      setTickMsg(`Triggered market tick for ${res.ticked_stocks_count} stock catalog items.`);
      loadPlatformStats();
    } catch (err: any) {
      setTickMsg(`Market tick error: ${err.message}`);
    }
  };

  if (loading) return <div className="loading-spinner">Loading platform analytics...</div>;
  if (error) return <div className="error-banner">{error}</div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Platform Order Statistics & Settlement Queue</h1>
        <button className="btn-secondary" onClick={handleTick}>
          ⚡ Trigger Market Random-Walk Tick
        </button>
      </div>

      {tickMsg && <div className="info-banner">{tickMsg}</div>}

      {stats && (
        <>
          <div className="stats-grid" style={{ marginBottom: "2rem" }}>
            <div className="stat-card">
              <span className="stat-label">Total Platform Orders</span>
              <span className="stat-value">{stats.total_orders}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Settlement Queue Length</span>
              <span className="stat-value">{stats.settlement_queue_length}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Executed Orders</span>
              <span className="stat-value">{stats.volume_by_status.EXECUTED || 0}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Cancelled Orders</span>
              <span className="stat-value">{stats.volume_by_status.CANCELLED || 0}</span>
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="card">
              <h3>🔥 Most Traded Symbols</h3>
              {stats.most_traded_symbols.length === 0 ? (
                <div className="empty-state">No trade history available yet.</div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Symbol</th>
                      <th>Trade Count</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.most_traded_symbols.map((item: any) => (
                      <tr key={item.symbol}>
                        <td><strong>{item.symbol}</strong></td>
                        <td>{item.trade_count} trades</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            <div className="card">
              <h3>⏳ Settlement Queue (Pending Orders)</h3>
              {stats.settlement_queue.length === 0 ? (
                <div className="empty-state">Settlement queue is currently empty.</div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Order ID</th>
                      <th>Symbol</th>
                      <th>Side</th>
                      <th>Price</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.settlement_queue.map((q: any) => (
                      <tr key={q.order_id}>
                        <td>#{q.order_id}</td>
                        <td><strong>{q.symbol}</strong></td>
                        <td>{q.side}</td>
                        <td>${q.quote_price}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
