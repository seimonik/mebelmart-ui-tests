from pages.sofas_page import SofasPage


def test_divany_filter(page, logger):
    """Параметризованный тест фильтрации стилей диванов"""

    logger.info("Запуск теста фильтрации диванов")
    sofas_page = SofasPage(page, logger)
    sofas_page.goto()

    sofas_page.filter_open("Стиль")

    sofas_page.choose("лофт (loft)")

    sofas_page.apply_filter()

    sofas_page.verify_product_visible("Диван Наоми")
