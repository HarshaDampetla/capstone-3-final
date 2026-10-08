import React, { useEffect, useState } from "react";
import { getOrders, executeOrder } from "../../services/api";

export const AdminOrdersPage: React.FC = () => {
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
      setError(err.message || "Failed to load platform orders");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

  const handleExecute = async (orderId: number) => {
    setError("");
    setSuccess("");
    try {
      await executeOrder(orderId);
      setSuccess(`Order #${orderId} executed by administrator!`);
      loadOrders();
    } catch (err: any) {
      setError(err.message || "Execution failed");
    }
  };

  return (
    <div className="page-container">
      <h1>Admin Trade Orders Management</h1>
      <p className="subtitle">Audit and process system trade order execution queues.</p>

      {error && <div className="error-banner">{error}</div>}
      {success && <div className="success-banner">{success}</div>}

      {loading ? (
        <div className="loading-spinner">Loading platform trade orders...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer ID</th>
              <th>Symbol</th>
              <th>Side</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Quote Price</th>
              <th>Status</th>
              <th>Placed At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id}>
                <td>#{o.id}</td>
                <td>User #{o.user_id}</td>
                <td><strong>{o.symbol}</strong></td>
                <td>
                  <span className={`badge ${o.side === "BUY" ? "badge-buy" : "badge-sell"}`}>{o.side}</span>
                </td>
                <td>{o.order_type}</td>
                <td>{o.quantity}</td>
                <td>${o.quote_price}</td>
                <td>
                  <span className={`status-badge status-${o.status.toLowerCase()}`}>{o.status}</span>
                </td>
                <td>{new Date(o.created_at).toLocaleString()}</td>
                <td>
                  {o.status === "PENDING" ? (
                    <button className="btn-success-sm" onClick={() => handleExecute(o.id)}>
                      Execute Order
                    </button>
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
