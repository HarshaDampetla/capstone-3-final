# Frontend Guidelines & Standards

## Code & Component Rules
- Written in React 18, TypeScript, and Vite.
- Use strict type annotations for all components and API service calls.
- Format currency values cleanly using fixed-point formatting (`.toFixed(2)` or `Intl.NumberFormat`).
- Authenticated requests must attach JWT Bearer tokens in headers.
- Support responsive layout for mobile, tablet, and desktop viewports (BUS-03).
- UI flows must be testable via Playwright E2E and visual snapshot assertions.
