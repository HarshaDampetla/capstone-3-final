# Stock Catalog Specification
**Feature:** Stock Catalog CRUD Administration & Soft Delete Lifecycle  
**AC References:** AC-03  

---

## 1. Purpose
Define specifications for stock catalog CRUD administration reserved for `ADMIN` role users, including symbol creation, lookup, price update, and soft-deletion (`DELETED` status).

---

## 2. Scope
- Admin stock creation and attribute configuration (symbol, company name, sector, exchange, price).
- Stock catalog searching and browsing by symbol, sector, or exchange.
- Admin soft-deletion of symbols. Hard-deleting symbols is strictly prohibited.

---

## 3. Actors
- **Admin:** Authenticated user with `ADMIN` role (can perform CRUD and soft-delete).
- **Customer:** Authenticated user with `CUSTOMER` role (can browse active catalog).

---

## 4. User Journeys
1. **Stock Creation (Admin):** Admin posts symbol payload → System validates `ADMIN` role → Creates stock entry with `status = ACTIVE` → Returns stock DTO.
2. **Stock Search (Customer/Admin):** User requests stock catalog → System filters for active stocks (`status = ACTIVE`) → Returns catalog list.
3. **Soft-Delete (Admin):** Admin submits delete request for symbol "AAPL" → System sets `status = DELETED` → Returns updated stock record. Symbol remains in database for order history integrity.

---

## 5. Business Rules
- **Rule SC-01:** Stock CRUD operations MUST be restricted to `ADMIN` role users only (AC-03).
- **Rule SC-02:** Stock symbols MUST be uppercase strings (e.g. "AAPL", "MSFT").
- **Rule SC-03:** Stock prices MUST be strictly positive Python `Decimal` values (NFR-01).
- **Rule SC-04 (Soft-Delete):** Deleting a stock symbol MUST transition its status to `DELETED` / `DELISTED`. Symbols MUST NEVER be hard-deleted from the database table (AC-03).

---

## 6. Domain Model
```python
class StockStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DELISTED = "DELISTED"
```

---

## 7. API Requirements
- `POST /api/v1/admin/catalog` — Create new stock symbol (ADMIN only).
- `GET /api/v1/catalog` — Search/List active stock symbols.
- `GET /api/v1/catalog/{symbol}` — Get stock details by symbol.
- `DELETE /api/v1/admin/catalog/{symbol}` — Soft-delete stock symbol (ADMIN only).

---

## 8. Error Handling
- Customer attempting catalog CRUD -> `403 Forbidden` (`PermissionDeniedException`).
- Creating duplicate stock symbol -> `400 Bad Request`.
- Non-positive stock price -> `422 Unprocessable Entity`.
- Soft-deleting non-existent symbol -> `404 Not Found`.

---

## 9. Security Requirements
- All POST/PUT/DELETE endpoints in catalog module MUST require `ADMIN` role in JWT token claims.

---

## 10. Acceptance Criteria

### AC-03: Stock Catalog Management & Soft-Delete
```gherkin
Given an authenticated user with "ADMIN" role
When the admin posts a new stock symbol "NVDA" with company_name = "NVIDIA Corp" and price = Decimal("850.00")
Then the stock is added to the catalog with status = "ACTIVE"
When the admin submits a soft-delete request for symbol "NVDA"
Then the stock's status transitions to "DELETED"
And the stock record remains present in the database table
And searching the public catalog excludes symbols in "DELETED" status
```

---

## 11. Negative Test Cases
- **NT-SC-01:** Customer attempts to create stock symbol "TSLA" -> Expect HTTP 403.
- **NT-SC-02:** Admin attempts hard-delete via SQL -> System soft-deletes symbol to `DELETED` status instead.

---

## 12. Non-Functional Requirements
- **NFR-01:** Prices represented using `Decimal` / `Numeric(18, 4)`.

---

## 13. Dependencies
- Depends on `src/repositories/catalog_repository.py`.
