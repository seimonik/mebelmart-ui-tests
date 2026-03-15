from playwright.sync_api import Page, expect


class SofasPage:
    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page
        self.price_min = page.locator('input[placeholder*="от"]')  # CSS для мин. цены
        self.price_max = page.locator('input[placeholder*="до"]')  # CSS для макс. цены
        # self.apply_filter = page.locator('button:has-text("Применить фильтр")')  # CSS
        self.product_cards = page.locator(".product-item")  # Пример CSS для товаров
        self.lotos_product = page.locator("text=Диван Лотос")  # Текст/CSS

        self.price_filter = page.locator(".filter__title_checkbox >> text=Цена")
        self.left_slider = page.locator(
            '//div[@role="slider" and @aria-valuemin="4315" and contains(@class, "min-slider-handle")]'
        )
        self.right_slider = page.locator(
            '//div[@role="slider" and @aria-valuemin="4315" and contains(@class, "max-slider-handle")]'
        )
        self.apply_filter_button = page.locator("#filterLinkContainer")

    def goto(self):
        self.page.goto(
            "https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove"
        )

    def price_filter_open(self):
        self.page.mouse.wheel(0, 500)
        self.price_filter.click()

    def apply_filter(self):
        with self.page.expect_navigation():
            self.apply_filter_button.click()

    def set_price_filter(self, min_price: str, max_price: str):
        self.price_min.fill(min_price)
        self.price_max.fill(max_price)
        self.page.wait_for_selector(
            'button:has-text("Применить фильтр")', state="visible"
        )  # Явное ожидание
        self.apply_filter_button.click()

    def verify_product_visible(self, product_name: str):
        expect(self.page.locator(f"text={product_name}")).to_be_visible()

    def add_product_to_favorites_by_name(self, product_name: str):
        """Находит товар по названию и добавляет в избранное"""
        # Находим карточку товара по тексту в заголовке
        product_card = self.page.locator(".col-sm-6.col-lg-4").filter(
            has=self.page.get_by_text(product_name, exact=True)
        )

        # Получаем название для логов
        actual_name = product_card.locator(".product-card__name b a").inner_text()
        self.logger.info(f"Найден товар: '{actual_name}'")

        # Иконка избранного внутри карточки
        favorites_icon = product_card.locator(".product-card__favorites .favorite-icon")

        # Сохраняем состояние до клика
        was_active_before = favorites_icon.get_attribute("class") or ""
        self.logger.info(f"Состояние иконки до: {was_active_before}")

        favorites_icon.click()
        self.page.wait_for_timeout(1000)

        # Проверяем изменение состояния
        was_active_after = favorites_icon.get_attribute("class") or ""
        expect(favorites_icon).to_have_class("favorite-icon active")
        self.logger.info(f"Состояние иконки после: {was_active_after}")
        self.logger.info("Товар добавлен в Избранное")

        return actual_name
    
    def go_to_favorites(self):
        """Переход в раздел Избранное и ожидание загрузки"""
        self.logger.info("Переход в раздел 'Избранное'")

        favorites_link = self.page.locator('.header-laptop__favorite .favorite-informer')
    
        expect(favorites_link).to_be_visible()
        self.logger.info("Кнопка 'Избранное' найдена")
    
        with self.page.expect_navigation():
            favorites_link.click()
    
        expect(self.page.locator('.page-favorite')).to_be_visible(timeout=10000)
        self.logger.info("Страница Избранное загружена")
    
    def search_product(self, search_query: str):
        """Поиск товара по названию"""
        self.logger.info(f"Поиск: '{search_query}'")
    
        search_input = self.page.locator('input.searchInput.border.border-light.rounded-right.form-control.pr-5.flex-grow-1[name="query"]')
        
        # search_input = self.page.locator('input[placeholder*="Поиск"], input[name="q"], .search-input')
        search_input.click()
        search_input.fill(search_query)
        self.logger.info(f"Введен запрос: '{search_query}'")
    
        # Нажимаем Enter
        with self.page.expect_navigation():
            search_input.press('Enter')
    
        expect(self.page.locator('.page-search.mb-5')).to_be_visible(timeout=10000)
        self.logger.info("Результаты поиска загружены")
    
    def verify_search_first_result(self, expected_word: str):
        """Проверяет, что первый результат содержит ожидаемое слово"""
        first_product_card = self.page.locator('.col-md-4.mb-4').first
        expect(first_product_card).to_be_visible()

        first_title_locator = first_product_card.locator('.product-card__name b a')
        first_title = first_title_locator.inner_text()

        self.logger.info(f"Первый результат: '{first_title}'")

        assert expected_word.lower() in first_title.lower(), \
            f"'{expected_word}' не найден в первом результате: '{first_title}'"
    
        self.logger.info(f"Первый результат содержит '{expected_word}'")
        return first_title
