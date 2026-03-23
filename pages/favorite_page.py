from playwright.sync_api import Page


class FavoritePage:
    """Страница избранных товаров"""

    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page
        self.favorite_link = "**/favorite"

    def goto(self):
        self.page.goto("https://mebelmart-saratov.ru/favorite")

    def confirm_favorites_url(self):
        self.page.wait_for_url(self.favorite_link, wait_until="networkidle")
        self.logger.info("Переход в раздел Избранное выполнен")
