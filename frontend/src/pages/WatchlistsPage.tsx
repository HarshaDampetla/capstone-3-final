import React, { useEffect, useState } from "react";
import { getWatchlists, createWatchlist, deleteWatchlist } from "../services/api";

export const WatchlistsPage: React.FC = () => {
  const [watchlists, setWatchlists] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [symbolsInput, setSymbolsInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadWatchlists = async () => {
    setLoading(true);
    try {
      const data = await getWatchlists();
      setWatchlists(data);
    } catch (err: any) {
      setError(err.message || "Failed to load watchlists");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWatchlists();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    const symbols = symbolsInput.split(",").map((s) => s.trim().toUpperCase()).filter(Boolean);
    try {
      await createWatchlist({ name, symbols });
      setSuccess("Watchlist created successfully (AC-04)!");
      setName("");
      setSymbolsInput("");
      loadWatchlists();
    } catch (err: any) {
      setError(err.message || "Failed to create watchlist");
    }
  };

  const handleDelete = async (id: number) => {
    setError("");
    setSuccess("");
    try {
      await deleteWatchlist(id);
      setSuccess("Watchlist deleted atomically (AC-05)!");
      loadWatchlists();
    } catch (err: any) {
      setError(err.message || "Failed to delete watchlist");
    }
  };

  return (
    <div className="page-container">
      <h1>Watchlists Management (AC-04, AC-05)</h1>
      <p className="subtitle">Maximum 10 watchlists per customer. Operations are atomic.</p>

      {error && <div className="error-banner">{error}</div>}
      {success && <div className="success-banner">{success}</div>}

      <div className="card" style={{ marginBottom: "2rem" }}>
        <h3>Create New Watchlist</h3>
        <form onSubmit={handleCreate} className="inline-form">
          <input
            type="text"
            required
            placeholder="Watchlist Name (e.g. Tech Leaders)"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="text"
            required
            placeholder="Comma-separated Symbols (e.g. AAPL, MSFT, GOOGL)"
            value={symbolsInput}
            onChange={(e) => setSymbolsInput(e.target.value)}
          />
          <button type="submit" className="btn-primary">
            Create Watchlist
          </button>
        </form>
      </div>

      {loading ? (
        <div className="loading-spinner">Loading watchlists...</div>
      ) : watchlists.length === 0 ? (
        <div className="empty-state">No watchlists found. Create your first watchlist above!</div>
      ) : (
        <div className="watchlists-grid">
          {watchlists.map((w) => (
            <div key={w.id} className="watchlist-card">
              <div className="watchlist-header">
                <h3>{w.name}</h3>
                <button className="btn-danger-sm" onClick={() => handleDelete(w.id)}>
                  Delete
                </button>
              </div>
              <div className="symbols-tags">
                {w.symbols.map((sym: string) => (
                  <span key={sym} className="symbol-tag">
                    {sym}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
