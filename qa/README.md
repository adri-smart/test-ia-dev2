# Playwright E2E Tests for KAN-463

This project contains the end-to-end (E2E) tests for the Customer Analysis Conversational Agent, implemented using Playwright.

## What is being tested?

These tests validate the functionality of the conversational agent from a user's perspective, covering the user stories defined in Epic KAN-463. This includes:
- Core conversational interface
- User feedback mechanism
- Data visualization
- And other key features.

## Prerequisites

- [Node.js](https://nodejs.org/) (v20 or higher recommended)
- [Python](https://www.python.org/) (as required by the main application)
- A running instance of Redis (if not provided by the backend setup).

## Installation

1.  **Install main project dependencies:**
    Follow the setup instructions in the root `README.md` to create the Python virtual environment and install dependencies.

2.  **Install test suite dependencies:**
    From the root of the project, run:
    ```bash
    npm --prefix qa install
    ```

3.  **Install Playwright browsers:**
    ```bash
    npx --prefix qa playwright install --with-deps
    ```

4.  **Set up environment variables:**
    Copy `qa/.env.example` to `qa/.env` and fill in any required values.
    ```bash
    cp qa/.env.example qa/.env
    ```

## Running Tests

The Playwright configuration is set up to automatically start the Python backend and a simple web server for the frontend.

-   **Run all tests in headless mode:**
    ```bash
    npm run test --prefix qa
    ```

-   **Run tests with the Playwright UI:**
    ```bash
    npm run test:ui --prefix qa
    ```

## Viewing Reports

After running the tests, an HTML report will be generated in `qa/playwright-report/`. You can view it by running:

```bash
npm run report --prefix qa
```

## Project Structure

```
qa/
├── .github/
│   └── workflows/
│       └── playwright.yml      # CI workflow for running tests
├── components/                 # Reusable UI component page objects
├── pages/                      # Page Object Model (POM) files
├── tests/                      # Test files (specs)
├── .env.example                # Environment variable template
├── .gitignore
├── package.json
├── playwright.config.ts
├── README.md
└── tsconfig.json
```

## Conventions and Best Practices

-   **Page Object Model (POM):** All interactions with the UI are encapsulated within page objects (`/pages`) or component objects (`/components`).
-   **Selectors:** Use `data-testid` attributes for robust selectors where possible.
-   **Independence:** Tests are written to be independent and can be run in any order.
-   **AAA Pattern:** Tests follow the Arrange, Act, Assert pattern for clarity.
