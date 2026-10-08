# MarketScope — Playwright End-to-End (E2E) UI Validation Report

**Business Case ID:** BC-AINE-006  
**UI Framework:** React + TypeScript + Vite  
**Testing Framework:** Playwright Test Suite (`@playwright/test`)  
**MCP Server Integration:** Configured in `.mcp.json` (`@playwright/mcp-server`)  

---

## 1. Overview
The Playwright E2E UI validation suite executes automated browser interactions against the live MarketScope React application, validating customer journeys, admin management workflows, role-based route protection, and visual layout responsiveness.

---

## 2. Test Execution Summary

| Test # | Workflow Scenario | AC Reference | Expected Behavior | Status |
|---|---|---|---|---|
| **1** | Customer Registration | **AC-01** | Account created in `ACTIVE` state with `CUSTOMER` role, redirected to `/dashboard`. | **PASSED** |
| **2** | Login & JWT Authentication | **AC-01** | Token stored in `localStorage`, user email badge displayed in Navbar. | **PASSED** |
| **3** | Stock Catalog Browsing & Search | **AC-03** | Multi-attribute search by symbol, sector, and exchange filters active stocks. | **PASSED** |
| **4** | Watchlist Creation & Atomicity | **AC-04**, **AC-05** | Watchlist created with name and symbol tags, max 10 limit enforced. | **PASSED** |
| **5** | Trade Order Placement | **AC-06** | Market/Limit order submitted, created in `PENDING` status with server timestamp. | **PASSED** |
| **6** | Portfolio Holdings Valuation | **AC-09** | Displays total invested, current market value, absolute & percentage P&L. | **PASSED** |
| **7** | Daily Analytics & Top Gainers/Losers | **AC-10** | Displays top 5 gainers and top 5 losers ranked by percentage P&L. | **PASSED** |
| **8** | Admin User Management | **AC-02** | Role switching (CUSTOMER/ADMIN) and account state toggling (ACTIVE/SUSPENDED). | **PASSED** |
| **9** | Admin Stock Catalog Management | **AC-03** | Stock creation and soft-deletion with `DELETED` status badge. | **PASSED** |
| **10** | Unauthorized Route Protection | Security / NFR-04 | CUSTOMER attempting to navigate to `/admin/users` redirected to `/dashboard`. | **PASSED** |

---

## 3. Playwright MCP Configuration (`.mcp.json`)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp-server"
      ]
    }
  }
}
```

---

## 4. Snapshots & Artifact Storage
- Test scripts: `playwright/tests/marketscope.spec.ts`
- Screen snapshots & visual artifacts: `playwright/snapshots/`
- Playwright configuration: `playwright.config.ts`
