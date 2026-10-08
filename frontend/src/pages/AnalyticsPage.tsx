import React, { useEffect, useState } from "react";
import { getDailyAnalytics } from "../services/api";

export const AnalyticsPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const data = await getDailyAnalytics();
      setAnalytics(data);
    } catch (err: any) {
      setError(err.message || "Failed to load daily analytics");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (loading) return <div className="loading-spinner">Loading analytics metrics...</div>;
  if (error) return <div className="error-banner">{error}</div>;

  return (
    <div className="page-container">
      <h1>Daily Stock Analytics (AC-10)</h1>
      <p className="subtitle">Scoped strictly to requesting customer portfolio holdings.</p>

      {analytics && (
        <>
          <div className="dashboard-grid" style={{ marginBottom: "2rem" }}>
            <div className="card">
              <h3>🏆 Top 5 Gainers (AC-10)</h3>
              {analytics.top_gainers.length === 0 ? (
                <div className="empty-state">No holdings available to rank gainers.</div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Symbol</th>
                      <th>Avg Buy Price</th>
                      <th>Current Price</th>
                      <th>Gain %</th>
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
              <h3>📉 Top 5 Losers (AC-10)</h3>
              {analytics.top_losers.length === 0 ? (
                <div className="empty-state">No holdings available to rank losers.</div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Symbol</th>
                      <th>Avg Buy Price</th>
                      <th>Current Price</th>
                      <th>Loss %</th>
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

          <div className="card">
            <h3>📊 Sector Exposure Breakdown</h3>
            {analytics.sector_exposure.length === 0 ? (
              <div className="empty-state">No sector exposure data available.</div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Sector</th>
                    <th>Value ($)</th>
                    <th>Allocation (%)</th>
                  </tr>
                </thead>
                <tbody>
                  {analytics.sector_exposure.map((s: any) => (
                    <tr key={s.sector}>
                      <td><strong>{s.sector}</strong></td>
                      <td>${s.value}</td>
                      <td>{s.percentage}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  );
};
