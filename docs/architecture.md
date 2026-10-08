# MarketScope — System Architecture & Layered Design

**Business Case:** BC-AINE-006  
**System:** Stock Trading & Portfolio Analytics Platform  
**Stack:** FastAPI, SQLAlchemy, Pydantic, SQLite, React, TypeScript, Vite  

---

## 1. System Context Diagram

```mermaid
flowchart TD
    CUSTOMER["👤 Customer (Trader)"] -->|HTTPS / JSON REST| FE["🖥️ React TypeScript Frontend (Port 5173)"]
    ADMIN["👨‍💼 Administrator"] -->|HTTPS / JSON REST| FE
    
    FE -->|JWT Bearer Auth| API["🚀 FastAPI Backend API (Port 8000)"]
    
    subgraph Backend Core
        API --> SVC["⚙️ Service Layer"]
        SVC --> DOMAIN["🧠 Domain Layer & PnL Calculator"]
        SVC --> REPO["🗄️ Repository Persistence Layer"]
    end
    
    REPO -->|SQLAlchemy ORM| DB[("💾 SQLite Database marketscope.db")]

    style FE fill:#eff6ff,stroke:#2563eb,stroke-width:2px
    style API fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style DOMAIN fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style DB fill:#f1f5f9,stroke:#64748b,stroke-width:2px
```

---

## 2. Layered Architecture Diagram

```mermaid
flowchart TD
    subgraph Controllers Layer ["API / Controllers (src/api)"]
        AUTH_R["Auth Router (/api/v1/auth)"]
        CAT_R["Catalog Router (/api/v1/catalog)"]
        ORD_R["Order Router (/api/v1/orders)"]
        PF_R["Portfolio Router (/api/v1/portfolio)"]
        AN_R["Analytics Router (/api/v1/analytics)"]
    end

    subgraph Service Layer ["Service Layer (src/services)"]
        AUTH_S["AuthService"]
        CAT_S["CatalogService"]
        ORD_S["OrderService"]
        PF_S["PortfolioService"]
        AN_S["AnalyticsService"]
    end

    subgraph Domain Layer ["Domain Core (src/domain) - Zero External Imports"]
        USER_RULES["User & Role Policy"]
        ORDER_RULES["OrderPolicy & Rules"]
        FUNDS_VAL["FundsValidator"]
        PNL_CALC["PnLCalculator"]
    end

    subgraph Repository Layer ["Repositories (src/repositories)"]
        USER_R["UserRepository"]
        CAT_R_REPO["CatalogRepository"]
        ORD_R_REPO["OrderRepository"]
        PF_R_REPO["PortfolioRepository"]
    end

    subgraph Database Layer ["Database (src/db)"]
        MODELS["SQLAlchemy Models (UserModel, OrderModel, StockCatalogModel, etc.)"]
    end

    AUTH_R --> AUTH_S
    CAT_R --> CAT_S
    ORD_R --> ORD_S
    PF_R --> PF_S
    AN_R --> AN_S

    AUTH_S --> USER_RULES
    ORD_S --> ORDER_RULES
    ORD_S --> FUNDS_VAL
    PF_S --> PNL_CALC
    AN_S --> PNL_CALC

    AUTH_S --> USER_R
    CAT_S --> CAT_R_REPO
    ORD_S --> ORD_R_REPO
    PF_S --> PF_R_REPO

    USER_R --> MODELS
    CAT_R_REPO --> MODELS
    ORD_R_REPO --> MODELS
    PF_R_REPO --> MODELS
```

---

## 3. Order Placement Sequence Diagram (AC-06, AC-07, AC-08)

```mermaid
sequenceDiagram
    autonumber
    actor Customer as 👤 Customer
    participant Router as 🚦 OrderRouter
    participant Service as ⚙️ OrderService
    participant FundsVal as 💵 FundsValidator (Domain)
    participant Repo as 🗄️ OrderRepository
    participant DB as 💾 SQLite DB

    Customer->>Router: POST /api/v1/orders {symbol, side="BUY", type="LIMIT", quantity=2, quote_price=150}
    Router->>Service: place_order(user_id, symbol, side, type, quantity, quote_price)
    
    Service->>Service: Retrieve user profile & available_cash
    
    rect rgb(254, 243, 199)
        note over Service, FundsVal: Domain Financial Validation (AC-08, NFR-01)
        Service->>FundsVal: validate_buy_order_cash(quote_price, quantity, available_cash)
        alt Required Cash (300.00) > Available Cash (100.00)
            FundsVal-->>Service: Raise InsufficientFundsException
            Service-->>Router: HTTP 400 Bad Request ("Insufficient funds")
            Router-->>Customer: Return Error Response (400)
        else Cash Sufficient
            FundsVal-->>Service: Return total_cost (Decimal("300.00"))
        end
    end

    Service->>Repo: create_order(user_id, symbol, side, type, quantity, quote_price, status="PENDING")
    Repo->>DB: INSERT INTO orders (created_at=UTC timestamp, status='PENDING')
    DB-->>Repo: Order record created (ID #42)
    Repo-->>Service: OrderModel instance
    Service-->>Router: Order DTO
    Router-->>Customer: Return HTTP 201 Created {id: 42, status: "PENDING", created_at: "..."}
```

---

## 4. Architectural Discipline Summary
- **Layer Isolation:** Controllers access Services; Services access Domain & Repositories; Repositories access Database ORM models.
- **Domain Independence:** `src/domain/` contains pure Python models, calculators, and validators with zero dependencies on external frameworks or database layers.
- **Fixed-Point Financial Policy:** Python `Decimal` is enforced across all domain calculations and entity models (`NFR-01`).
