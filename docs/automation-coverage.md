# Automation coverage and verification

Date: 2026-09-24 (America/Los_Angeles). Target: https://www.saucedemo.com/.

The user authorized automation after the original manual drafts. The implementation uses the Python interpreter configured in PyCharm and Playwright's synchronous API with pytest. Playwright MCP is still unavailable; observations and test execution used **local Playwright Chromium**, not MCP. The earlier requirement for MCP exploration has therefore not been satisfied literally. This method difference is recorded rather than hidden.

## Evidence basis

Browser interaction confirmed the ten application pages listed in the [README](../README.md). The primary flow is login → products → product details or add from products → cart → checkout information → overview → completion → back home. A public demo account and password are displayed on the login screen. No private credentials are stored.

Assertions are **observed regression baselines**, not approved business requirements. Test assertions below are also the concrete expected results for the corresponding instantiated manual cases. Setup and test data are explicit in `tests/conftest.py` and parameterized test files. No backend purchase, payment, shipment, security, or performance guarantee is inferred from UI messages.

During local browser exploration:

- Login displayed errors for missing username, missing password, wrong password, and the supplied locked account. Rejected inputs are followed by a valid-login recovery check in the suite.
- Surrounding spaces in the standard username or password were rejected. No universal maximum length or trimming rule is inferred for other inputs.
- Checkout required first name, last name, and postal code. `QA`, `Tester`, `90210` proceeded to overview. **Three single-space values also proceeded to overview.** Intended whitespace validation remains an open requirement; it is not asserted as correct behavior.
- One Backpack appeared at `$29.99`, with item total `$29.99`, tax `$2.40`, and total `$32.39`; completing the demo flow cleared the cart. No universal tax formula is assumed.
- Completion offered a PDF download, which produced a `swag-labs-order-…pdf` file. The automation checks the PDF signature, not semantic contents.
- Dynamic Catalog is an expandable menu, not a page itself. It exposes Lazy Load, Spinner, and Slider pages. Lazy Load revealed item 11 after scrolling; Spinner resolved to product cards; selecting slider dot 4 displayed Backpack at `$29.99`.

## Manual script traceability

| Manual ID | Concrete automated coverage | Priority | Smoke | Regression | Remaining limit |
| --- | --- | --- | --- | --- | --- |
| EXP-001 | `test_exploration_evidence.py::test_capture_primary_pages`, plus dynamic-page captures | P0 discovery prerequisite; capture utility P3 | No | Capture runs in full suite, outside regression selection | Recorded tour/evidence automated; open-ended discovery and requirement judgment remain manual |
| MT-001 | `test_login.py::test_valid_login`; `test_checkout_overview.py::test_overview_item_and_total`; `test_checkout_complete.py::test_complete_purchase_and_return_home` | P0 Critical | Login and completed purchase | Yes | Standard user, one-product purchase; other accounts and combinations not claimed |
| MT-002 | Sorting in four orders; details consistency and add/remove; cart removal; logout; cancellation from both checkout stages; PDF download; lazy loading; spinner completion; slider selection | P2 Medium; logout/cart removal P1 High | No | Yes | External About/social sites, reset menu semantics, and PDF contents not covered |
| MT-003 | Three login missing-value cases and four checkout missing-value cases, each with valid recovery | P1 High | Login cases | Yes | Exact observed errors; no claim about inaccessible or undocumented validation |
| MT-004 | Wrong password and locked account rejected, then standard login succeeds | P1 High | No | Yes | Does not infer checkout format rules or authorization security |
| MT-005 | Spaces surrounding username and password rejected, then valid recovery | P2 Medium | No | Yes | Checkout length/format/whitespace rules unresolved: explicit skip |
| MT-006 | Cart item and badge retained through inventory refresh, cart refresh, and cart → inventory → cart navigation | P1 High | No | Yes | Browser restart, logout persistence, cross-user state, and multi-tab behavior not verified |
| MT-007 | Add changes to Remove, badge becomes 1; remove clears badge; re-add yields exactly one cart row with quantity 1 | P1 High | No | Yes | No forced double click on a removed control; no backend duplicate-order claim |
| MT-008 | Page readiness/labels asserted throughout tests; screenshots and accessibility snapshots captured for ten pages | P3 Low | No | Deterministic labels covered; screenshot review separate | Visual pass/fail comparison explicitly skipped pending approved baseline; subjective usability remains manual |

Every test carries a `manual_script` marker. `smoke`, `regression`, and priority markers make the coverage executable rather than just descriptive. Functional tests have one source priority; evidence utilities are labeled separately from functional coverage.

## Isolation and maintenance

- The pytest Playwright plugin creates a fresh context for each test and closes it on teardown, including failures. Fixtures log in through the UI and assert an empty initial cart. No local-storage bypass, fixed sleeps, or dependency on test execution order is used.
- Page objects hold selectors and reusable interactions, with a shared header component. `data-test` is configured as Playwright's test-ID attribute. URL checks and retrying locator assertions wait for page readiness.
- Tests are grouped by page, with a separate cross-page evidence tour. Synthetic checkout data and the observed Backpack product are deterministic test data.
- Dependency versions are pinned in `requirements.txt`; only Chromium desktop has been validated. Browser-support requirements are not established.

## Execution results

Final validation: **33 passed, 2 intentionally skipped in 34.11 seconds** using local Chromium at 1280×800. Command: `.venv/bin/python -m pytest -q -x --output artifacts/verification --junitxml=artifacts/verification.xml`. The JUnit report is [verification.xml](../artifacts/verification.xml); captures are under `artifacts/verification/`. This separate directory preserves verification evidence from subsequent runs that clear the default `test-results/` directory. Of the passing cases, 32 are functional regression cases and one is the primary-page evidence tour. Five passing functional cases are marked smoke. The two skips cover undefined checkout boundaries and visual approval. Initial development failures in a shared URL assertion were fixed; an interrupted obsolete run is not the acceptance result.

Evidence is generated under the configured Playwright output directory. A successful capture means the recorded flow completed and files were written; it does not mean screenshots were approved. The two intentional skips are visible in pytest output and the JUnit report and must never be counted as passed coverage.
