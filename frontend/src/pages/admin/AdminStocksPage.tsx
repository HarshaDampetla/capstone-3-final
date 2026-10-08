import React, { useEffect, useState } from "react";
import { searchStocks, createAdminStock, deleteAdminStock } from "../../services/api";

export const AdminStocksPage: React.FC = () => {
  const [stocks, setStocks] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Create Form State
  const [symbol, setSymbol] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [sector, setSector] = useState("");
  const [exchange, setExchange] = useState("NASDAQ");
  const [price, setPrice] = useState("100.00");

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const data = await searchStocks();
      setStocks(data as any[]);
    } catch (err: any) {
      setError(err.message || "Failed to load catalog");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCatalog();
  }, []);

  const handleCreateStock = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      await createAdminStock({
        symbol: symbol.toUpperCase(),
        company_name: companyName,
        sector,
        exchange,
        current_price: price,
      });
      setSuccess(`Stock ${symbol.toUpperCase()} created successfully (AC-03)!`);
      setSymbol("");
      setCompanyName("");
      setSector("");
      setPrice("100.00");
      loadCatalog();
    } catch (err: any) {
      setError(err.message || "Failed to create stock");
    }
  };

  const handleSoftDelete = async (sym: string) => {
    setError("");
    setSuccess("");
    try {
      await deleteAdminStock(sym);
      setSuccess(`Stock ${sym} soft-deleted with DELETED status (AC-03)!`);
      loadCatalog();
    } catch (err: any) {
      setError(err.message || "Failed to soft-delete stock");
    }
  };

  return (
    <div className="page-container">
      <h1>Admin Stock Catalog Management (AC-03)</h1>
      <p className="subtitle">Stock CRUD operations with mandatory soft delete (`DELETED` status).</p>

      {error && <div className="error-banner">{error}</div>}
      {success && <div className="success-banner">{success}</div>}

      <div className="card" style={{ marginBottom: "2rem" }}>
        <h3>Add New Stock to Catalog</h3>
        <form onSubmit={handleCreateStock} className="grid-form">
          <input type="text" required placeholder="Symbol (e.g. NVDA)" value={symbol} onChange={(e) => setSymbol(e.target.value)} />
          <input type="text" required placeholder="Company Name (e.g. Nvidia)" value={companyName} onChange={(e) => setCompanyName(e.target.value)} />
          <input type="text" required placeholder="Sector (e.g. Semiconductors)" value={sector} onChange={(e) => setSector(e.target.value)} />
          <select value={exchange} onChange={(e) => setExchange(e.target.value)}>
            <option value="NASDAQ">NASDAQ</option>
            <option value="NYSE">NYSE</option>
            <option value="AMEX">AMEX</option>
          </select>
          <input type="text" required placeholder="Initial Price ($)" value={price} onChange={(e) => setPrice(e.target.value)} />
          <button type="submit" className="btn-primary">Create Stock</button>
        </form>
      </div>

      {loading ? (
        <div className="loading-spinner">Loading stock catalog...</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Company Name</th>
              <th>Sector</th>
              <th>Exchange</th>
              <th>Current Price</th>
              <th>Status</th>
              <th>Actions</th>
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
                  <span className={`status-badge status-${s.status.toLowerCase()}`}>{s.status}</span>
                </td>
                <td>
                  {s.status !== "DELETED" && (
                    <button className="btn-danger-sm" onClick={() => handleSoftDelete(s.symbol)}>
                      Soft Delete (AC-03)
                    </button>
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
