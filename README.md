# SauceDemo UI tests

Python 3.12, pytest, and Playwright with one page object and one functional test file per application page. Page objects own locators and reusable interactions; tests own scenarios and assertions. Shared header behavior is a composed component. This follows the structure described in [Playwright's POM guide](https://playwright.dev/docs/pom) and its [Python example](https://playwright.dev/python/docs/pom).

## Setup

Run from the project root using the project's configured virtual environment:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
```

The suite accesses the live public demo at `https://www.saucedemo.com`. It uses the public `standard_user` / `secret_sauce` credentials displayed by the application. Each test receives a new browser context; no tests depend on another test's state. Context teardown discards the test's local session state. No production service is involved in the demo purchase flow.

## Run tests

```bash
# Entire suite (Chromium headless)
.venv/bin/python -m pytest -v

# One page's test file
.venv/bin/python -m pytest tests/test_login.py -v
.venv/bin/python -m pytest tests/test_cart.py -v --headed

# One individual test (all its parameter variations, if any)
.venv/bin/python -m pytest tests/test_login.py::test_valid_login -v

# Smoke or regression selection
.venv/bin/python -m pytest -m smoke -v
.venv/bin/python -m pytest -m regression -v

# List available node IDs, including parameterized cases
.venv/bin/python -m pytest --collect-only -q

# Report and failure artifacts
.venv/bin/python -m pytest -v --junitxml=test-results/results.xml

# Capture all traces, including passed tests
.venv/bin/python -m pytest tests/test_cart.py --tracing on
```

Use a quoted node ID copied from `--collect-only` to select one parameter variation. In PyCharm, select this project's `.venv` interpreter and run the desired pytest file or function. Tests are executable files under `tests/`; files under `pages/` are reusable objects, not test entry points.

## Files by page

| Page | Page object | Test file |
| --- | --- | --- |
| Login | `pages/login_page.py` | `tests/test_login.py` |
| Products | `pages/inventory_page.py` | `tests/test_inventory.py` |
| Product details | `pages/product_page.py` | `tests/test_product.py` |
| Cart | `pages/cart_page.py` | `tests/test_cart.py` |
| Checkout information | `pages/checkout_information_page.py` | `tests/test_checkout_information.py` |
| Checkout overview | `pages/checkout_overview_page.py` | `tests/test_checkout_overview.py` |
| Checkout complete | `pages/checkout_complete_page.py` | `tests/test_checkout_complete.py` |
| Dynamic Catalog: Lazy Load | `pages/lazy_load_page.py` | `tests/test_lazy_load.py` |
| Dynamic Catalog: Spinner | `pages/spinner_page.py` | `tests/test_spinner.py` |
| Dynamic Catalog: Slider | `pages/slider_page.py` | `tests/test_slider.py` |

`tests/test_exploration_evidence.py` records the seven-page primary journey with screenshots, accessibility snapshots, URLs, timestamps, browser version, and viewport. Dynamic-page tests also capture evidence. `tests/conftest.py` supplies fixtures and capture support.

## Reports and limitations

Failure screenshots and traces are saved under `test-results/` by default. Each new run clears its configured Playwright output directory. Use `--output test-results/<run-name>` to keep separate runs. Evidence JSON/PNG files are saved per test even when the evidence-capture tests pass. These screenshots are observations, not approved visual baselines. PDF download checks verify a successful download, filename convention, and PDF signature, not receipt content/layout.

Two cases explicitly skip: checkout boundaries without confirmed rules, and visual approval without an approved baseline. Open-ended exploration and subjective visual review still require a person. See [coverage and verification](docs/automation-coverage.md) for the mapping of every manual script, observed behavior, and remaining gaps.
