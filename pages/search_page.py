from playwright.sync_api import Page


class SearchPage:
    """Страница избранных товаров"""

    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page
        self.product_card = ".product-card"
        self.product_card_name = ".product-card__name"
    
    def verify_first_search_result(self, search_query):
        self.page.locator(self.product_card).first.wait_for(state="visible", timeout=10000)
        
        first_card = self.page.locator(self.product_card).first

        first_product_name = first_card.locator(self.product_card_name).inner_text()
    
        self.logger.info(f"Первый товар в списке: '{first_product_name.strip()}'")
    
        assert search_query.lower() in first_product_name.lower(), \
            f"Ожидали '{search_query}' в названии первого товара, но получили '{first_product_name}'"

