# Testing Strategy

## Goal

Prove that the financial calculations are correct, the application handles bad external data safely, and the deployed import/startup assumptions match local and CI assumptions.

## Test layers

### 1. Unit tests

Pure financial functions are tested against deterministic, hand-verifiable fixtures. Tests cover normal calculations and edge cases for validation, returns, volatility, risk metrics, correlation, and regimes.

### 2. Data-loader tests

`yfinance` is mocked at the data-loader boundary. The suite explicitly tests:
- valid provider data;
- empty provider response;
- provider exception;
- rate-limit-like failure;
- malformed columns/data.

The test suite never calls Yahoo Finance. This is deliberate because the previous project had tests that had to be retrofitted to mock `yfinance` after rate-limit behavior interfered with deterministic tests. fileciteturn14file0L3-L11

### 3. Integration tests

Integration tests exercise the pipeline from a deterministic DataFrame through validation, returns, and risk analytics. They verify that module contracts fit together without involving the network.

### 4. Streamlit smoke test

Import the Streamlit entry module under the same package installation assumptions used in CI and Render. Startup must not perform a live network request merely because the module is imported.

A second local smoke check runs Streamlit using the production-style command and verifies the process can start without a traceback when live data is not required for module initialization.

## Coverage

CI enforces a minimum of 80% meaningful coverage, with the financial calculation layer expected to be substantially higher. Coverage is measured with `pytest-cov` and is never guessed or manually reported.

## Static analysis

CI runs:

```text
ruff check .
black --check .
```

Both must pass before the test result is accepted.

## CI pipeline

The single CI workflow runs on pushes to `main` and pull requests targeting `main`:

```text
checkout
  ↓
setup Python
  ↓
install pinned dependencies
  ↓
Ruff
  ↓
Black
  ↓
pytest + coverage
  ↓
Streamlit import/startup smoke test
```

There are no scheduled workflows, notification bots, or screenshot jobs attached to normal pushes.

## External-data failure policy

A provider failure is an expected runtime condition, not a reason to make tests depend on the provider. Tests mock the boundary and assert that the application converts failures into controlled user-facing errors.

No fallback is introduced solely to make tests pass. If demo data is ever added, it must be explicit and visibly identified.

## Deployment validation

Before Render deployment:
1. run the complete local test suite;
2. run Ruff and Black checks;
3. run the Streamlit startup smoke test using production-style assumptions;
4. verify the final dependency and Python versions;
5. inspect repository contents for secrets and temporary workflows;
6. deploy once after CI is green.

After deployment, verify the actual live application: startup, title, sidebar, data retrieval, charts, metrics, control changes, and graceful invalid/no-data behavior.

A green deployment status alone is not considered proof that the application works.
