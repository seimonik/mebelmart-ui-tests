import re

from playwright.sync_api import Page


class CartPage:
    """Страница корзины"""

    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page
        self.price_column = ".col-md-2"
    
    def get_item_price(self, product_name: str) -> str:
        row = self.page.locator("div").filter(has=self.page.get_by_role("link", name=product_name)).first
        raw_price = row.locator(self.price_column).first.inner_text()
        return re.sub(r"\D", "", raw_price)

    def get_total_sum(self) -> str:
        raw_total = self.page.locator("text=/^Итого:/").inner_text()
        return re.sub(r"\D", "", raw_total)
