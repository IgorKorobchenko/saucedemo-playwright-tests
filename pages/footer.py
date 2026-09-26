import re

from playwright.sync_api import Page, expect


class Footer:
    """Shared footer; verifies application links without visiting social sites."""

    def __init__(self, page: Page):
        self.root = page.get_by_test_id("footer")
        self.copy = self.root.get_by_test_id("footer-copy")
        self.links = {
            "X": (self.root.get_by_test_id("social-x"), "https://x.com/saucelabs"),
            "Facebook": (self.root.get_by_test_id("social-facebook"), "https://www.facebook.com/saucelabs"),
            "LinkedIn": (self.root.get_by_test_id("social-linkedin"), "https://www.linkedin.com/company/sauce-labs/"),
        }

    def expect_content(self):
        expect(self.root).to_be_visible()
        expect(self.copy).to_have_text(re.compile(
            r"^© \d{4} Sauce Labs\. All Rights Reserved\. Terms of Service \| Privacy Policy$"
        ))
        for label, (link, destination) in self.links.items():
            expect(link).to_be_visible()
            expect(link).to_have_text(label)
            expect(link).to_have_attribute("href", destination)
            expect(link).to_have_attribute("target", "_blank")
