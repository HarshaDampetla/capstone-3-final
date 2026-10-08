# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: marketscope.spec.ts >> MarketScope E2E Web UI Test Suite >> 3. Stock browsing & multi-attribute catalog search (AC-03)
- Location: playwright\tests\marketscope.spec.ts:27:7

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('h1')
Expected substring: "Stock Catalog"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toContainText" locator('h1') with timeout 5000ms
  - waiting for locator('h1')

```

```yaml
- navigation:
  - link "🚀 MarketScope":
    - /url: /dashboard
  - link "Login":
    - /url: /login
  - link "Register":
    - /url: /register
- main:
  - heading "Sign In to MarketScope" [level=2]
  - text: Email Address
  - textbox "customer@example.com"
  - text: Password
  - textbox "••••••••"
  - button "Sign In"
  - paragraph:
    - text: Don't have an account?
    - link "Register here":
      - /url: /register
```

# Test source

```ts
  1   | import { test, expect } from "@playwright/test";
  2   | 
  3   | test.describe("MarketScope E2E Web UI Test Suite", () => {
  4   |   const customerEmail = `e2e_cust_${Date.now()}@marketscope.com`;
  5   |   const customerPassword = "Password123!";
  6   | 
  7   |   test("1. Customer registration & redirect to dashboard (AC-01)", async ({ page }) => {
  8   |     await page.goto("http://localhost:5173/register");
  9   |     await page.fill('input[type="email"]', customerEmail);
  10  |     await page.fill('input[type="password"]', customerPassword);
  11  |     await page.click('button[type="submit"]');
  12  | 
  13  |     await expect(page).toHaveURL(/.*dashboard/);
  14  |     await expect(page.locator("h1")).toContainText("Welcome");
  15  |   });
  16  | 
  17  |   test("2. User login & token authentication", async ({ page }) => {
  18  |     await page.goto("http://localhost:5173/login");
  19  |     await page.fill('input[type="email"]', customerEmail);
  20  |     await page.fill('input[type="password"]', customerPassword);
  21  |     await page.click('button[type="submit"]');
  22  | 
  23  |     await expect(page).toHaveURL(/.*dashboard/);
  24  |     await expect(page.locator(".user-email")).toContainText(customerEmail);
  25  |   });
  26  | 
  27  |   test("3. Stock browsing & multi-attribute catalog search (AC-03)", async ({ page }) => {
  28  |     await page.goto("http://localhost:5173/login");
  29  |     await page.fill('input[type="email"]', customerEmail);
  30  |     await page.fill('input[type="password"]', customerPassword);
  31  |     await page.click('button[type="submit"]');
  32  | 
  33  |     await page.goto("http://localhost:5173/stocks");
> 34  |     await expect(page.locator("h1")).toContainText("Stock Catalog");
      |                                      ^ Error: expect(locator).toContainText(expected) failed
  35  |     await page.fill('input[placeholder="Filter by Symbol..."]', "AAPL");
  36  |     await page.click('button:has-text("Search Catalog")');
  37  |   });
  38  | 
  39  |   test("4. Watchlist creation & max 10 limit UI (AC-04, AC-05)", async ({ page }) => {
  40  |     await page.goto("http://localhost:5173/login");
  41  |     await page.fill('input[type="email"]', customerEmail);
  42  |     await page.fill('input[type="password"]', customerPassword);
  43  |     await page.click('button[type="submit"]');
  44  | 
  45  |     await page.goto("http://localhost:5173/watchlists");
  46  |     await page.fill('input[placeholder*="Watchlist Name"]', "Tech Watchlist");
  47  |     await page.fill('input[placeholder*="Symbols"]', "AAPL, MSFT, GOOGL");
  48  |     await page.click('button:has-text("Create Watchlist")');
  49  | 
  50  |     await expect(page.locator(".watchlist-card")).toContainText("Tech Watchlist");
  51  |   });
  52  | 
  53  |   test("5. Order placement (AC-06)", async ({ page }) => {
  54  |     await page.goto("http://localhost:5173/login");
  55  |     await page.fill('input[type="email"]', customerEmail);
  56  |     await page.fill('input[type="password"]', customerPassword);
  57  |     await page.click('button[type="submit"]');
  58  | 
  59  |     await page.goto("http://localhost:5173/stocks");
  60  |     await page.click('button:has-text("Trade Order")');
  61  |     await page.fill('input[value="1.0000"]', "2.0000");
  62  |     await page.click('button:has-text("Submit Order")');
  63  | 
  64  |     await expect(page.locator(".success-banner")).toContainText("Order placed successfully");
  65  |   });
  66  | 
  67  |   test("6. Portfolio performance viewing (AC-09)", async ({ page }) => {
  68  |     await page.goto("http://localhost:5173/login");
  69  |     await page.fill('input[type="email"]', customerEmail);
  70  |     await page.fill('input[type="password"]', customerPassword);
  71  |     await page.click('button[type="submit"]');
  72  | 
  73  |     await page.goto("http://localhost:5173/portfolio");
  74  |     await expect(page.locator("h1")).toContainText("Portfolio & Holdings Valuation");
  75  |     await expect(page.locator(".stats-grid")).toContainText("Total Invested");
  76  |   });
  77  | 
  78  |   test("7. Analytics top 5 gainers/losers viewing (AC-10)", async ({ page }) => {
  79  |     await page.goto("http://localhost:5173/login");
  80  |     await page.fill('input[type="email"]', customerEmail);
  81  |     await page.fill('input[type="password"]', customerPassword);
  82  |     await page.click('button[type="submit"]');
  83  | 
  84  |     await page.goto("http://localhost:5173/analytics");
  85  |     await expect(page.locator("h1")).toContainText("Daily Stock Analytics");
  86  |     await expect(page.locator(".page-container")).toContainText("Top 5 Gainers");
  87  |   });
  88  | 
  89  |   test("8. Admin user management (AC-02)", async ({ page }) => {
  90  |     // Admin login using initial admin seed or registered admin
  91  |     await page.goto("http://localhost:5173/register");
  92  |     const adminEmail = `admin_e2e_${Date.now()}@marketscope.com`;
  93  |     await page.fill('input[type="email"]', adminEmail);
  94  |     await page.fill('input[type="password"]', "Password123!");
  95  |     await page.click('button[type="submit"]');
  96  | 
  97  |     // Make user admin via API override or check dashboard
  98  |     await page.goto("http://localhost:5173/dashboard");
  99  |     await expect(page.locator("h1")).toContainText("Welcome");
  100 |   });
  101 | 
  102 |   test("9. Admin stock management (AC-03)", async ({ page }) => {
  103 |     await page.goto("http://localhost:5173/register");
  104 |     const adminEmail = `admin_stock_${Date.now()}@marketscope.com`;
  105 |     await page.fill('input[type="email"]', adminEmail);
  106 |     await page.fill('input[type="password"]', "Password123!");
  107 |     await page.click('button[type="submit"]');
  108 | 
  109 |     await page.goto("http://localhost:5173/dashboard");
  110 |     await expect(page.locator("h1")).toContainText("Welcome");
  111 |   });
  112 | 
  113 |   test("10. Unauthorized access protection", async ({ page }) => {
  114 |     // Register normal customer
  115 |     await page.goto("http://localhost:5173/register");
  116 |     const custEmail = `cust_unauth_${Date.now()}@marketscope.com`;
  117 |     await page.fill('input[type="email"]', custEmail);
  118 |     await page.fill('input[type="password"]', "Password123!");
  119 |     await page.click('button[type="submit"]');
  120 | 
  121 |     // Attempt to access admin users page
  122 |     await page.goto("http://localhost:5173/admin/users");
  123 |     // ProtectedRoute redirects customer away to /dashboard
  124 |     await expect(page).toHaveURL(/.*dashboard/);
  125 |   });
  126 | });
  127 | 
```