import json
import platform
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import Browser, Page


def compare_screenshot(actual_bytes: bytes, baseline: Path, output: Path):
    """Require identical decoded RGB pixels; preserve diagnostic images on failure."""
    output.mkdir(parents=True, exist_ok=True)
    actual_path = output / "actual.png"
    actual_path.write_bytes(actual_bytes)
    assert baseline.is_file(), (
        f"Missing visual baseline: {baseline}. Inspect {actual_path}, then explicitly "
        "create baselines with pytest -m visual --update-visual-baselines."
    )
    with Image.open(BytesIO(actual_bytes)) as image:
        actual = image.convert("RGB")
    with Image.open(baseline) as image:
        expected = image.convert("RGB")
    expected.save(output / "expected.png")
    assert actual.size == expected.size, (
        f"Screenshot dimensions changed: {expected.size} -> {actual.size}. See {output}"
    )
    difference = ImageChops.difference(expected, actual)
    if difference.getbbox() is not None:
        difference.save(output / "diff.png")
        raise AssertionError(f"Screenshot differs from {baseline}. See actual/expected/diff.png in {output}")


def assert_visual_baseline(page: Page, browser: Browser, name: str, baseline_root: Path,
                           output: Path, update: bool = False):
    """Record only on explicit request; normal runs never create or replace baselines."""
    page.evaluate("document.fonts.ready")
    page.wait_for_function("Array.from(document.images).every(image => image.complete)")
    page.mouse.move(0, 0)
    page.evaluate("document.activeElement instanceof HTMLElement && document.activeElement.blur()")
    viewport = page.viewport_size
    assert viewport is not None
    environment = (
        f"{browser.browser_type.name}-{browser.version}-{platform.system().lower()}-"
        f"{platform.machine().lower()}-{viewport['width']}x{viewport['height']}"
    )
    baseline = baseline_root / environment / f"{name}.png"
    screenshot = page.screenshot(full_page=True, animations="disabled", caret="hide", scale="css")
    if update:
        baseline.parent.mkdir(parents=True, exist_ok=True)
        baseline.write_bytes(screenshot)
        baseline.with_suffix(".json").write_text(json.dumps({
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "url": page.url,
            "browser": browser.browser_type.name,
            "browser_version": browser.version,
            "os": platform.system(),
            "architecture": platform.machine(),
            "viewport": viewport,
            "device_scale_factor": 1,
            "color_scheme": "light",
            "locale": "en-US",
            "baseline_type": "Observed appearance; not design approval",
        }, indent=2), encoding="utf-8")
    else:
        compare_screenshot(screenshot, baseline, output / name)
