from playwright.async_api import Page
import pytest
from pages.sofas_page import SofasPage


@pytest.mark.parametrize("search_query", ["Бостон", "Лотос", "замша"])
def test_product_search(page: Page, logger, search_query: str):
    """Тест поиска товара по названию"""
    logger.info(f"Тест поиска: '{search_query}'")

    sofas_page = SofasPage(page, logger)
    sofas_page.goto()

    sofas_page.search_product(search_query)
    sofas_page.verify_search_first_result(search_query)
