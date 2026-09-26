# SauceDemo UI tests

**Main:** [![Main CI status](https://github.com/IgorKorobchenko/saucedemo-playwright-tests/actions/workflows/playwright.yml/badge.svg?branch=main&event=push)](https://github.com/IgorKorobchenko/saucedemo-playwright-tests/actions/workflows/playwright.yml?query=branch%3Amain+event%3Apush)
**Pull requests:** [![Pull request CI status](https://github.com/IgorKorobchenko/saucedemo-playwright-tests/actions/workflows/playwright.yml/badge.svg?event=pull_request)](https://github.com/IgorKorobchenko/saucedemo-playwright-tests/actions/workflows/playwright.yml?query=event%3Apull_request)

These live GitHub badges show workflow results, not a hardcoded status. Main tracks push runs on `main`; Pull requests tracks the latest pull-request run across branches. For an individual PR, check its **Checks** tab. Main will show a result after the workflow is merged and runs on `main`. Click either badge to open the corresponding runs. GitHub may briefly cache badge updates. See [GitHub's status badge documentation](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge).

Python 3.12, pytest, and Playwright with one page object and one functional test file per application page. Page objects own locators and reusable interactions; tests own scenarios and assertions. Shared header and footer behavior lives in components. This follows the structure described in [Playwright's POM guide](https://playwright.dev/docs/pom) and its [Python example](https://playwright.dev/python/docs/pom).

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

# Scenarios added from the old-framework coverage comparison
.venv/bin/python -m pytest -m coverage_gap -v

# Exclude observed baselines (empty cart, sampled inputs, current screenshots)
.venv/bin/python -m pytest -m 'regression and not observed_baseline' -v

# Visual comparisons only; requires a baseline for this browser/platform
.venv/bin/python -m pytest -m visual -v

# List available node IDs, including parameterized cases
.venv/bin/python -m pytest --collect-only -q

# Report and failure artifacts
.venv/bin/python -m pytest -v --junitxml=test-results/results.xml

# Capture all traces, including passed tests
.venv/bin/python -m pytest tests/test_cart.py --tracing on
```

Use a quoted node ID copied from `--collect-only` to select one parameter variation. In PyCharm, select this project's `.venv` interpreter and run the desired pytest file or function. Tests are executable files under `tests/`; files under `pages/` are reusable objects, not test entry points.

## GitHub Actions

The `Playwright tests` workflow runs all 69 nonvisual tests (including smoke scenarios) on pushes to `main`, pull requests targeting `main`, and manual runs from the repository's **Actions** tab. It uses Python 3.12 and the official Playwright `v1.63.0-noble` Linux container, following [Playwright's CI guidance](https://playwright.dev/python/docs/ci). Keep the container version in both workflows aligned with `requirements.txt` when upgrading Playwright.

Download `functional-results` from a run's **Artifacts** section for JUnit XML, evidence captures, and failure screenshots/traces. Artifacts are retained for 14 days, including when tests fail. Open a downloaded trace with `.venv/bin/python -m playwright show-trace path/to/trace.zip`. Failed tests fail the workflow; there are no automatic retries or baseline updates. A newer run cancels an older run for the same branch/PR. No repository secrets are required for the public demo.

`Record visual baselines` is a separate manual workflow for generating Linux PNG/JSON files in the same container. Download `linux-visual-baselines`, inspect every image, and copy its environment directory into `tests/visual_baselines/` before committing. Recording is not a visual comparison or design approval. This workflow has read-only permissions and cannot commit baseline updates.

The seven visual comparisons currently run locally using the committed macOS baselines. They are explicitly excluded from the Linux functional job; Linux baselines still need to be recorded and reviewed. After adding them, enable visual comparisons in the main workflow by removing `-m "not visual"` from its pytest command. Never add `--update-visual-baselines` to the normal CI run.

First-time activation: push these workflow files to GitHub. If HTTPS push reports a missing `workflow` scope, update the saved classic Personal Access Token's permissions in GitHub settings, then retry `git push origin main`. Once pushed, open **Actions → Playwright tests** to inspect the automatic run. Use **Actions → Record visual baselines → Run workflow** for the one-time Linux baseline setup above.

This repository delivers automated test results; it has no application to deploy. Branch protection is a separate repository setting: select the CI checks as required checks if you want to block merging failed pull requests.

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

`test_data/products.json` contains the six-product baseline observed on 2026-09-25. Tests load it through `test_data/products.py`; they do not generate expected values from the live page during execution. Shared locators stay in `pages/header.py` and `pages/footer.py`.

## Reports and limitations

Every normal pytest run generates a self-contained HTML report at `artifacts/report.html`. At the end of the terminal output, `Generated html report: file:///.../artifacts/report.html` links to the report. Open that URL in your browser to see results, durations, and failure details. Each run replaces this report; use `--html=artifacts/my-run.html` to keep a separate report. Install the updated `requirements.txt` before running tests.

The report includes an outcome distribution chart, pass percentage, and horizontal bars for the 10 slowest tests (including setup and teardown). Each executed test is counted once; setup/teardown errors override a passing test body. Charts describe the whole run and do not change when filtering the results table. They work offline without external chart libraries.

GitHub Actions includes the HTML report in the `functional-results` artifact. Download and extract that artifact, then open `report.html`; the `file://` URL printed in CI refers to the runner's filesystem, not a public website. Screenshots and traces remain separate files in the artifact.

Latest local verification (2026-09-25): **76 passed, 0 skipped in 70.18 seconds**, including normal visual comparisons without baseline updates. Command: `.venv/bin/python -m pytest -q --output artifacts/no-skips --junitxml=artifacts/no-skips.xml`. This supersedes the earlier 64-passed/two-skipped report.

Failure screenshots and traces are saved under `test-results/` by default. Each new run clears its configured Playwright output directory. Use `--output test-results/<run-name>` to keep separate runs. Evidence JSON/PNG files are saved per test even when the evidence-capture tests pass. These screenshots are observations, not approved visual baselines. PDF download checks verify a successful download, filename convention, and PDF signature, not receipt content/layout.

The two original skipped placeholders have been replaced with executable observed-baseline checks: five checkout input samples and seven primary-page screenshot comparisons. Single characters, whitespace-only values, surrounding whitespace, Unicode, and 256-character strings currently reach checkout overview. The number 256 is a tested sample, not a documented maximum length. Required empty-field rejection remains covered separately. These tests detect changes in behavior; they do not approve the validation rules or establish that all input lengths/formats work.

## Visual regression baselines

Visual tests compare decoded RGB pixels against files under `tests/visual_baselines/`. Initial images record the observed application; they are not an approved design specification. Baselines are separate for browser version, operating system, architecture, and viewport. Visual tests always launch the bundled browser headless, even when `--headed` is supplied for functional tests, because headed rendering changes fonts and scrollbar dimensions. The visual context fixes 1280×800, scale factor 1, light mode, reduced motion, and en-US locale; capture waits for fonts/images, disables animations, and hides the caret.

Normal runs **fail** for missing baselines, different image dimensions, or any changed pixel. They never silently create/replace expected images. Actual and expected images are saved in the test's output directory; a pixel mismatch also saves `diff.png`. This strict comparison intentionally requires review after browser, platform, font, or UI changes. A matching screenshot does not replace accessibility or usability testing.

To deliberately create or replace baselines after reviewing the application:

```bash
.venv/bin/python -m pytest -m visual --update-visual-baselines
# Then verify in a separate run without the update flag:
.venv/bin/python -m pytest -m visual
```

Review the image changes and commit the PNG and JSON files together. Baseline-recording runs are setup, not successful comparisons. The implementation uses [Playwright screenshots](https://playwright.dev/python/docs/screenshots) and [Pillow pixel differences](https://pillow.readthedocs.io/en/stable/reference/ImageChops.html#PIL.ImageChops.difference). `support/visual.py` contains the comparator; `tests/test_visual.py` covers login, inventory, product details, cart, information, overview, and completion. Dynamic catalog pages remain outside the visual baseline suite.

Open-ended exploration, approval of business rules, and subjective design review still require a person. None are reported as automated passes merely because the placeholder skips were replaced.

The local `docs/` folder is intentionally excluded from Git. Empty-cart checkout is marked `observed_baseline`: it currently reaches an empty overview with $0 totals. This detects behavioral changes without claiming that empty checkout is the intended business rule. The test cancels at overview and does not test finishing an empty order. About navigation is checked with the external destination response stubbed; social links are checked by URL, not by visiting them. These checks do not validate external site availability or content.

[![GitHub Actions Playwright tests](https://github.com/IgorKorobchenko/saucedemo-playwright-tests/actions/workflows/playwright.yml/badge.svg)](https://github.com/IgorKorobchenko/saucedemo-playwright-tests/actions/workflows/playwright.yml)
