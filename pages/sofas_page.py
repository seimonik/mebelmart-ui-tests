from playwright.sync_api import Page, expect


class SofasPage:
    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page
        self.sofa_page_check = "//h1[contains(@class, 'mb-4') and normalize-space()='Диваны']"
        self.favorites_icon = ".product-card__favorites .favorite-icon"
        self.favorites_icon_active_class = "favorite-icon active"
        self.icon_favorites = ".header-laptop__favorite .favorite-informer"
        self.search_input = "input[name='query']"
        self.product_card = ".product-card"
        self.product_name = ".product-card__name"
        self.buy_button = "a.btn-primary:has-text('Купить')"
        self.product_price = ".product-card__now_price span b"
        self.icon_cart = ".header-laptop__cart a"

    def goto(self):
        self.page.goto(
            "https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove"
        )
        self.page.wait_for_selector(self.sofa_page_check)

    def filter_open(self, filter_name: str):
        self.page.locator(f".filter__title_checkbox >> text={filter_name}").click()
        self.logger.info(f"Открыта область '{filter_name}' фильтра")

    def choose(self, filter_name: str, option: str):
        self.page.locator(".filter__item").filter(has_text=filter_name).get_by_role("link", name=option).click()
        self.logger.info(f"Выбрана фильтрация по '{option}'")

    def apply_filter(self):
        with self.page.expect_navigation(timeout=10000):
            self.page.get_by_text("Применить фильтр").click()

    def verify_product_visible(self, product_name: str):
        expect(self.page.locator(f"text={product_name}")).to_be_visible()

    def find_and_click_sofa(self, sofa_name: str):
        """Найти и кликнуть на диван по названию"""
        sofa_item = self.page.locator(f"text={sofa_name}").first
        expect(sofa_item).to_be_visible()
        sofa_item.click()
        self.logger.info(f"Клик по дивану: '{sofa_name}'")
        return sofa_name

    def add_product_to_favorites_by_name(self, product_name: str):
        """Находит товар по названию и добавляет в избранное"""
        # Находим карточку товара по тексту в заголовке
        product_card = self.page.locator(".product-card").filter(has_text=product_name).first
        self.logger.info(f"Найден товар: '{product_name}'")

        # Иконка избранного внутри карточки
        favorites_icon = product_card.locator(self.favorites_icon)

        # Сохраняем состояние до клика
        was_active_before = favorites_icon.get_attribute("class") or ""
        self.logger.info(f"Состояние иконки до: {was_active_before}")

        favorites_icon.click()
        self.page.wait_for_timeout(1000)

        # Проверяем изменение состояния
        was_active_after = favorites_icon.get_attribute("class") or ""
        expect(favorites_icon).to_have_class(self.favorites_icon_active_class)
        self.logger.info(f"Состояние иконки после: {was_active_after}")
        self.logger.info("Товар добавлен в Избранное")

    def go_to_favorites(self):
        """Переход в раздел Избранное и ожидание загрузки"""
        self.logger.info("Переход в раздел 'Избранное'")

        favorites_btn = self.page.locator(self.icon_favorites)

        expect(favorites_btn).to_be_visible()
        self.logger.info("Кнопка 'Избранное' найдена")

        favorites_btn.click()

    def search_product(self, search_query: str):
        """Поиск товара по названию"""
        search_input = self.page.locator(self.search_input).locator("visible=true")
        search_input.fill(search_query)
        self.logger.info(f"Введен запрос: '{search_query}'")
        search_input.press("Enter")

    def add_product_to_cart(self, product_name: str):
        self.logger.info(f"Добавление товара '{product_name}' в корзину")
    
        # Находим конкретную карточку по тексту названия
        target_card = self.page.locator(self.product_card).filter(
            has=self.page.locator(self.product_name, has_text=product_name)
        ).first
    
        # Кликаем по кнопке "Купить" в карточке
        target_card.locator(self.buy_button).click()
    
        self.logger.info(f"Нажата кнопка 'Купить' для '{product_name}'")
    
    def get_product_price(self, product_name: str) -> str:
        """Получить цену товара по его названию"""
        card = self.page.locator(self.product_card).filter(
            has=self.page.locator(self.product_name, has_text=product_name)
        ).first

        card.wait_for(state="visible")
        
        raw_price = card.locator(self.product_price).last.inner_text()
        clean_price = raw_price.replace("\xa0", "").replace(" ", "").strip()
        
        self.logger.info(f"Цена товара '{product_name}': {clean_price}")
        return clean_price

    def go_to_cart(self):
        """Переход в корзину"""
        self.logger.info("Переход в корзину")

        cart_link = self.page.locator(self.icon_cart)
        expect(cart_link).to_be_visible()
        cart_link.click()
