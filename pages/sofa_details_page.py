from playwright.sync_api import Page, expect


class SofaDetailsPage:
    """Страница деталей дивана"""

    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page
        self.width_xpath = "//td[contains(., 'Ширина')]/following-sibling::td"
        self.add_to_cart_button = '.btnToCart:has-text("В корзину")'

    def open_characteristics(self):
        """Открыть характеристики"""
        characteristics_tab = self.page.get_by_role("tab", name="Характеристики")
        characteristics_tab.wait_for(state="visible")
        characteristics_tab.click()
        self.logger.info("Открыты характеристики")

    def get_sofa_width(self) -> str:
        """Получить ширину дивана из характеристик"""
        actual_width = self.page.locator(self.width_xpath).inner_text().strip()
        self.logger.info(f"Ширина дивана: '{actual_width}'")
        return actual_width
    
    def click_add_to_cart(self, product_name: str):
        """Нажать кнопку 'В корзину' на странице товара"""
        expect(self.page.get_by_role("heading", name=product_name)).to_be_visible()
        button = self.page.locator("//div[contains(@class, 'page-product__buy')]//a[contains(@class, 'btnToCart')]")
        button.wait_for(state="visible")
        self.page.once("dialog", lambda dialog: dialog.accept()) # cancel, ok - accept
        button.click()
        self.page.wait_for_timeout(5000)
        self.logger.info("Товар добавлен в корзину со страницы карточки товара")

