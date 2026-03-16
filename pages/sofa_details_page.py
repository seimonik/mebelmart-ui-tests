from playwright.async_api import Page
from playwright.sync_api import expect


class SofaDetailsPage:
    """Страница деталей дивана"""

    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page

    def wait_for_page_load(self, sofa_id: str):
        """Ждем загрузки страницы товара"""
        self.page.wait_for_url(f"**/{sofa_id}", timeout=15000)
        self.logger.info("Страница товара загружена")

    def open_characteristics(self):
        """Открыть характеристики"""
        self.page.click("text=Характеристики")
        self.logger.info("Открыты характеристики")

    def get_sofa_width(self) -> str:
        """Получить ширину дивана из характеристик"""
        width_row = self.page.locator("tr:has-text('Ширина, мм.')")
        expect(width_row).to_be_visible()

        actual_width = width_row.locator("td:nth-child(2)").text_content().strip()
        self.logger.info(f"Ширина дивана: '{actual_width}'")
        return actual_width
