// API Service client communicating with FastAPI backend
const API_BASE = "http://localhost:8000/api/v1";

export function getToken(): string | null {
  return localStorage.getItem("marketscope_token");
}

export function setToken(token: string) {
  localStorage.setItem("marketscope_token", token);
}

export function clearToken() {
  localStorage.removeItem("marketscope_token");
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    let errorDetail = "API request failed";
    try {
      const errorJson = await res.json();
      errorDetail = errorJson.detail || JSON.stringify(errorJson);
    } catch {
      errorDetail = await res.text();
    }
    throw new Error(errorDetail);
  }

  return res.json();
}

// Auth API
export async function registerUser(payload: any) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function loginUser(payload: any) {
  const formData = new URLSearchParams();
  formData.append("username", payload.email);
  formData.append("password", payload.password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });

  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(errorJson.detail || "Login failed");
  }

  return res.json();
}

export async function getProfile() {
  return request("/auth/me");
}

// Stock Catalog API
export async function searchStocks(params?: { symbol?: string; sector?: string; exchange?: string }) {
  const query = new URLSearchParams(params as any).toString();
  return request(`/catalog?${query}`);
}

export async function createAdminStock(payload: any) {
  return request("/admin/catalog", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateAdminStock(symbol: string, payload: any) {
  return request(`/admin/catalog/${symbol}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export async function deleteAdminStock(symbol: string) {
  return request(`/admin/catalog/${symbol}`, {
    method: "DELETE",
  });
}

// Watchlist API
export async function getWatchlists() {
  return request<any[]>("/watchlists");
}

export async function createWatchlist(payload: { name: string; symbols: string[] }) {
  return request("/watchlists", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateWatchlist(id: number, payload: { name?: string; symbols?: string[] }) {
  return request(`/watchlists/${id}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export async function deleteWatchlist(id: number) {
  return request(`/watchlists/${id}`, {
    method: "DELETE",
  });
}

// Orders API
export async function getOrders() {
  return request<any[]>("/orders");
}

export async function placeOrder(payload: {
  symbol: string;
  side: "BUY" | "SELL";
  order_type: "MARKET" | "LIMIT";
  quantity: string;
  quote_price: string;
}) {
  return request("/orders", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function cancelOrder(orderId: number) {
  return request(`/orders/${orderId}`, {
    method: "DELETE",
  });
}

export async function executeOrder(orderId: number) {
  return request(`/orders/${orderId}/execute`, {
    method: "POST",
  });
}

// Portfolio API
export async function getPortfolioStats() {
  return request<any>("/portfolio/stats");
}

// Analytics API
export async function getDailyAnalytics() {
  return request<any>("/analytics/daily");
}

export async function getPlatformAnalytics() {
  return request<any>("/analytics/platform");
}

export async function triggerMarketTick() {
  return request<any>("/market/tick", {
    method: "POST",
  });
}

// Admin Users API
export async function listAdminUsers() {
  return request<any[]>("/admin/users");
}

export async function updateAdminUserRole(userId: number, role: string) {
  return request(`/admin/users/${userId}/role`, {
    method: "PUT",
    body: JSON.stringify({ target_role: role }),
  });
}

export async function suspendAdminUser(userId: number) {
  return request(`/admin/users/${userId}/suspend`, {
    method: "POST",
  });
}

export async function reactivateAdminUser(userId: number) {
  return request(`/admin/users/${userId}/reactivate`, {
    method: "POST",
  });
}
