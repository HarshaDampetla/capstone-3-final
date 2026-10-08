# MarketScope — Technical Debugging Postmortem Report

**Business Case ID:** BC-AINE-006  
**Document Type:** Engineering Incident & Debugging Postmortem  

---

## 1. Postmortem 1: Passlib / Bcrypt 4.x Compatibility Failure

### Summary
During early authentication testing (`tests/unit/test_auth.py`), `passlib.context.CryptContext` failed with `AttributeError: module 'bcrypt' has no attribute '__about__'`.

### Root Cause
Passlib version 1.7.4 relies on obsolete internal module attribute checking (`bcrypt.__about__`) which was deprecated and removed in `bcrypt 4.0.0+`.

### Resolution & Prevention
- **Fix:** Bypassed passlib and implemented direct native `bcrypt` module functions (`bcrypt.hashpw` and `bcrypt.checkpw`) in `src/core/security.py`.
- **Safety Slicing:** Added input password byte slicing (`password.encode("utf-8")[:72]`) to protect against bcrypt 72-byte truncation traps.
- **Prevention Asset:** Created `test_ac_01_customer_registration` unit test validating direct bcrypt hashing.

---

## 2. Postmortem 2: Pydantic v2 ORM Relationship List Serialization

### Summary
When returning `WatchlistResponse` objects containing SQLAlchemy `WatchlistModel.symbols` relationship lists, Pydantic v2 raised validation errors attempting to serialize `WatchlistSymbolModel` ORM objects as plain string lists (`List[str]`).

### Root Cause
Pydantic v2 `from_attributes=True` maps relationship fields as list of ORM model objects rather than extracting the `symbol` string attribute.

### Resolution & Prevention
- **Fix:** Added a pre-validation validator to `WatchlistResponse` in `src/api/schemas.py`:
  ```python
  @field_validator("symbols", mode="before")
  @classmethod
  def serialize_symbols(cls, v):
      if isinstance(v, list):
          return [item.symbol if hasattr(item, "symbol") else item for item in v]
      return v
  ```
- **Prevention Asset:** Added integration test `test_ac_04_watchlist_api_creation_and_limit` verifying clean JSON string array output.

---

## 3. Postmortem 3: SQLite Numeric(18, 4) String Formatting in API Responses

### Summary
In integration API assertions (`test_ac_03_admin_stock_crud_api`), assertions checking `response.json()["current_price"] == "420.00"` failed because SQLite returned `"420.0000"`.

### Root Cause
SQLite's `Numeric(18, 4)` column type formats trailing scale zeros to 4 decimal places in text responses.

### Resolution & Prevention
- **Fix:** Updated test assertions to compare exact numeric equality using `Decimal(response.json()["key"]) == Decimal("420.00")`.
- **Prevention Asset:** Added `test_financial_models_use_decimal_types` in `tests/architecture/test_layering.py`.
