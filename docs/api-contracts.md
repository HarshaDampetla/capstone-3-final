# MarketScope — API Contracts Specification

**Base URL:** `/api/v1`  
**Authentication:** Bearer Token (`Authorization: Bearer <JWT_TOKEN>`)  
**Data Format:** `application/json`  

---

## 1. Authentication Endpoints

### `POST /api/v1/auth/register` (AC-01)
- **Description:** Self-service customer registration.
- **Request Body:**
  ```json
  {
    "email": "customer@example.com",
    "password": "Password123!"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "email": "customer@example.com",
    "role": "CUSTOMER",
    "state": "ACTIVE",
    "available_cash": "10000.0000",
    "created_at": "2026-10-06T00:00:00Z"
  }
  ```

### `POST /api/v1/auth/login` (AC-01)
- **Description:** OAuth2 password flow login returning JWT token.
- **Request Body (form-data):** `username=customer@example.com&password=Password123!`
- **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

### `GET /api/v1/auth/me`
- **Description:** Returns profile details for current authenticated user.
- **Response (200 OK):** UserResponse object.

---

## 2. Stock Catalog Endpoints (AC-03)

### `GET /api/v1/catalog`
- **Query Params:** `symbol`, `sector`, `exchange` (optional filters).
- **Response (200 OK):** `Array<StockResponse>` (excludeds `DELETED` stocks).

### `POST /api/v1/admin/catalog` (AC-03, Admin Only)
- **Request Body:**
  ```json
  {
    "symbol": "NVDA",
    "company_name": "NVIDIA Corp",
    "sector": "Technology",
    "exchange": "NASDAQ",
    "current_price": "120.0000"
  }
  ```
- **Response (201 Created):** StockResponse object.

### `DELETE /api/v1/admin/catalog/{symbol}` (AC-03, Admin Only)
- **Description:** Soft-deletes stock catalog item, updating status to `DELETED`.
- **Response (200 OK):** StockResponse with `status: "DELETED"`.

---

## 3. Watchlist Endpoints (AC-04, AC-05)

### `GET /api/v1/watchlists`
- **Response (200 OK):** List of watchlists owned by authenticated customer.

### `POST /api/v1/watchlists` (AC-04, AC-05)
- **Request Body:**
  ```json
  {
    "name": "Tech Leaders",
    "symbols": ["AAPL", "MSFT", "GOOGL"]
  }
  ```
- **Response (201 Created):** WatchlistResponse object.

### `DELETE /api/v1/watchlists/{id}` (AC-05)
- **Description:** Atomic deletion of customer watchlist and associated symbols.
- **Response (204 No Content) / (200 OK).**

---

## 4. Trade Order Endpoints (AC-06, AC-07, AC-08)

### `POST /api/v1/orders` (AC-06, AC-08)
- **Request Body:**
  ```json
  {
    "symbol": "AAPL",
    "side": "BUY",
    "order_type": "LIMIT",
    "quantity": "2.0000",
    "quote_price": "150.0000"
  }
  ```
- **Response (201 Created):** OrderResponse object (`status: "PENDING"`).
- **Errors:** `400 Bad Request` ("Insufficient funds", "Quantity and quote price must be strictly positive").

### `GET /api/v1/orders`
- **Response (200 OK):** List of trade orders for current user.

### `DELETE /api/v1/orders/{id}` (AC-07)
- **Description:** Cancels a pending order (`PENDING` -> `CANCELLED`).
- **Response (200 OK):** OrderResponse (`status: "CANCELLED"`).
- **Errors:** `400 Bad Request` ("Executed orders are immutable").

### `POST /api/v1/orders/{id}/execute` (AC-07)
- **Description:** Executes pending order, atomically updating cash and portfolio holdings.
- **Response (200 OK):** OrderResponse (`status: "EXECUTED"`).

---

## 5. Portfolio & Analytics Endpoints (AC-09, AC-10)

### `GET /api/v1/portfolio/stats` (AC-09)
- **Response (200 OK):**
  ```json
  {
    "customer_id": 1,
    "total_invested": "3000.00",
    "current_value": "3200.00",
    "absolute_pnl": "200.00",
    "percent_pnl": "6.67"
  }
  ```

### `GET /api/v1/analytics/daily` (AC-10)
- **Response (200 OK):**
  ```json
  {
    "top_gainers": [...],
    "top_losers": [...],
    "sector_exposure": [...],
    "portfolio_stats": {...}
  }
  ```

### `GET /api/v1/analytics/platform`
- **Response (200 OK):** Platform order stats, volume by status, most traded symbols, settlement queue.

### `POST /api/v1/market/tick`
- **Response (200 OK):** Synthetic random-walk price tick execution output.

---

## 6. Admin User Management Endpoints (AC-02)

### `GET /api/v1/admin/users`
- **Response (200 OK):** List of all users in system.

### `PUT /api/v1/admin/users/{id}/role` (AC-02)
- **Request Body:** `{"target_role": "ADMIN"}`
- **Response (200 OK):** UserResponse with updated role.

### `POST /api/v1/admin/users/{id}/suspend` (AC-02)
- **Response (200 OK):** UserResponse with `state: "SUSPENDED"`.

### `POST /api/v1/admin/users/{id}/reactivate` (AC-02)
- **Response (200 OK):** UserResponse with `state: "ACTIVE"`.
