"""Self-contained, accessible charts for the pytest HTML summary."""

from collections import Counter
from html import escape

import pytest


REPORTS = pytest.StashKey[list]()
COLORS = {
    "Passed": "#16803c", "Failed": "#dc2626", "Error": "#b91c1c",
    "Skipped": "#64748b", "XFailed": "#b7791f", "XPassed": "#7c3aed",
    "Incomplete": "#475569",
}


def render_charts(reports):
    """Count each test once; setup/teardown errors override a passing call."""
    tests = {}
    priority = {"Incomplete": 0, "Passed": 1, "Skipped": 2, "XFailed": 3,
                "XPassed": 4, "Failed": 5, "Error": 6}
    for report in reports:
        test = tests.setdefault(report.nodeid, {"outcome": "Incomplete", "duration": 0})
        test["duration"] += report.duration
        outcome = "Incomplete"
        if report.failed:
            outcome = "Failed" if report.when == "call" else "Error"
        elif report.skipped:
            outcome = "XFailed" if hasattr(report, "wasxfail") else "Skipped"
        elif report.when == "call":
            outcome = "XPassed" if hasattr(report, "wasxfail") else "Passed"
        if priority[outcome] > priority[test["outcome"]]:
            test["outcome"] = outcome

    counts = Counter(test["outcome"] for test in tests.values())
    total = len(tests)
    parts = ['<section aria-label="Test charts" style="max-width:1000px;margin:24px 0">',
             '<h2>Test outcomes</h2>',
             '<p>Each test is counted once. Setup or teardown errors override its result.</p>']
    if not total:
        return ''.join(parts) + '<p>No test execution results available.</p></section>'
    passed = counts["Passed"]
    parts.append(f'<p><strong>{total} tests · {passed / total:.0%} passed</strong></p>')
    parts.append('<div style="display:flex;height:32px;border-radius:6px;overflow:hidden" aria-hidden="true">')
    for outcome, color in COLORS.items():
        if counts[outcome]:
            label = f'{outcome}: {counts[outcome]}'
            parts.append(f'<div title="{label}" style="width:{counts[outcome] / total * 100:.4f}%;background:{color}"></div>')
    parts.append('</div><p>')
    for outcome, color in COLORS.items():
        parts.append(f'<span style="display:inline-block;margin:8px 16px 0 0;color:{color}">'
                     f'■ {outcome}: <strong>{counts[outcome]}</strong></span>')
    parts.append('</p><h2>Slowest tests</h2><p>Top 10 durations, including setup and teardown. Hover over a name for its full test ID.</p>')
    slowest = sorted(tests.items(), key=lambda item: item[1]["duration"], reverse=True)[:10]
    maximum = slowest[0][1]["duration"] or 1
    for nodeid, test in slowest:
        label = escape(nodeid, quote=True)
        duration = test["duration"]
        parts.append(f'<div style="margin:12px 0"><div title="{label}" style="overflow-wrap:anywhere">'
                     f'{label} — <strong>{duration:.2f} s</strong></div>'
                     f'<div style="background:#e2e8f0;height:14px;border-radius:4px;margin-top:4px" aria-hidden="true">'
                     f'<div style="background:#2563eb;height:100%;border-radius:4px;width:{duration / maximum * 100:.4f}%"></div>'
                     '</div></div>')
    parts.append('</section>')
    return ''.join(parts)
