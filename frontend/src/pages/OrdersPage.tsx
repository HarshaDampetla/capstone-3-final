import React, { useEffect, useState } from "react";
import { getOrders, cancelOrder, executeOrder } from "../services/api";

export const OrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadOrders = async () => {
    setLoading(true);
    try {
      const data = await getOrders();
      setOrders(data);
    } catch (err: any) {
      setError(err.message || "Failed to load trade orders");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

  const handleCancel = async (orderId: number) => {
    setError("");
    setSuccess("");
    try {
      await cancelOrder(orderId);
      setSuccess("Order cancelled successfully (AC-07)!");
      loadOrders();
    } catch (err: any) {
      setError(err.message || "Failed to cancel order");
    }
  };

  const handleExecute = async (orderId: number) => {
    setError("");
    setSuccess("");
    try {
      await executeOrder(orderId);
      setSuccess("Order executed successfully (AC-07)!");
      loadOrders();
    } catch (err: any) {
      setError(err.message || "Execution failed");
    }
  };

  return (
    <div className="page-container">
      <h1>Trade Orders History & Execution (AC-06, AC-07, AC-08)</h1>

      {error && <div className="error-banner">{error}</div>}
      {success && <div className="success-banner">{success}</div>}

      {loading ? (
        <div className="loading-spinner">Loading trade orders...</div>
      ) : orders.length === 0 ? (
        <div className="empty-state">No trade orders placed yet.</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Symbol</th>
              <th>Side</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Quote Price</th>
              <th>Status</th>
              <th>Placed At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id}>
                <td>#{o.id}</td>
                <td><strong>{o.symbol}</strong></td>
                <td>
                  <span className={`badge ${o.side === "BUY" ? "badge-buy" : "badge-sell"}`}>
                    {o.side}
                  </span>
                </td>
                <td>{o.order_type}</td>
                <td>{o.quantity}</td>
                <td>${o.quote_price}</td>
                <td>
                  <span className={`status-badge status-${o.status.toLowerCase()}`}>
                    {o.status}
                  </span>
                </td>
                <td>{new Date(o.created_at).toLocaleString()}</td>
                <td>
                  {o.status === "PENDING" ? (
                    <>
                      <button className="btn-success-sm" onClick={() => handleExecute(o.id)}>
                        Execute
                      </button>
                      <button className="btn-danger-sm" onClick={() => handleCancel(o.id)}>
                        Cancel
                      </button>
                    </>
                  ) : (
                    <span className="immutable-label">Immutable (NFR-02)</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
