# SauceDemo test plan

Updated: 2026-09-24 (America/Los_Angeles). Target: https://www.saucedemo.com/.

## Status and scope

The user has authorized automation. A Python/pytest/Playwright Page Object Model suite now covers the observed primary journey and selected negative, edge, and secondary flows. **Final Chromium run: 33 passed, 2 intentionally skipped.** These are observed regression baselines, not approved business requirements.

Playwright MCP remains unavailable. Browser observations and validation were performed using local Playwright Chromium instead; the original MCP-specific exploration request has not been fulfilled literally. No functionality below is inferred solely from prior knowledge of SauceDemo.

Related documents: [manual script templates](manual-test-scripts.md), [scenario mapping and verification](automation-coverage.md), [setup and commands](../README.md).

## Observed functionality and flows

| Flow | Observed functionality | Concrete coverage |
| --- | --- | --- |
| F01 Access | Public test usernames/password displayed; standard login succeeds; missing credentials, wrong password, and locked account produce errors; logout returns to login | Valid access, rejection, and recovery tests |
| F02 Browse | Inventory contains named products, descriptions, prices, detail navigation, and four sorting options | Four sort orders; details match inventory; return navigation |
| F03 Cart | Add/Remove controls and badge; cart rows show product, price, and quantity; continue shopping and checkout controls | Add/remove/re-add; cart removal; quantity 1; refresh/navigation persistence |
| F04 Checkout | First name, last name, and postal code; validation errors; overview; cancellation; Finish | Required-value omission/recovery; item and total checks; cancel from both stages |
| F05 Completion | Completion message, cleared cart, Back Home, Generate PDF order | Full purchase journey, empty resulting cart, PDF download/signature |
| F06 Dynamic catalog | Expandable submenu opens three distinct pages: Lazy Load, Spinner, Slider | Scroll reveals later item; loaded spinner grid; selected slider item |

Primary journey: login → inventory → select product → cart → enter information → review → finish → return home. All ten observed application pages have separate page-object and functional test files. Shared header controls are modeled as a component.

## Priority and suites

| Priority | Impact criterion | Included scenarios |
| --- | --- | --- |
| P0 Critical | Failure blocks the primary user objective | Valid login; item/total overview; completed purchase and cleared cart |
| P1 High | Failure disrupts major validation or state handling | Missing fields and recovery; wrong credentials/locked account; cart removal; refresh/navigation consistency; repeated add/remove; logout |
| P2 Medium | Supporting functions and bounded edge cases | Sorting; product details; checkout cancellation; credential whitespace; PDF generation; dynamic catalog interactions |
| P3 Low | Presentation observations with limited functional impact | Screenshot/label evidence and pending visual baseline review |

**Smoke:** valid login, three login required-value/recovery cases, and the complete purchase flow. All five cases are marked `smoke` and are also part of regression.

**Regression:** all implemented functional checks, including smoke, are marked `regression`. The primary-page evidence tour is separate from regression pass/fail gating. All functional cases map to manual script IDs through pytest markers; [the coverage matrix](automation-coverage.md#manual-script-traceability) specifies the concrete cases, expected results, limits, and priority rationale.

**UI automation:** deterministic UI actions with retrying assertions are implemented. A browser context is created and discarded per case; fixtures establish verified starting state via the UI. No fixed sleeps, direct local-storage setup, or inter-test ordering dependency is used.

## Positive, negative, and edge coverage

- Positive: successful access, product browsing/sorting, details consistency, cart operations, completed checkout, cancel/return navigation, PDF download, and dynamic catalog interactions.
- Negative: missing login/checkout inputs, wrong password, and the supplied locked account. Valid correction/recovery follows rejection.
- Edge: surrounding credential whitespace, refresh and navigation after adding an item, add-control replacement and remove/re-add behavior, and dynamic content loaded by scrolling.
- Evidence support: screenshots and accessibility snapshots record URLs, timestamps, browser version, and viewport for the primary and dynamic pages. A capture does not establish visual correctness.

## Unverified requirements and exclusions

Two explicit skipped cases prevent unsupported assertions:

1. Checkout length/format/whitespace boundary rules are unspecified. Single-space first name, last name, and postal code were accepted in exploration; the intended behavior needs clarification.
2. Visual approval has no approved design/copy/image baseline. Screenshot capture is implemented; subjective review and approval remain manual.

Open-ended exploration is only assisted by the recorded tour. No claim of complete discovery is made. Other special accounts, all product combinations, empty-cart checkout semantics, session expiry, browser restart/multi-tab state, reset-menu behavior, external destinations, PDF content/layout, cross-browser/mobile support, accessibility compliance, security, and performance have not been verified by this suite. P0/P1 defects outside covered paths can still exist.

## Execution and evidence

Environment: PyCharm-configured Python 3.12.6 virtual environment; Playwright 1.63.0; pytest 9.1.1; pytest-playwright 0.9.0; Chromium desktop, 1280×800.

Final validation command:

```bash
.venv/bin/python -m pytest -q -x --output artifacts/verification --junitxml=artifacts/verification.xml
```

Result: **33 passed, 2 skipped in 34.11 seconds.** The JUnit report is at `artifacts/verification.xml`; screenshots and observation JSON are under `artifacts/verification/`. Output files are generated artifacts and ignored by version control. Subsequent runs can replace their configured output directory.

Acceptance for implemented coverage: all executable functional assertions pass, skips are explicit, every case maps to a manual template, and setup/cleanup is independent. Full manual-plan closure still requires resolving the boundary expectations, approving visual baselines, and completing human exploratory review.
