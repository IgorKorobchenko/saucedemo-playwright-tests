# SauceDemo manual test scripts

Source: [Test plan](test-plan.md). Drafted: 2026-09-24.

These are the original human-executed script templates. After the user authorized automation, concrete cases were implemented using local Playwright Chromium and a Page Object Model. See [automation coverage and verification](automation-coverage.md) for all script mappings, observed expectations, execution results, and explicit gaps. The generic templates below remain reusable drafting guidance; their original pending placeholders are not the current execution status of the implemented cases.

## Execution rules

- Use https://www.saucedemo.com/ as the entry point. The plan requires Playwright MCP for the initial exploration; its availability must be checked before execution.
- Record browser/version, viewport, date, tester, starting state, and evidence for each run. Use synthetic data and only accounts explicitly supplied by the application or project owner.
- Before executing an MT script, replace every placeholder with an observed control, concrete data, and a documented expected result. Create a separate case for each flow, field, or input variation; retain the parent script ID for traceability.
- Distinguish a requirement-backed expectation from an observed baseline. A baseline is useful for detecting change but does not prove the product is correct.
- If a prerequisite or expected result is unknown, mark the case **Blocked** or **Needs clarification**. Record observations without assigning Pass or Fail. If exploration confirms the feature does not exist, mark the template **Not applicable** and record the evidence.
- Restore the verified starting state before each independent case. Do not assume refresh, logout, or reopening the browser resets application state.

## Coverage index

Priorities and suite assignments below are provisional proposals, not verified scenario membership. “Candidate” requires the stated feature, deterministic setup, and expected result to be established first. Regression candidates include any adopted smoke cases.

| ID | Purpose | Type | Priority and rationale | Smoke | Regression | Future UI automation |
| --- | --- | --- | --- | --- | --- | --- |
| EXP-001 | Discover controls, flows, rules, and reset procedure | Exploration | P0 Critical: prerequisite for meaningful testing | No | No | Manual/exploratory |
| MT-001 | Complete a primary journey with valid data | Positive | P0 Critical: primary user objective | Candidate | Candidate | Conditional; strong candidate once deterministic |
| MT-002 | Complete a secondary visible action | Positive | P2 Medium: supporting function | No | Candidate | Conditional; value depends on repetition |
| MT-003 | Omit a confirmed required value | Negative | P1 High: validation and recovery | Candidate only if critical | Candidate | Conditional; parameterize confirmed required fields later |
| MT-004 | Violate a confirmed input rule | Negative | P1 High: invalid data handling | No | Candidate | Conditional; explicit rule and outcome required |
| MT-005 | Exercise a confirmed input boundary | Edge | P2 Medium: boundary handling | No | Candidate | Conditional; explicit limits required |
| MT-006 | Revisit state through navigation and refresh | Edge | P1 High: state consistency | No | Candidate | Conditional; persistence expectations required |
| MT-007 | Repeat an observed state-changing action | Edge | P1 High: possible unintended repeated effect | No | Candidate | Conditional; repeat-action semantics required |
| MT-008 | Review secondary labels and presentation | Positive | P3 Low: minor presentation quality | No | Candidate for manual review | Manual; visual automation only with an approved baseline |

## EXP-001 — Establish an evidence-backed flow inventory

**Preconditions:** Playwright MCP is available and can open the target. No prior application state is assumed.

| Step | Manual action | Record / completion checkpoint |
| --- | --- | --- |
| 1 | Open the supplied URL in the browser. | Initial and final URL, page title, visible page, browser details, snapshot or screenshot. Record any access failure as a blocker. |
| 2 | Inventory visible controls, links, text, and any supplied test credentials. | Exact labels and evidence. Do not infer behavior from a label alone. |
| 3 | Follow a visible path toward a user objective using supplied credentials and synthetic inputs where applicable. | Each action, input, page transition, and visible state change. If data is unavailable, record the blocker instead of inventing credentials. |
| 4 | Exercise visible alternate paths and recovery controls from a reproducible starting state. | Actual outcomes, errors, and the inputs that produced them. |
| 5 | Establish how to return to the starting state and verify it visibly. | Exact reset steps and any state that remains. |
| 6 | Repeat for remaining visible functions and map related pages. | Flow IDs, prerequisites, primary/secondary classification with rationale, and unvisited paths. |
| 7 | Update the source plan and instantiate applicable MT scripts. | Evidence-linked flows and concrete cases; unknown expectations remain explicitly unresolved. |

**Expected outcome:** A documented inventory and evidence trail, not a predetermined page or business outcome. No product pass/fail verdict is assigned by this procedure.

## MT-001 — Complete a primary journey

**Plan trace:** Primary journeys; positive coverage; smoke selection.

**Preconditions/data:** `<verified flow ID>`, `<starting state>`, `<valid synthetic inputs>`, `<completion expectation and source>`, and `<verified reset steps>` are documented.

1. Establish the starting state and record its visible indicators.
2. Follow the recorded flow one action at a time, using the specified valid inputs.
3. Compare every significant page transition and state change with the documented flow.
4. Verify the documented completion indicator and resulting visible data.
5. Restore the starting state using the verified reset procedure.

**Expected result:** Transitions, final indicator, and resulting data match the instantiated case's documented expectations. Exact application outcomes are **pending exploration**.

## MT-002 — Complete a secondary action

**Plan trace:** Secondary paths; positive regression coverage.

**Preconditions/data:** An observed `<secondary action>` with `<entry page>`, `<input if applicable>`, and `<expected outcome and source>`.

1. Establish the recorded entry state.
2. Activate the exact observed control and provide the case's input if required.
3. Inspect the resulting page or changed data.
4. Return using an observed navigation path and perform the verified cleanup.

