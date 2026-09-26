import json
from pathlib import Path

# Captured from standard_user inventory on 2026-09-25; reviewed, not read live
# during test execution. Changes in product content should fail the assertions.
PRODUCTS = json.loads(Path(__file__).with_suffix(".json").read_text(encoding="utf-8"))
