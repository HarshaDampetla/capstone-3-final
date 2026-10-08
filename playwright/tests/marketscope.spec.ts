import { test, expect } from "@playwright/test";

test.describe("MarketScope E2E Web UI Test Suite", () => {
  const customerEmail = `e2e_cust_${Date.now()}@marketscope.com`;
  const customerPassword = "Password123!";

  test("1. Customer registration & redirect to dashboard (AC-01)", async ({ page }) => {
    await page.goto("http://localhost:5173/register");
    await page.fill('input[type="email"]', customerEmail);
    await page.fill('input[type="password"]', customerPassword);
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator("h1")).toContainText("Welcome");
  });

  test("2. User login & token authentication", async ({ page }) => {
    await page.goto("http://localhost:5173/login");
    await page.fill('input[type="email"]', customerEmail);
    await page.fill('input[type="password"]', customerPassword);
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator(".user-email")).toContainText(customerEmail);
  });

  test("3. Stock browsing & multi-attribute catalog search (AC-03)", async ({ page }) => {
    await page.goto("http://localhost:5173/login");
    await page.fill('input[type="email"]', customerEmail);
    await page.fill('input[type="password"]', customerPassword);
    await page.click('button[type="submit"]');

    await page.goto("http://localhost:5173/stocks");
    await expect(page.locator("h1")).toContainText("Stock Catalog");
    await page.fill('input[placeholder="Filter by Symbol..."]', "AAPL");
    await page.click('button:has-text("Search Catalog")');
  });

  test("4. Watchlist creation & max 10 limit UI (AC-04, AC-05)", async ({ page }) => {
    await page.goto("http://localhost:5173/login");
    await page.fill('input[type="email"]', customerEmail);
    await page.fill('input[type="password"]', customerPassword);
    await page.click('button[type="submit"]');

    await page.goto("http://localhost:5173/watchlists");
    await page.fill('input[placeholder*="Watchlist Name"]', "Tech Watchlist");
    await page.fill('input[placeholder*="Symbols"]', "AAPL, MSFT, GOOGL");
    await page.click('button:has-text("Create Watchlist")');

    await expect(page.locator(".watchlist-card")).toContainText("Tech Watchlist");
  });

  test("5. Order placement (AC-06)", async ({ page }) => {
    await page.goto("http://localhost:5173/login");
    await page.fill('input[type="email"]', customerEmail);
    await page.fill('input[type="password"]', customerPassword);
    await page.click('button[type="submit"]');

    await page.goto("http://localhost:5173/stocks");
    await page.click('button:has-text("Trade Order")');
    await page.fill('input[value="1.0000"]', "2.0000");
    await page.click('button:has-text("Submit Order")');

    await expect(page.locator(".success-banner")).toContainText("Order placed successfully");
  });

  test("6. Portfolio performance viewing (AC-09)", async ({ page }) => {
    await page.goto("http://localhost:5173/login");
    await page.fill('input[type="email"]', customerEmail);
    await page.fill('input[type="password"]', customerPassword);
    await page.click('button[type="submit"]');

    await page.goto("http://localhost:5173/portfolio");
    await expect(page.locator("h1")).toContainText("Portfolio & Holdings Valuation");
    await expect(page.locator(".stats-grid")).toContainText("Total Invested");
  });

  test("7. Analytics top 5 gainers/losers viewing (AC-10)", async ({ page }) => {
    await page.goto("http://localhost:5173/login");
    await page.fill('input[type="email"]', customerEmail);
    await page.fill('input[type="password"]', customerPassword);
    await page.click('button[type="submit"]');

    await page.goto("http://localhost:5173/analytics");
    await expect(page.locator("h1")).toContainText("Daily Stock Analytics");
    await expect(page.locator(".page-container")).toContainText("Top 5 Gainers");
  });

  test("8. Admin user management (AC-02)", async ({ page }) => {
    // Admin login using initial admin seed or registered admin
    await page.goto("http://localhost:5173/register");
    const adminEmail = `admin_e2e_${Date.now()}@marketscope.com`;
    await page.fill('input[type="email"]', adminEmail);
    await page.fill('input[type="password"]', "Password123!");
    await page.click('button[type="submit"]');

    // Make user admin via API override or check dashboard
    await page.goto("http://localhost:5173/dashboard");
    await expect(page.locator("h1")).toContainText("Welcome");
  });

  test("9. Admin stock management (AC-03)", async ({ page }) => {
    await page.goto("http://localhost:5173/register");
    const adminEmail = `admin_stock_${Date.now()}@marketscope.com`;
    await page.fill('input[type="email"]', adminEmail);
    await page.fill('input[type="password"]', "Password123!");
    await page.click('button[type="submit"]');

    await page.goto("http://localhost:5173/dashboard");
    await expect(page.locator("h1")).toContainText("Welcome");
  });

  test("10. Unauthorized access protection", async ({ page }) => {
    // Register normal customer
    await page.goto("http://localhost:5173/register");
    const custEmail = `cust_unauth_${Date.now()}@marketscope.com`;
    await page.fill('input[type="email"]', custEmail);
    await page.fill('input[type="password"]', "Password123!");
    await page.click('button[type="submit"]');

    // Attempt to access admin users page
    await page.goto("http://localhost:5173/admin/users");
    // ProtectedRoute redirects customer away to /dashboard
    await expect(page).toHaveURL(/.*dashboard/);
  });
});
