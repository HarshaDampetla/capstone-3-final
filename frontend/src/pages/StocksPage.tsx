import React, { useEffect, useState } from "react";
import { searchStocks, placeOrder } from "../services/api";

export const StocksPage: React.FC = () => {
  const [stocks, setStocks] = useState<any[]>([]);
  const [symbol, setSymbol] = useState("");
  const [sector, setSector] = useState("");
  const [exchange, setExchange] = useState("");
  const [loading, setLoading] = useState(false);

  // Order Placement Modal state
  const [selectedStock, setSelectedStock] = useState<any | null>(null);
  const [orderSide, setOrderSide] = useState<"BUY" | "SELL">("BUY");
  const [orderType, setOrderType] = useState<"MARKET" | "LIMIT">("LIMIT");
  const [quantity, setQuantity] = useState("1.0000");
  const [quotePrice, setQuotePrice] = useState("");
  const [orderMsg, setOrderMsg] = useState("");
  const [orderError, setOrderError] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (symbol) params.symbol = symbol;
      if (sector) params.sector = sector;
      if (exchange) params.exchange = exchange;

      const data = await searchStocks(params);
      setStocks(data as any[]);
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch();
  }, []);

  const openTradeModal = (stock: any) => {
    setSelectedStock(stock);
    setQuotePrice(stock.current_price);
    setOrderMsg("");
    setOrderError("");
  };

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    setOrderMsg("");
    setOrderError("");
    try {
      await placeOrder({
        symbol: selectedStock.symbol,
        side: orderSide,
        order_type: orderType,
        quantity,
        quote_price: quotePrice,
      });
      setOrderMsg(`Order placed successfully for ${selectedStock.symbol} in PENDING state!`);
      setTimeout(() => setSelectedStock(null), 1500);
    } catch (err: any) {
      setOrderError(err.message || "Failed to place order");
    }
  };

  return (
    <div className="page-container">
      <h1>Stock Catalog & Browse (AC-03)</h1>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Filter by Symbol..."
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <input
          type="text"
          placeholder="Filter by Sector..."
          value={sector}
          onChange={(e) => setSector(e.target.value)}
        />
        <input
          type="text"
          placeholder="Filter by Exchange..."
          value={exchange}
          onChange={(e) => setExchange(e.target.value)}
        />
        <button className="btn-primary" onClick={handleSearch}>
          Search Catalog
        </button>
      </div>

      {loading ? (
        <div className="loading-spinner">Searching stock catalog...</div>
      ) : stocks.length === 0 ? (
        <div className="empty-state">No active stocks found matching criteria.</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Company Name</th>
              <th>Sector</th>
              <th>Exchange</th>
              <th>Current Price</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((s) => (
              <tr key={s.symbol}>
                <td><strong>{s.symbol}</strong></td>
                <td>{s.company_name}</td>
                <td>{s.sector}</td>
                <td>{s.exchange}</td>
                <td>${s.current_price}</td>
                <td>
                  <button className="btn-secondary" onClick={() => openTradeModal(s)}>
                    Trade Order
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {selectedStock && (
        <div className="modal-backdrop">
          <div className="modal-card">
            <h3>Place Trade Order — {selectedStock.symbol}</h3>
            {orderMsg && <div className="success-banner">{orderMsg}</div>}
            {orderError && <div className="error-banner">{orderError}</div>}

            <form onSubmit={handlePlaceOrder}>
              <div className="form-group">
                <label>Side</label>
                <select value={orderSide} onChange={(e: any) => setOrderSide(e.target.value)}>
                  <option value="BUY">BUY</option>
                  <option value="SELL">SELL</option>
                </select>
              </div>

              <div className="form-group">
                <label>Order Type</label>
                <select value={orderType} onChange={(e: any) => setOrderType(e.target.value)}>
                  <option value="LIMIT">LIMIT</option>
                  <option value="MARKET">MARKET</option>
                </select>
              </div>

              <div className="form-group">
                <label>Quantity</label>
                <input
                  type="text"
                  required
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label>Quote Price ($)</label>
                <input
                  type="text"
                  required
                  value={quotePrice}
                  onChange={(e) => setQuotePrice(e.target.value)}
                />
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn-primary">
                  Submit Order (AC-06)
                </button>
                <button type="button" className="btn-secondary" onClick={() => setSelectedStock(null)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