**Expected result:** The action and return path match the documented expectations. Their actual behavior is **unverified**.

## MT-003 — Submit with a required value missing

**Plan trace:** Visible validation and recovery; negative coverage.

**Preconditions/data:** An observed form, a confirmed required `<field>`, valid values for other fields, and a documented rejection/recovery expectation. Create one case per required field; consider an all-required-fields-empty case separately.

1. Open the form in its verified initial state.
2. Fill other fields with the specified valid data; leave the target field empty.
3. Activate the observed submission control once.
4. Record validation text, field indicators, current page, and any state change.
5. Enter a valid value in the target field and submit again.
6. Record recovery and perform verified cleanup.

**Expected result:** The confirmed required-field rule prevents the invalid operation; correcting the value permits the documented valid path. Exact messages and data-retention behavior require evidence before assertion.

## MT-004 — Submit a value that violates a confirmed rule

**Plan trace:** Invalid input against an observed control or rule.

**Preconditions/data:** `<field>`, `<documented rule>`, `<specific invalid value>`, `<valid correction>`, and `<expected rejection>`. Do not assume format restrictions exist.

1. Establish a valid baseline state.
2. Change only the target value to the specified invalid input.
3. Submit using the observed control.
4. Record the result and compare it with the documented rule.
5. Correct the value, resubmit, and verify the documented recovery path.
6. Perform verified cleanup.

**Expected result:** Rejection and recovery match the confirmed rule. If the rule is unknown, this is an exploratory observation with **Needs clarification**, not a failed test.

## MT-005 — Check input boundaries

**Plan trace:** Empty, whitespace, and length exploration; edge coverage.

**Preconditions/data:** An observed input and confirmed boundary or normalization rule. Define separate cases for each relevant value: a stated length limit minus one, exactly the limit, and plus one; whitespace-only or leading/trailing whitespace only where relevant. Specify the actual strings and how length is measured.

1. Restore the initial state for the individual case.
2. Enter the specified value; record what remains visibly entered.
3. Trigger the observed validation/submission action.
4. Record acceptance, rejection, normalization, or truncation and any resulting state.
5. Compare with the explicit rule, then clean up.

**Expected result:** Behavior matches the case's confirmed boundary rule. No maximum length, trimming policy, or whitespace rejection is currently established.

## MT-006 — Check state when revisiting a page

**Plan trace:** Navigation, refresh, and cross-page state consistency.

**Preconditions/data:** An observed state-changing flow, visible state indicators, a second observed page, and a documented retention/reset expectation for each transition. Run navigation and refresh as separate cases.

1. Establish the baseline and perform the recorded state-changing action.
2. Record the resulting visible state.
3. For the navigation case, follow the observed path away and back. For the refresh case, refresh the page once.
4. Inspect the same indicators and compare them with the transition-specific expectation.
5. Restore state using the verified procedure.

**Expected result:** State matches the documented transition policy. Persistence or clearing is **not assumed**; browser refresh is not presumed to reset anything.

## MT-007 — Repeat a state-changing action

**Plan trace:** Repeated actions; edge coverage.

**Preconditions/data:** An observed action safe to repeat in the demo, a verified reset procedure, and documented single/repeated-action expectations. If its effects are unknown or cannot be reset, stop pending clarification.

1. Establish the recorded starting state.
2. Perform the action once and record its visible effect.
3. Attempt the same action a second time if the UI still exposes it. Record a disabled or removed control instead of bypassing it.
4. Inspect the final visible state and compare with the documented repeat-action semantics.
5. Perform verified cleanup.

**Expected result:** Each effect matches the documented behavior. A second action may legitimately have another effect; idempotency, duplicate prevention, and control disabling are **not assumed**.

## MT-008 — Review labels and presentation

**Plan trace:** Minor presentation quality; manual coverage.

**Preconditions/data:** Observed pages, recorded viewport, and approved copy/design references where available.

1. Visit each selected page at the recorded viewport.
2. Review secondary text and controls for clipping, overlap, readability, and consistency.
3. Compare with approved references where supplied.
4. Capture evidence for discrepancies and distinguish functional obstruction from minor presentation concerns.

**Expected result:** Matches approved references where available. Without a reference, record usability observations for review rather than asserting a design defect. Reprioritize any issue that blocks a primary journey.

## Execution record

Copy this record for each additional manual case and run. For implemented cases, pytest/JUnit results and [automation coverage](automation-coverage.md) provide the current execution record; do not infer a manual execution result from an automated pass.

| Field | Value to fill during preparation/execution |
| --- | --- |
| Case ID / parent script | Concrete case ID / EXP-001 or MT-001–MT-008 |
| Flow and plan trace | Observed flow ID and source-plan scenario ID once assigned |
| Preconditions and reset | Exact state and verified setup/cleanup actions |
| Test data | Concrete synthetic values; avoid storing sensitive credentials |
| Expected result and source | Requirement reference or explicitly labeled observed baseline |
| Environment | Date, tester, browser/version, viewport, target URL |
| Actual result | Step-level observations; leave blank until executed |
| Evidence | Snapshot/screenshot references, relevant page URLs and messages |
| Outcome | Not run / Pass / Fail / Blocked / Needs clarification / Not applicable |
| Defect or question | Reproduction details and issue/reference if created |
| Final priority and suites | Confirmed impact rationale; Smoke and Regression membership |
| Automation assessment | Good candidate / Conditional / Manual, with reason |

Only instantiated cases with supported expectations can enter smoke or regression pass/fail gating. The automation coverage document records which cases now satisfy this condition and which still require clarification or manual review. Playwright MCP exploration remains unavailable; local Playwright execution is explicitly distinguished from it.
