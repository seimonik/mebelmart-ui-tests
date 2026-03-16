from playwright.sync_api import Page, expect


class SofasPage:
    def __init__(self, page: Page, logger):
        self.logger = logger
        self.page = page

    def goto(self):
        self.page.goto(
            "https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove"
        )

    def filter_open(self, filter_name: str):
        self.page.locator(f".filter__title_checkbox >> text={filter_name}").click()

    def choose(self, option: str):
        self.page.get_by_text(option).click()

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

        favorites_link = self.page.locator(
            ".header-laptop__favorite .favorite-informer"
        )

        expect(favorites_link).to_be_visible()
        self.logger.info("Кнопка 'Избранное' найдена")

        with self.page.expect_navigation():
            favorites_link.click()

        expect(self.page.locator(".page-favorite")).to_be_visible(timeout=10000)
        self.logger.info("Страница Избранное загружена")

    def search_product(self, search_query: str):
        """Поиск товара по названию"""
        self.logger.info(f"Поиск: '{search_query}'")

        search_input = self.page.locator(
            'input.searchInput.border.border-light.rounded-right.form-control.pr-5.flex-grow-1[name="query"]'
        )

        search_input.click()
        search_input.fill(search_query)
        self.logger.info(f"Введен запрос: '{search_query}'")

        # Нажимаем Enter
        with self.page.expect_navigation():
            search_input.press("Enter")

        expect(self.page.locator(".page-search.mb-5")).to_be_visible(timeout=10000)
        self.logger.info("Результаты поиска загружены")

    def verify_search_first_result(self, expected_word: str):
        """Проверяет, что первый результат содержит ожидаемое слово"""
        first_product_card = self.page.locator(".col-md-4.mb-4").first
        expect(first_product_card).to_be_visible()

        first_title_locator = first_product_card.locator(".product-card__name b a")
        first_title = first_title_locator.inner_text()

        self.logger.info(f"Первый результат: '{first_title}'")

        assert (
            expected_word.lower() in first_title.lower()
        ), f"'{expected_word}' не найден в первом результате: '{first_title}'"

        self.logger.info(f"Первый результат содержит '{expected_word}'")
        return first_title

    def add_first_product_to_cart(self):
        """Добавляет первый товар в корзину"""
        self.logger.info("Добавление первого товара в корзину")

        first_card = self.page.locator(".col-sm-6.col-lg-4.mb-4").first

        price_text = first_card.locator(".product-card__now_price span b").inner_text()
        cart_price = int(price_text.replace(" ", "").replace("₽", ""))

        actual_name = first_card.locator(".product-card__name b a").inner_text()

        self.logger.info(f"Товар: '{actual_name}', Цена: {cart_price}₽")

        buy_button = first_card.locator("a.btn.btn-primary.btn-block")
        expect(buy_button).to_be_visible()

        buy_button.click()
        self.page.wait_for_timeout(1500)

        # Кнопка "В корзину" на странице товара
        add_to_cart_btn = self.page.locator('a.btnToCart:has-text("В корзину")')
        expect(add_to_cart_btn).to_be_visible()

        add_to_cart_btn.click()
        self.page.wait_for_timeout(2000)

        # Авто-OK для всех confirm
        self.page.on("dialog", lambda dialog: dialog.accept())

        self.logger.info("Первый товар в корзине")
        return actual_name, cart_price

    def go_to_cart(self):
        """Переход в корзину"""
        self.logger.info("Переход в корзину")

        cart_link = self.page.locator(".header-laptop__cart a")
        expect(cart_link).to_be_visible()

        with self.page.expect_navigation():
            cart_link.click()

        expect(self.page.locator(".container.mb-5")).to_be_visible()

    def verify_cart_content(self, expected_name: str, expected_price: int):
        """Проверяет товар и цену в корзине по вашей HTML-структуре"""
        expect(self.page.locator(".list-group")).to_be_visible()

        cart_item = self.page.locator(".list-group-item a.font-weight-bold").filter(
            has=self.page.get_by_text(expected_name)
        )
        expect(cart_item).to_be_visible()
        self.logger.info(f"'{expected_name}' найден в корзине")

        cart_price_elem = self.page.locator(".list-group-item .col-md-2.py-2").first
        cart_price_text = cart_price_elem.inner_text().strip()

        cart_price = int("".join(filter(str.isdigit, cart_price_text)))

        self.logger.info(f"Корзина: '{cart_price_text}' → {cart_price}₽")

        assert cart_price == expected_price, (
            f"Цены не совпадают\n"
            f"Каталог: {expected_price}₽\n"
            f"Корзина:  {cart_price}₽\n"
            f"Элемент: '{cart_price_text}'"
        )

        # Итоговая сумма должна совпадать с ценой 1 товара
        total_price_elem = self.page.locator('xpath=//h2[contains(text(), "Итого:")]')
        # total_price_elem = self.page.locator('h2: has-text("Итого: ")').first
        total_text = total_price_elem.inner_text()
        total_price = int("".join(filter(str.isdigit, total_text)))

        assert (
            total_price == expected_price
        ), f"Итоговая сумма не совпадает!\nОжидалось: {expected_price}₽\nПолучено: {total_price}₽"
